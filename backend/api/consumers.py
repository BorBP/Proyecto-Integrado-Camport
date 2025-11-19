import json
from datetime import datetime, timedelta
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.models import Animal, Telemetria, Alerta, AlertaUsuario
from shapely.geometry import Point, Polygon
import time


class TelemetriaConsumer(AsyncWebsocketConsumer):
    # Sistema de cooldown para alertas (diccionario compartido entre instancias a nivel de clase)
    alert_cooldowns = {}
    last_cleanup = time.time()  # Timestamp de última limpieza
    
    # Configuración de tiempos
    COOLDOWN_VITALS = 40  # 40 segundos para temperatura y BPM
    COOLDOWN_PERIMETER = 30  # 30 segundos para alertas de perímetro
    CLEANUP_INTERVAL = 300  # Limpiar cooldowns expirados cada 5 minutos
    
    # Desfase entre tipos de alertas para distribuir temporalmente
    OFFSET_TEMPERATURE = 0   # Temperatura: sin desfase (t=0s)
    OFFSET_BPM = 30          # BPM: 30 segundos después (t=30s)
    OFFSET_PERIMETER = 60    # Perímetro: 60 segundos después (t=60s)

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
            
            # Log de recepción de telemetría
            print(f"📡 Telemetría recibida: {telemetria['collar_id']} - "
                  f"Pos:({telemetria['latitud']:.5f},{telemetria['longitud']:.5f}) "
                  f"Temp:{telemetria['temperatura_corporal']}°C "
                  f"BPM:{telemetria['frecuencia_cardiaca']} "
                  f"Alertas:{len(alertas)}")

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
        # Asegurar que los datos se envían correctamente al frontend
        try:
            data_to_send = event['data']
            # Log para debugging
            print(f"🔄 Enviando al frontend: {data_to_send['collar_id']} - Pos:({data_to_send['latitud']},{data_to_send['longitud']})")
            await self.send(text_data=json.dumps(data_to_send))
        except Exception as e:
            print(f"❌ Error enviando al frontend: {e}")

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

    def cleanup_expired_cooldowns(self):
        """
        Limpia cooldowns expirados del diccionario para evitar acumulación infinita.
        Se ejecuta periódicamente cada CLEANUP_INTERVAL segundos.
        """
        now = time.time()
        
        # Solo limpiar si ha pasado el intervalo de limpieza
        if now - self.last_cleanup < self.CLEANUP_INTERVAL:
            return
        
        # Calcular el tiempo máximo de cooldown
        max_cooldown = max(self.COOLDOWN_VITALS, self.COOLDOWN_PERIMETER)
        
        # Identificar keys expirados
        expired_keys = []
        for key, timestamp in self.alert_cooldowns.items():
            if now - timestamp > max_cooldown * 2:  # Doble del cooldown máximo para seguridad
                expired_keys.append(key)
        
        # Eliminar keys expirados
        for key in expired_keys:
            del self.alert_cooldowns[key]
        
        if expired_keys:
            print(f"🧹 Limpieza de cooldowns: {len(expired_keys)} registros antiguos eliminados")
        
        # Actualizar timestamp de última limpieza
        self.last_cleanup = now
    
    def can_send_alert(self, collar_id, alert_category, cooldown_seconds):
        """
        Verifica si se puede enviar una alerta basándose en el cooldown.
        
        Args:
            collar_id: ID del collar del animal
            alert_category: Categoría de alerta ('temp', 'bpm', 'perimeter')
            cooldown_seconds: Tiempo de cooldown en segundos
        
        Returns:
            bool: True si puede enviar la alerta, False si está en cooldown
        """
        # Ejecutar limpieza periódica
        self.cleanup_expired_cooldowns()
        
        now = time.time()
        key = f"{collar_id}_{alert_category}"

        if key in self.alert_cooldowns:
            last_alert_time = self.alert_cooldowns[key]
            time_diff = now - last_alert_time

            if time_diff < cooldown_seconds:
                remaining = int(cooldown_seconds - time_diff)
                print(f"⏱️  Cooldown activo para {collar_id} - {alert_category}: {remaining}s restantes")
                return False

        # Actualizar timestamp de última alerta
        self.alert_cooldowns[key] = now
        print(f"✅ Alerta permitida para {collar_id} - {alert_category}")
        return True

    @database_sync_to_async
    def check_alerts(self, telemetria_data):
        """Verifica si se deben generar alertas - CON COOLDOWN Y VARIACIÓN DE ANIMALES"""
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
                if self.can_send_alert(animal.collar_id, 'temp', self.COOLDOWN_VITALS):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='TEMPERATURA',
                        mensaje=f'Fiebre detectada: {temp}°C (Animal: {animal.display_id or animal.collar_id})',
                        valor_registrado=temp
                    )
                    # Crear alertas para todos los usuarios
                    usuarios = User.objects.all()
                    alert_usuarios_created = 0
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                        alert_usuarios_created += 1
                    print(f"🌡️🔥 ALERTA CREADA EN BD: {alerta.mensaje} - Temp: {temp}°C - {alert_usuarios_created} usuarios notificados")
                    alertas.append({
                        'tipo': 'TEMPERATURA',
                        'subtipo': 'FIEBRE',
                        'mensaje': alerta.mensaje,
                        'valor': float(temp),
                        'collar_id': animal.collar_id
                    })
            elif temp < 37.5:
                if self.can_send_alert(animal.collar_id, 'temp', self.COOLDOWN_VITALS):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='TEMPERATURA',
                        mensaje=f'Hipotermia detectada: {temp}°C (Animal: {animal.display_id or animal.collar_id})',
                        valor_registrado=temp
                    )
                    # Crear alertas para todos los usuarios
                    usuarios = User.objects.all()
                    alert_usuarios_created = 0
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                        alert_usuarios_created += 1
                    print(f"🌡️❄️ ALERTA CREADA EN BD: {alerta.mensaje} - Temp: {temp}°C - {alert_usuarios_created} usuarios notificados")
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
                if self.can_send_alert(animal.collar_id, 'bpm', self.COOLDOWN_VITALS):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='FRECUENCIA',
                        mensaje=f'Frecuencia cardíaca alta: {fc} lpm (Animal: {animal.display_id or animal.collar_id})',
                        valor_registrado=fc
                    )
                    # Crear alertas para todos los usuarios
                    usuarios = User.objects.all()
                    alert_usuarios_created = 0
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                        alert_usuarios_created += 1
                    print(f"❤️⬆️ ALERTA CREADA EN BD: {alerta.mensaje} - BPM: {fc} - {alert_usuarios_created} usuarios notificados")
                    alertas.append({
                        'tipo': 'FRECUENCIA',
                        'subtipo': 'AGITACION',
                        'mensaje': alerta.mensaje,
                        'valor': int(fc),
                        'collar_id': animal.collar_id
                    })
            elif fc < 40:
                if self.can_send_alert(animal.collar_id, 'bpm', self.COOLDOWN_VITALS):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='FRECUENCIA',
                        mensaje=f'Frecuencia cardíaca baja: {fc} lpm (Animal: {animal.display_id or animal.collar_id})',
                        valor_registrado=fc
                    )
                    # Crear alertas para todos los usuarios
                    usuarios = User.objects.all()
                    alert_usuarios_created = 0
                    for usuario in usuarios:
                        AlertaUsuario.objects.create(
                            alerta=alerta,
                            usuario=usuario,
                            leido=False
                        )
                        alert_usuarios_created += 1
                    print(f"❤️⬇️ ALERTA CREADA EN BD: {alerta.mensaje} - BPM: {fc} - {alert_usuarios_created} usuarios notificados")
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
                    if self.can_send_alert(animal.collar_id, 'perimeter', self.COOLDOWN_PERIMETER):
                        alerta = Alerta.objects.create(
                            animal=animal,
                            tipo_alerta='PERIMETRO',
                            mensaje=f'Animal {animal.display_id or animal.collar_id} fuera de geocerca "{geocerca.nombre}"'
                        )
                        # Crear alertas para todos los usuarios
                        usuarios = User.objects.all()
                        alert_usuarios_created = 0
                        for usuario in usuarios:
                            AlertaUsuario.objects.create(
                                alerta=alerta,
                                usuario=usuario,
                                leido=False
                            )
                            alert_usuarios_created += 1
                        print(f"🚨 ALERTA CREADA EN BD: {alerta.mensaje} - {alert_usuarios_created} usuarios notificados")
                        alertas.append({
                            'tipo': 'PERIMETRO',
                            'subtipo': 'FUGA',
                            'mensaje': alerta.mensaje,
                            'geocerca': geocerca.nombre,
                            'collar_id': animal.collar_id
                        })

        except Animal.DoesNotExist:
            print(f"❌ Animal no encontrado: {telemetria_data.get('collar_id', 'UNKNOWN')}")
        except Exception as e:
            print(f"❌ ERROR en check_alerts: {str(e)}")
            import traceback
            traceback.print_exc()

        return alertas
