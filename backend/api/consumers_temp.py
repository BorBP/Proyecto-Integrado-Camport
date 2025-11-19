import json
from datetime import datetime, timedelta
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Animal, Telemetria, Geocerca, Alerta, AlertaUsuario, User
from shapely.geometry import Point, Polygon

class TelemetriaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("telemetria", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("telemetria", self.channel_name)

    async def receive(self, text_data):
        """Recibe datos de telemetría y los procesa"""
        try:
            data = json.loads(text_data)
            
            # Guardar telemetría en la base de datos
            telemetria = await self.save_telemetria(data)
            
            # Verificar alertas
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
        except Exception as e:
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
            'latitud': telemetria.latitud,
            'longitud': telemetria.longitud,
            'temperatura_corporal': telemetria.temperatura_corporal,
            'frecuencia_cardiaca': telemetria.frecuencia_cardiaca,
            'timestamp': telemetria.timestamp.isoformat()
        }

    @database_sync_to_async
    def check_alerts(self, telemetria_data):
        """Verifica si se deben generar alertas"""
        alertas = []
        animal = Animal.objects.get(collar_id=telemetria_data['collar_id'])
        
        # Verificar temperatura
        temp = telemetria_data['temperatura_corporal']
        if temp > 40:
            alerta = Alerta.objects.create(
                animal=animal,
                tipo_alerta='TEMPERATURA',
                mensaje=f'Fiebre detectada: {temp}°C (Animal: {animal.display_id or animal.collar_id})'
            )
            self.create_user_alerts(alerta)
            alertas.append({
                'tipo': 'TEMPERATURA',
                'mensaje': alerta.mensaje
            })
        elif temp < 37.5:
            alerta = Alerta.objects.create(
                animal=animal,
                tipo_alerta='TEMPERATURA',
                mensaje=f'Hipotermia detectada: {temp}°C (Animal: {animal.display_id or animal.collar_id})'
            )
            self.create_user_alerts(alerta)
            alertas.append({
                'tipo': 'TEMPERATURA',
                'mensaje': alerta.mensaje
            })
        
        # Verificar frecuencia cardíaca
        fc = telemetria_data['frecuencia_cardiaca']
        if fc > 120:
            alerta = Alerta.objects.create(
                animal=animal,
                tipo_alerta='FRECUENCIA',
                mensaje=f'Frecuencia cardíaca alta: {fc} lpm (Animal: {animal.display_id or animal.collar_id})'
            )
            self.create_user_alerts(alerta)
            alertas.append({
                'tipo': 'FRECUENCIA',
                'mensaje': alerta.mensaje
            })
        elif fc < 40:
            alerta = Alerta.objects.create(
                animal=animal,
                tipo_alerta='FRECUENCIA',
                mensaje=f'Frecuencia cardíaca baja: {fc} lpm (Animal: {animal.display_id or animal.collar_id})'
            )
            self.create_user_alerts(alerta)
            alertas.append({
                'tipo': 'FRECUENCIA',
                'mensaje': alerta.mensaje
            })
        
        # Verificar perímetro - usar la geocerca asignada al animal
        try:
            # Obtener la geocerca asignada al animal
            geocerca = animal.geocerca
            if geocerca and geocerca.activa:
                point = Point(telemetria_data['longitud'], telemetria_data['latitud'])
                polygon_coords = [(coord['lng'], coord['lat']) for coord in geocerca.coordenadas]
                polygon = Polygon(polygon_coords)
                
                if not polygon.contains(point):
                    alerta = Alerta.objects.create(
                        animal=animal,
                        tipo_alerta='PERIMETRO',
                        mensaje=f'Animal {animal.display_id or animal.collar_id} fuera de geocerca "{geocerca.nombre}"'
                    )
                    self.create_user_alerts(alerta)
                    alertas.append({
                        'tipo': 'PERIMETRO',
                        'mensaje': alerta.mensaje
                    })
        except Exception as e:
            pass
        
        return alertas

    def create_user_alerts(self, alerta):
        """Crea alertas para todos los usuarios"""
        users = User.objects.filter(is_active=True)
        for user in users:
            AlertaUsuario.objects.create(
                alerta=alerta,
                usuario=user,
                leido=False
            )
