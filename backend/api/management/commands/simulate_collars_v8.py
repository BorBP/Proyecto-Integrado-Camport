"""
Management Command: simulate_collars_v8
Versión 8.0 - CAMPORT - SIGNOS VITALES REALISTAS CON INTERVALOS INDEPENDIENTES

NUEVAS CARACTERÍSTICAS V8.0:
============================
1. INTERVALOS INDEPENDIENTES:
   - Movimiento (posición): Configurable (default: 3s)
   - Temperatura: Configurable (default: 5s) 
   - Frecuencia cardíaca (BPM): Configurable (default: 2s)

2. SIGNOS VITALES COHERENTES:
   - Variación gradual y realista
   - Sin saltos bruscos
   - Rangos por especie

3. ALERTAS INTELIGENTES:
   - Solo si animal tiene geocerca asignada
   - Alertas de salud (temperatura y BPM)
   - Alertas de fuga (fuera de perímetro)
   - Sistema de cooldown para evitar spam

4. ARQUITECTURA ASÍNCRONA:
   - Múltiples tasks concurrentes
   - Un task por tipo de dato
   - Coordinación centralizada

Autor: CAMPORT Team - V8.0
Fecha: 2025
"""

import asyncio
import websockets
import json
import random
import time
import hashlib
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from shapely.geometry import Point, Polygon
from api.models import Animal, Telemetria, Geocerca


class VitalSignsManager:
    """Gestor de signos vitales con variación coherente"""
    
    def __init__(self):
        self.vital_signs = {}  # {collar_id: {'temp': X, 'bpm': Y, 'last_update': timestamp}}
        self.alert_cooldown = {}  # {collar_id: {'temp': timestamp, 'bpm': timestamp, 'perimeter': timestamp}}
    
    def initialize_animal(self, collar_id, tipo_animal):
        """Inicializa signos vitales base para un animal"""
        temp_base, bpm_base = self.get_base_vital_signs(tipo_animal)
        
        self.vital_signs[collar_id] = {
            'temperatura': temp_base,
            'bpm': bpm_base,
            'last_temp_update': time.time(),
            'last_bpm_update': time.time(),
            'tipo_animal': tipo_animal
        }
        
        self.alert_cooldown[collar_id] = {
            'temp': 0,
            'bpm': 0,
            'perimeter': 0
        }
    
    def get_base_vital_signs(self, tipo_animal):
        """Retorna signos vitales base según tipo de animal"""
        vital_ranges = {
            'OVINO': {
                'temperatura': (38.5, 39.5),
                'bpm': (70, 90)
            },
            'BOVINO': {
                'temperatura': (38.0, 39.0),
                'bpm': (60, 80)
            },
            'EQUINO': {
                'temperatura': (37.5, 38.5),
                'bpm': (28, 40)
            }
        }
        
        ranges = vital_ranges.get(tipo_animal, vital_ranges['OVINO'])
        temp = round(random.uniform(*ranges['temperatura']), 1)
        bpm = random.randint(*ranges['bpm'])
        
        return temp, bpm
    
    def update_temperature(self, collar_id, max_variation=0.3, allow_anomalies=True):
        """Actualiza temperatura con variación gradual y posibilidad de anomalías"""
        if collar_id not in self.vital_signs:
            return None
        
        current = self.vital_signs[collar_id]['temperatura']
        tipo_animal = self.vital_signs[collar_id]['tipo_animal']
        
        # Límites por especie
        limits = {
            'OVINO': (37.0, 41.0),
            'BOVINO': (37.0, 40.5),
            'EQUINO': (36.5, 40.0)
        }
        min_temp, max_temp = limits.get(tipo_animal, (37.0, 41.0))
        
        # Variación gradual con tendencia a volver al rango normal
        delta = random.uniform(-max_variation, max_variation)
        
        # Tendencia a volver al centro del rango normal
        normal_ranges = {
            'OVINO': 39.0,
            'BOVINO': 38.5,
            'EQUINO': 38.0
        }
        target = normal_ranges.get(tipo_animal, 38.5)
        
        # NUEVO: Posibilidad aleatoria de generar anomalía (para variar alertas)
        if allow_anomalies and random.random() < 0.05:  # 5% de probabilidad
            # Decidir si sube o baja
            if random.random() < 0.7:  # 70% fiebre, 30% hipotermia
                # Empujar hacia fiebre (>40°C)
                delta += 0.5
            else:
                # Empujar hacia hipotermia (<37.5°C)
                delta -= 0.5
        # Si está lejos del target, empujar suavemente hacia él
        elif abs(current - target) > 1.5:
            direction = 1 if current < target else -1
            delta += direction * 0.15
        
        new_temp = current + delta
        new_temp = max(min_temp, min(max_temp, new_temp))
        new_temp = round(new_temp, 1)
        
        self.vital_signs[collar_id]['temperatura'] = new_temp
        self.vital_signs[collar_id]['last_temp_update'] = time.time()
        
        return new_temp
    
    def update_bpm(self, collar_id, max_variation=5, allow_anomalies=True):
        """Actualiza BPM con variación gradual y posibilidad de anomalías"""
        if collar_id not in self.vital_signs:
            return None
        
        current = self.vital_signs[collar_id]['bpm']
        tipo_animal = self.vital_signs[collar_id]['tipo_animal']
        
        # Límites por especie
        limits = {
            'OVINO': (50, 120),
            'BOVINO': (40, 100),
            'EQUINO': (25, 60)
        }
        min_bpm, max_bpm = limits.get(tipo_animal, (40, 120))
        
        # Variación gradual
        delta = random.randint(-max_variation, max_variation)
        
        # Tendencia a volver al rango normal
        normal_ranges = {
            'OVINO': 80,
            'BOVINO': 70,
            'EQUINO': 35
        }
        target = normal_ranges.get(tipo_animal, 70)
        
        # NUEVO: Posibilidad aleatoria de generar anomalía (para variar alertas)
        if allow_anomalies and random.random() < 0.05:  # 5% de probabilidad
            # Decidir si sube o baja
            if random.random() < 0.6:  # 60% agitación, 40% bajo estímulo
                # Empujar hacia agitación (>120 BPM para ovino/bovino, >50 para equino)
                delta += 10
            else:
                # Empujar hacia bajo estímulo (<40 BPM)
                delta -= 10
        # Si está lejos del target, empujar hacia él
        elif abs(current - target) > 20:
            direction = 1 if current < target else -1
            delta += direction * 5
        
        new_bpm = current + delta
        new_bpm = max(min_bpm, min(max_bpm, new_bpm))
        new_bpm = int(new_bpm)
        
        self.vital_signs[collar_id]['bpm'] = new_bpm
        self.vital_signs[collar_id]['last_bpm_update'] = time.time()
        
        return new_bpm
    
    def get_current_vitals(self, collar_id):
        """Obtiene signos vitales actuales"""
        if collar_id not in self.vital_signs:
            return None, None
        
        return (
            self.vital_signs[collar_id]['temperatura'],
            self.vital_signs[collar_id]['bpm']
        )
    
    def can_send_alert(self, collar_id, alert_type, cooldown_seconds=60):
        """Verifica si se puede enviar una alerta (cooldown)"""
        if collar_id not in self.alert_cooldown:
            return True
        
        last_alert_time = self.alert_cooldown[collar_id].get(alert_type, 0)
        return (time.time() - last_alert_time) > cooldown_seconds
    
    def mark_alert_sent(self, collar_id, alert_type):
        """Marca que se envió una alerta"""
        if collar_id not in self.alert_cooldown:
            self.alert_cooldown[collar_id] = {}
        
        self.alert_cooldown[collar_id][alert_type] = time.time()


class Command(BaseCommand):
    help = 'Simulador CAMPORT V8.0 - Signos Vitales Realistas con Intervalos Independientes'

    def add_arguments(self, parser):
        # Intervalos independientes
        parser.add_argument('--interval-movement', type=int, default=3,
                          help='Intervalo de actualización de movimiento en segundos (default: 3)')
        parser.add_argument('--interval-temperature', type=int, default=5,
                          help='Intervalo de actualización de temperatura en segundos (default: 5)')
        parser.add_argument('--interval-bpm', type=int, default=2,
                          help='Intervalo de actualización de BPM en segundos (default: 2)')
        
        # Parámetros de movimiento
        parser.add_argument('--movement-range', type=float, default=0.0003,
                          help='Rango de movimiento por paso (default: 0.0003)')
        
        # Oveja negra
        parser.add_argument('--black-sheep', type=str, default=None,
                          help='ID del collar de la "oveja negra"')
        parser.add_argument('--escape-probability', type=float, default=0.15,
                          help='Probabilidad de escape de la oveja negra (default: 0.15)')
        
        # Alertas
        parser.add_argument(
            '--alert-cooldown-vitals',
            type=int,
            default=180,
            help='Segundos de cooldown entre alertas de signos vitales (temp/BPM) (default: 180)'
        )
        parser.add_argument(
            '--alert-cooldown-perimeter',
            type=int,
            default=60,
            help='Segundos de cooldown entre alertas de perímetro (default: 60)'
        )
    def handle(self, *args, **options):
        self.interval_movement = options['interval_movement']
        self.interval_temperature = options['interval_temperature']
        self.interval_bpm = options['interval_bpm']
        self.movement_range = options['movement_range']
        self.black_sheep_id = options['black_sheep']
        self.escape_probability = options['escape_probability']
        self.alert_cooldown_vitals = options['alert_cooldown_vitals']
        self.alert_cooldown_perimeter = options['alert_cooldown_perimeter']

        self.stdout.write(self.style.SUCCESS('=' * 95))
        self.stdout.write(self.style.SUCCESS('🏥 CAMPORT V8.0 - SIGNOS VITALES REALISTAS CON INTERVALOS INDEPENDIENTES 🏥'))
        self.stdout.write(self.style.SUCCESS('=' * 95))
        self.stdout.write(self.style.SUCCESS('\n📊 INTERVALOS INDEPENDIENTES:'))
        self.stdout.write(f'   🚶 Movimiento: {self.interval_movement}s')
        self.stdout.write(f'   🌡️  Temperatura: {self.interval_temperature}s')
        self.stdout.write(f'   ❤️  Frecuencia cardíaca (BPM): {self.interval_bpm}s')
        
        self.stdout.write(self.style.SUCCESS('\n⚕️  SISTEMA DE ALERTAS INTELIGENTES:'))
        self.stdout.write(f'   ✅ Solo para animales con geocerca asignada')
        self.stdout.write(f'   🔔 Cooldown alertas vitales (Temp/BPM): {self.alert_cooldown_vitals}s')
        self.stdout.write(f'   🔔 Cooldown alertas perímetro: {self.alert_cooldown_perimeter}s')
        self.stdout.write(f'   🌡️  Fiebre: >40°C | Hipotermia: <37.5°C')
        self.stdout.write(f'   ❤️  Agitación: >100 BPM | Bajo estímulo: <50 BPM')
        self.stdout.write(f'   🚨 Fuga: Fuera de perímetro')
        
        self.stdout.write(self.style.WARNING(f'\n🐑 Oveja negra: {self.black_sheep_id or "Selección automática"}'))
        self.stdout.write(self.style.SUCCESS('=' * 95 + '\n'))

        try:
            asyncio.run(self.run_simulation())
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⏹️  Simulación detenida'))
            self.stdout.write(self.style.SUCCESS('Gracias por usar CAMPORT V8.0\n'))

    async def run_simulation(self):
        """Ejecuta simulación con múltiples tasks asíncronos"""
        uri = 'ws://localhost:8000/ws/telemetria/'
        
        # Gestor de signos vitales
        self.vitals_manager = VitalSignsManager()
        
        # Estado compartido
        self.animal_positions = {}  # {collar_id: {'lat': X, 'lng': Y}}
        self.black_sheep = None
        self.black_sheep_escaped = False
        self.geofence_coords_cache = {}
        
        try:
            async with websockets.connect(uri) as websocket:
                self.websocket = websocket
                self.stdout.write(self.style.SUCCESS('✓ Conectado a WebSocket\n'))
                
                # Inicializar datos
                await self.initialize_simulation()
                
                # Crear tasks independientes
                tasks = [
                    asyncio.create_task(self.movement_loop(), name='movement'),
                    asyncio.create_task(self.temperature_loop(), name='temperature'),
                    asyncio.create_task(self.bpm_loop(), name='bpm'),
                    asyncio.create_task(self.stats_loop(), name='stats')
                ]
                
                # Ejecutar todos los tasks
                await asyncio.gather(*tasks)
                
        except websockets.exceptions.WebSocketException as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error WebSocket: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

    async def initialize_simulation(self):
        """Inicializa estado de la simulación"""
        # Obtener animales
        animales_data = await self.get_animals_with_geofences()
        
        # Inicializar signos vitales y posiciones
        for animal_data in animales_data:
            collar_id = animal_data['collar_id']
            tipo_animal = animal_data['tipo_animal']
            
            # Inicializar signos vitales
            self.vitals_manager.initialize_animal(collar_id, tipo_animal)
            
            # Inicializar posición
            if animal_data['geocerca']:
                geo_data = animal_data['geocerca']
                coords = [(c['lng'], c['lat']) for c in geo_data['coordenadas']]
                polygon = Polygon(coords)
                centroid = polygon.centroid
                
                # Posición inicial
                current_pos = await self.get_last_position(collar_id)
                if current_pos:
                    lat, lng = current_pos['latitud'], current_pos['longitud']
                    # Verificar si está dentro
                    if not polygon.contains(Point(lng, lat)):
                        lat, lng = centroid.y, centroid.x
                else:
                    lat, lng = centroid.y, centroid.x
                
                self.animal_positions[collar_id] = {'lat': lat, 'lng': lng}
        
        # Inicializar oveja negra
        self.black_sheep = await self.initialize_black_sheep(self.black_sheep_id)
        if self.black_sheep:
            self.stdout.write(
                self.style.WARNING(f'🐑 OVEJA NEGRA: {self.black_sheep["display_id"]}\n')
            )

    async def movement_loop(self):
        """Loop independiente para actualización de movimiento"""
        cycle = 0
        while True:
            cycle += 1
            try:
                animales_data = await self.get_animals_with_geofences()
                
                for animal_data in animales_data:
                    collar_id = animal_data['collar_id']
                    
                    if collar_id not in self.animal_positions:
                        continue
                    
                    # Obtener geocerca
                    if not animal_data['geocerca']:
                        continue
                    
                    geo_data = animal_data['geocerca']
                    coords = [(c['lng'], c['lat']) for c in geo_data['coordenadas']]
                    polygon = Polygon(coords)
                    centroid = polygon.centroid
                    
                    # Posición actual
                    lat = self.animal_positions[collar_id]['lat']
                    lng = self.animal_positions[collar_id]['lng']
                    
                    # Verificar si está dentro
                    if not polygon.contains(Point(lng, lat)):
                        # Reposicionar
                        lat, lng = centroid.y, centroid.x
                    else:
                        # Movimiento normal
                        is_black_sheep = (self.black_sheep and collar_id == self.black_sheep['collar_id'])
                        
                        if is_black_sheep and not self.black_sheep_escaped:
                            if random.random() < self.escape_probability:
                                # Escape
                                lat, lng = self.escape_movement(lat, lng, polygon, centroid, self.movement_range)
                                self.black_sheep_escaped = True
                            else:
                                lat, lng = self.random_walk_movement(lat, lng, polygon, self.movement_range)
                        elif is_black_sheep and self.black_sheep_escaped:
                            lat, lng = self.continue_escape(lat, lng, polygon, centroid, self.movement_range)
                            if random.random() < 0.05:
                                self.black_sheep_escaped = False
                                lat, lng = centroid.y, centroid.x
                        else:
                            lat, lng = self.random_walk_movement(lat, lng, polygon, self.movement_range)
                    
                    # Actualizar posición
                    self.animal_positions[collar_id] = {'lat': lat, 'lng': lng}
                
                await asyncio.sleep(self.interval_movement)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error en movement_loop: {e}'))
                await asyncio.sleep(self.interval_movement)

    async def temperature_loop(self):
        """Loop independiente para actualización de temperatura"""
        await asyncio.sleep(1)  # Offset inicial
        
        while True:
            try:
                animales_data = await self.get_animals_with_geofences()
                
                for animal_data in animales_data:
                    collar_id = animal_data['collar_id']
                    display_id = animal_data['display_id']
                    
                    # Actualizar temperatura
                    temp = self.vitals_manager.update_temperature(collar_id)
                    
                    if temp and animal_data['geocerca']:  # Solo alertas si tiene geocerca
                        # Verificar alertas de temperatura
                        await self.check_temperature_alert(collar_id, display_id, temp, animal_data)
                    
                    # Enviar telemetría
                    if collar_id in self.animal_positions:
                        pos = self.animal_positions[collar_id]
                        temp, bpm = self.vitals_manager.get_current_vitals(collar_id)
                        
                        if temp and bpm:
                            await self.send_telemetry(collar_id, pos['lat'], pos['lng'], temp, bpm)
                
                await asyncio.sleep(self.interval_temperature)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error en temperature_loop: {e}'))
                await asyncio.sleep(self.interval_temperature)

    async def bpm_loop(self):
        """Loop independiente para actualización de BPM"""
        await asyncio.sleep(0.5)  # Offset inicial
        
        while True:
            try:
                animales_data = await self.get_animals_with_geofences()
                
                for animal_data in animales_data:
                    collar_id = animal_data['collar_id']
                    display_id = animal_data['display_id']
                    
                    # Actualizar BPM
                    bpm = self.vitals_manager.update_bpm(collar_id)
                    
                    if bpm and animal_data['geocerca']:  # Solo alertas si tiene geocerca
                        # Verificar alertas de BPM
                        await self.check_bpm_alert(collar_id, display_id, bpm, animal_data)
                
                await asyncio.sleep(self.interval_bpm)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error en bpm_loop: {e}'))
                await asyncio.sleep(self.interval_bpm)

    async def stats_loop(self):
        """Loop para mostrar estadísticas periódicas"""
        await asyncio.sleep(2)
        cycle = 0
        
        while True:
            cycle += 1
            try:
                animales_data = await self.get_animals_with_geofences()
                
                self.stdout.write(self.style.SUCCESS(f'\n━━━ ESTADÍSTICAS CICLO #{cycle} ━━━'))
                
                for animal_data in animales_data:
                    collar_id = animal_data['collar_id']
                    display_id = animal_data['display_id']
                    
                    if collar_id not in self.animal_positions:
                        continue
                    
                    temp, bpm = self.vitals_manager.get_current_vitals(collar_id)
                    pos = self.animal_positions[collar_id]
                    
                    # Estado
                    has_geo = '✅' if animal_data['geocerca'] else '❌'
                    is_black = '🐑' if self.black_sheep and collar_id == self.black_sheep['collar_id'] else ''
                    
                    self.stdout.write(
                        f'  {has_geo} {display_id}{is_black}: '
                        f'Temp={temp:.1f}°C | BPM={bpm} | '
                        f'Pos=({pos["lat"]:.5f}, {pos["lng"]:.5f})'
                    )
                
                await asyncio.sleep(10)  # Estadísticas cada 10s
                
            except Exception as e:
                await asyncio.sleep(10)

    async def send_telemetry(self, collar_id, lat, lng, temp, bpm):
        """Envía telemetría al WebSocket"""
        try:
            telemetria = {
                'collar_id': collar_id,
                'latitud': round(lat, 6),
                'longitud': round(lng, 6),
                'temperatura_corporal': round(temp, 1),
                'frecuencia_cardiaca': int(bpm)
            }
            
            await self.websocket.send(json.dumps(telemetria))
            
            # Leer respuesta (no bloqueante)
            try:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=0.1)
            except asyncio.TimeoutError:
                pass
                
        except Exception as e:
            pass  # Silenciar errores de envío

    async def check_temperature_alert(self, collar_id, display_id, temp, animal_data):
        """Verifica y envía alertas de temperatura"""
        # Rangos de alerta por especie
        tipo_animal = animal_data['tipo_animal']
        
        alert_ranges = {
            'OVINO': {'fiebre': 40.0, 'hipotermia': 37.5},
            'BOVINO': {'fiebre': 39.5, 'hipotermia': 37.0},
            'EQUINO': {'fiebre': 39.0, 'hipotermia': 36.5}
        }
        
        ranges = alert_ranges.get(tipo_animal, alert_ranges['OVINO'])
        
        if temp > ranges['fiebre']:
            if self.vitals_manager.can_send_alert(collar_id, 'temp', self.alert_cooldown_vitals):
                self.stdout.write(
                    self.style.ERROR(f'  🌡️🔥 ALERTA: {display_id} - FIEBRE: {temp}°C')
                )
                self.vitals_manager.mark_alert_sent(collar_id, 'temp')
                
        elif temp < ranges['hipotermia']:
            if self.vitals_manager.can_send_alert(collar_id, 'temp', self.alert_cooldown_vitals):
                self.stdout.write(
                    self.style.ERROR(f'  🌡️❄️  ALERTA: {display_id} - HIPOTERMIA: {temp}°C')
                )
                self.vitals_manager.mark_alert_sent(collar_id, 'temp')

    async def check_bpm_alert(self, collar_id, display_id, bpm, animal_data):
        """Verifica y envía alertas de BPM"""
        # Rangos de alerta por especie
        tipo_animal = animal_data['tipo_animal']
        
        alert_ranges = {
            'OVINO': {'agitacion': 100, 'bajo': 50},
            'BOVINO': {'agitacion': 90, 'bajo': 45},
            'EQUINO': {'agitacion': 55, 'bajo': 25}
        }
        
        ranges = alert_ranges.get(tipo_animal, alert_ranges['OVINO'])
        
        if bpm > ranges['agitacion']:
            if self.vitals_manager.can_send_alert(collar_id, 'bpm', self.alert_cooldown_vitals):
                self.stdout.write(
                    self.style.ERROR(f'  ❤️⚡ ALERTA: {display_id} - AGITACIÓN: {bpm} BPM')
                )
                self.vitals_manager.mark_alert_sent(collar_id, 'bpm')
                
        elif bpm < ranges['bajo']:
            if self.vitals_manager.can_send_alert(collar_id, 'bpm', self.alert_cooldown_vitals):
                self.stdout.write(
                    self.style.ERROR(f'  ❤️💤 ALERTA: {display_id} - BAJO ESTÍMULO: {bpm} BPM')
                )
                self.vitals_manager.mark_alert_sent(collar_id, 'bpm')

    # =============== MÉTODOS DE SOPORTE ===============
    
    @sync_to_async
    def get_animals_with_geofences(self):
        """Obtiene todos los animales con sus geocercas"""
        animales = Animal.objects.select_related('geocerca').all()
        result = []
        
        for animal in animales:
            data = {
                'collar_id': animal.collar_id,
                'display_id': animal.display_id,
                'tipo_animal': animal.tipo_animal,
                'geocerca': None
            }
            
            if animal.geocerca and animal.geocerca.activa:
                data['geocerca'] = {
                    'id': animal.geocerca.id,
                    'nombre': animal.geocerca.nombre,
                    'coordenadas': animal.geocerca.coordenadas
                }
            
            result.append(data)
        
        return result

    @sync_to_async
    def get_last_position(self, collar_id):
        """Obtiene la última posición registrada"""
        telemetria = Telemetria.objects.filter(
            animal__collar_id=collar_id
        ).order_by('-timestamp').first()
        
        if telemetria:
            return {
                'latitud': telemetria.latitud,
                'longitud': telemetria.longitud
            }
        return None

    @sync_to_async
    def initialize_black_sheep(self, black_sheep_id):
        """Inicializa la oveja negra"""
        if black_sheep_id:
            try:
                animal = Animal.objects.get(collar_id=black_sheep_id)
                return {
                    'collar_id': animal.collar_id,
                    'display_id': animal.display_id,
                    'tipo_animal': animal.tipo_animal
                }
            except Animal.DoesNotExist:
                pass
        
        animales = list(Animal.objects.all())
        if animales:
            animal = random.choice(animales)
            return {
                'collar_id': animal.collar_id,
                'display_id': animal.display_id,
                'tipo_animal': animal.tipo_animal
            }
        return None

    def random_walk_movement(self, lat, lng, polygon, movement_range):
        """Random walk puro"""
        delta_lat = random.uniform(-movement_range, movement_range)
        delta_lng = random.uniform(-movement_range, movement_range)
        
        nueva_lat = lat + delta_lat
        nueva_lng = lng + delta_lng
        
        if polygon.contains(Point(nueva_lng, nueva_lat)):
            return nueva_lat, nueva_lng
        else:
            rebote_lat = lat - delta_lat * 0.5
            rebote_lng = lng - delta_lng * 0.5
            
            if polygon.contains(Point(rebote_lng, rebote_lat)):
                return rebote_lat, rebote_lng
            else:
                return lat, lng

    def escape_movement(self, lat, lng, polygon, centroid, movement_range):
        """Movimiento de escape"""
        vector_lat = lat - centroid.y
        vector_lng = lng - centroid.x
        
        if abs(vector_lat) < 0.00001 and abs(vector_lng) < 0.00001:
            vector_lat = random.choice([-1, 1]) * 0.0001
            vector_lng = random.choice([-1, 1]) * 0.0001
        
        magnitude = (vector_lat**2 + vector_lng**2) ** 0.5
        if magnitude > 0:
            vector_lat /= magnitude
            vector_lng /= magnitude
        
        escape_factor = random.uniform(3, 5)
        return lat + vector_lat * movement_range * escape_factor, lng + vector_lng * movement_range * escape_factor

    def continue_escape(self, lat, lng, polygon, centroid, movement_range):
        """Continuar escape"""
        vector_lat = lat - centroid.y
        vector_lng = lng - centroid.x
        
        magnitude = (vector_lat**2 + vector_lng**2) ** 0.5
        if magnitude > 0:
            vector_lat /= magnitude
            vector_lng /= magnitude
        
        escape_factor = random.uniform(1.5, 2.5)
        delta_lat = vector_lat * movement_range * escape_factor + random.uniform(-movement_range, movement_range) * 0.5
        delta_lng = vector_lng * movement_range * escape_factor + random.uniform(-movement_range, movement_range) * 0.5
        
        return lat + delta_lat, lng + delta_lng
