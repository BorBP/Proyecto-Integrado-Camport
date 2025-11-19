import json
from datetime import datetime, timedelta
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import Animal, Telemetria, Alerta, AlertaUsuario
from shapely.geometry import Point, Polygon
import time


class TelemetriaConsumer(AsyncWebsocketConsumer):
    # Sistema de cooldown para alertas (diccionario compartido entre instancias)
    alert_cooldowns = {}
    COOLDOWN_BASE = 90  # 90 segundos (1:30 min) - base para todas las alertas
    
    # Desfase entre tipos de alertas para evitar spam simultáneo
    OFFSET_TEMPERATURE = 0   # Temperatura: sin desfase
    OFFSET_BPM = 30          # BPM: 30 segundos después de temperatura
    OFFSET_PERIMETER = 60    # Perímetro: 60 segundos después de temperatura

    async def connect(self):
        """Conecta el WebSocket"""
        await self.channel_layer.group_add("telemetria", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Desconecta el WebSocket"""
        await self.channel_layer.group_discard("telemetria", self.channel_name)

    async def receive(self, text_data):
        """Recibe datos de telemetría y los procesa"""
        try:
            data = json.loads(text_data)

            # Guardar telemetría en la base de datos
            telemetria = await self.save_telemetria(data)

            # Verificar alertas CON COOLDOWN
            alertas = await self.check_alerts(telemetria)

            # Enviar actualización a todos los clientes conectados
            await self.channel_layer.group_send(
                "telemetria",
                {
                    "type": "telemetria_update",
                    "data": {
                        "collar_id": telemetria['collar_id'],
                        "tipo_animal": telemetria['tipo_animal'],
                        "latitud": telemetria['latitud'],
                        "longitud": telemetria['longitud'],
                        "temperatura_corporal": telemetria['temperatura_corporal'],
                        "frecuencia_cardiaca": telemetria['frecuencia_cardiaca'],
                        "timestamp": telemetria['timestamp'],
                        "alertas": alertas
                    }
                }
            )

            # Responder al emisor
            await self.send(text_data=json.dumps({
                'status': 'success',
                'collar_id': telemetria['collar_id'],
                'alertas': alertas
            }))

        except Exception as e:
            print(f"❌ ERROR en consumer.receive: {str(e)}")
            import traceback
            traceback.print_exc()
            await self.send(text_data=json.dumps({
                'error': str(e)
            }))

    async def telemetria_update(self, event):
        """Envía actualización de telemetría al cliente"""
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def save_telemetria(self, data):
        """Guarda la telemetría en la base de datos"""
        animal = Animal.objects.get(collar_id=data['collar_id'])

        telemetria = Telemetria.objects.create(
            animal=animal,
            latitud=data['latitud'],
            longitud=data['longitud'],
            temperatura_corporal=data['temperatura_corporal'],
            frecuencia_cardiaca=data['frecuencia_cardiaca']
        )

        return {
            'collar_id': animal.collar_id,
            'tipo_animal': animal.tipo_animal,
            'latitud': float(telemetria.latitud),
            'longitud': float(telemetria.longitud),
            'temperatura_corporal': float(telemetria.temperatura_corporal),
            'frecuencia_cardiaca': int(telemetria.frecuencia_cardiaca),
            'timestamp': telemetria.timestamp.isoformat()
        }

    def can_send_alert(self, collar_id, alert_type, offset_seconds=0):
        """
        Verifica si se puede enviar una alerta basándose en el cooldown y offset.
        
        Args:
            collar_id: ID del collar del animal
            alert_type: Tipo de alerta (TEMPERATURA_ALTA, FRECUENCIA_BAJA, etc.)
            offset_seconds: Desfase inicial para este tipo de alerta
        
        Returns:
            bool: True si puede enviar la alerta, False si está en cooldown
        """
        now = time.time()
        key = f"{collar_id}_{alert_type}"

        if key in self.alert_cooldowns:
            last_alert_time = self.alert_cooldowns[key]
            time_diff = now - last_alert_time
            
            # El cooldown efectivo incluye el offset
            cooldown_total = self.COOLDOWN_BASE + offset_seconds

            if time_diff < cooldown_total:
                remaining = int(cooldown_total - time_diff)
                print(f"⏱️  Cooldown activo para {collar_id} - {alert_type}: {remaining}s restantes")
                return False
        else:
            # Primera vez que se intenta enviar esta alerta
            # Aplicar el offset inicial
            if offset_seconds > 0:
                # Verificar si ya pasó el offset desde el inicio del sistema
                init_key = f"_init_{alert_type}"
                if init_key not in self.alert_cooldowns:
                    self.alert_cooldowns[init_key] = now
                    print(f"⏲️  Offset inicial de {offset_seconds}s para tipo {alert_type}")
                    return False
                
                init_time = self.alert_cooldowns[init_key]
                if (now - init_time) < offset_seconds:
                    remaining = int(offset_seconds - (now - init_time))
                    print(f"⏲️  Esperando offset inicial para {alert_type}: {remaining}s restantes")
                    return False

        # Actualizar timestamp de última alerta
        self.alert_cooldowns[key] = now
        return True

    @database_sync_to_async
    def check_alerts(self, telemetria_data):
        """Verifica si se deben generar alertas - CON COOLDOWN"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        alertas = []
        try:
            animal = Animal.objects.get(collar_id=telemetria_data['collar_id'])

            # CONDICIÓN 0: Si NO tiene geocerca asignada, NO generar alertas (silencio total)
            if not animal.geocerca:
                return alertas

            # ===============================
            # ALERTAS DE TEMPERATURA
            # ===============================
            temp = telemetria_data['temperatura_corporal']

            if temp > 40:
                if self.can_send_alert(animal.collar_id, 'TEMPERATURA_ALTA', self.OFFSET_TEMPERATURE):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='TEMPERATURA',
                        mensaje=f'Fiebre detectada: {temp}°C (Animal: {animal.display_id or animal.collar_id})'
                    )
                    # Crear alertas para todos los usuarios DENTRO DE ESTA FUNCIÓN
                    usuarios = User.objects.all()
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                    print(f"🌡️🔥 ALERTA CREADA EN BD: {alerta.mensaje}")
                    alertas.append({
                        'tipo': 'TEMPERATURA',
                        'subtipo': 'FIEBRE',
                        'mensaje': alerta.mensaje,
                        'valor': float(temp),
                        'collar_id': animal.collar_id
                    })
            elif temp < 37.5:
                if self.can_send_alert(animal.collar_id, 'TEMPERATURA_BAJA', self.OFFSET_TEMPERATURE):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='TEMPERATURA',
                        mensaje=f'Hipotermia detectada: {temp}°C (Animal: {animal.display_id or animal.collar_id})'
                    )
                    # Crear alertas para todos los usuarios DENTRO DE ESTA FUNCIÓN
                    usuarios = User.objects.all()
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                    print(f"🌡️❄️ ALERTA CREADA EN BD: {alerta.mensaje}")
                    alertas.append({
                        'tipo': 'TEMPERATURA',
                        'subtipo': 'HIPOTERMIA',
                        'mensaje': alerta.mensaje,
                        'valor': float(temp),
                        'collar_id': animal.collar_id
                    })

            # ===============================
            # ALERTAS DE FRECUENCIA CARDÍACA
            # ===============================
            fc = telemetria_data['frecuencia_cardiaca']

            if fc > 120:
                if self.can_send_alert(animal.collar_id, 'FRECUENCIA_ALTA', self.OFFSET_BPM):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='FRECUENCIA',
                        mensaje=f'Frecuencia cardíaca alta: {fc} lpm (Animal: {animal.display_id or animal.collar_id})'
                    )
                    # Crear alertas para todos los usuarios DENTRO DE ESTA FUNCIÓN
                    usuarios = User.objects.all()
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                    print(f"❤️⬆️ ALERTA CREADA EN BD: {alerta.mensaje}")
                    alertas.append({
                        'tipo': 'FRECUENCIA',
                        'subtipo': 'AGITACION',
                        'mensaje': alerta.mensaje,
                        'valor': int(fc),
                        'collar_id': animal.collar_id
                    })
            elif fc < 40:
                if self.can_send_alert(animal.collar_id, 'FRECUENCIA_BAJA', self.OFFSET_BPM):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='FRECUENCIA',
                        mensaje=f'Frecuencia cardíaca baja: {fc} lpm (Animal: {animal.display_id or animal.collar_id})'
                    )
                    # Crear alertas para todos los usuarios DENTRO DE ESTA FUNCIÓN
                    usuarios = User.objects.all()
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                    print(f"❤️⬇️ ALERTA CREADA EN BD: {alerta.mensaje}")
                    alertas.append({
                        'tipo': 'FRECUENCIA',
                        'subtipo': 'BAJO_ESTIMULO',
                        'mensaje': alerta.mensaje,
                        'valor': int(fc),
                        'collar_id': animal.collar_id
                    })

            # ===============================
            # ALERTAS DE PERÍMETRO
            # ===============================
            geocerca = animal.geocerca
            if geocerca and geocerca.activa:
                # Crear polígono de la geocerca
                polygon_coords = [(coord['lng'], coord['lat']) for coord in geocerca.coordenadas]
                polygon = Polygon(polygon_coords)

                # Verificar si está dentro
                point = Point(telemetria_data['longitud'], telemetria_data['latitud'])

                if not polygon.contains(point):
                    if self.can_send_alert(animal.collar_id, 'PERIMETRO', self.OFFSET_PERIMETER):
                        alerta = Alerta.objects.create(
                            animal=animal,
                            tipo_alerta='PERIMETRO',
                            mensaje=f'Animal {animal.display_id or animal.collar_id} fuera de geocerca "{geocerca.nombre}"'
                        )
                        # Crear alertas para todos los usuarios DENTRO DE ESTA FUNCIÓN
                        usuarios = User.objects.all()
                        for usuario in usuarios:
                            AlertaUsuario.objects.create(
                                alerta=alerta,
                                usuario=usuario,
                                leido=False
                            )
                        print(f"🚨 ALERTA CREADA EN BD: {alerta.mensaje}")
                        alertas.append({
                            'tipo': 'PERIMETRO',
                            'subtipo': 'FUGA',
                            'mensaje': alerta.mensaje,
                            'geocerca': geocerca.nombre,
                            'collar_id': animal.collar_id
                        })

        except Exception as e:
            print(f"❌ ERROR en check_alerts: {str(e)}")
            import traceback
            traceback.print_exc()

        return alertas
