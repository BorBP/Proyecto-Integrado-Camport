"""
Management Command: simulate_collars_v7
Versión 7.0 - CAMPORT - RANDOM WALK NATURAL Y OVEJA NEGRA

REQUERIMIENTOS V7.0:
==================
1. RANDOM WALK PURO - Sin tendencia al centro
2. OVEJA NEGRA - Un animal específico con tendencia a escapar
3. ABSTRACCIÓN TOTAL - Sin hardcodeo de ubicaciones
4. ADAPTABILIDAD - Recálculo automático al cambiar geocerca O sus coordenadas
5. PLACEHOLDER - Animales sin geocerca en primera geocerca disponible

NUEVA FUNCIONALIDAD:
===================
- Detección de cambios en coordenadas de geocercas
- Reposicionamiento automático cuando geocerca se mueve
- Reposicionamiento automático cuando animal cambia de geocerca

Autor: CAMPORT Team - Refactorización V7.0
Fecha: 2025
"""

import asyncio
import websockets
import json
import random
import time
import hashlib
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from shapely.geometry import Point, Polygon
from api.models import Animal, Telemetria, Geocerca


class Command(BaseCommand):
    help = 'Simulador CAMPORT V7.0 - Random Walk Natural + Oveja Negra'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=20,
            help='Intervalo de actualización en segundos (default: 20)'
        )
        parser.add_argument(
            '--movement-range',
            type=float,
            default=0.0003,
            help='Rango de movimiento por paso (default: 0.0003 grados)'
        )
        parser.add_argument(
            '--black-sheep',
            type=str,
            default=None,
            help='ID del collar de la "oveja negra" (default: selección aleatoria)'
        )
        parser.add_argument(
            '--escape-probability',
            type=float,
            default=0.15,
            help='Probabilidad de escape de la oveja negra por ciclo (default: 0.15 = 15%%)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        movement_range = options['movement_range']
        black_sheep_id = options['black_sheep']
        escape_probability = options['escape_probability']

        self.stdout.write(self.style.SUCCESS('=' * 90))
        self.stdout.write(self.style.SUCCESS('🐑 CAMPORT V7.0 - RANDOM WALK NATURAL + OVEJA NEGRA 🐑'))
        self.stdout.write(self.style.SUCCESS('=' * 90))
        self.stdout.write(f'⏱️  Intervalo: {interval} segundos')
        self.stdout.write(f'🎲 Rango movimiento: {movement_range} grados (Random Walk puro)')
        self.stdout.write(f'🚫 SIN gravedad de centroide - Movimiento 100% errático')
        self.stdout.write(self.style.WARNING(f'🐑 Oveja negra: {black_sheep_id or "Selección automática"}'))
        self.stdout.write(self.style.WARNING(f'🏃 Probabilidad de escape: {escape_probability * 100:.1f}%'))
        self.stdout.write(f'🗺️  Abstracción completa - Compatible con cualquier geocerca')
        self.stdout.write(f'🔄 Adaptabilidad dinámica a cambios de geocerca Y coordenadas')
        self.stdout.write(self.style.SUCCESS('=' * 90 + '\n'))

        try:
            asyncio.run(self.run_simulation(
                interval, movement_range, black_sheep_id, escape_probability
            ))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⏹️  Simulación detenida por el usuario'))
            self.stdout.write(self.style.SUCCESS('Gracias por usar CAMPORT V7.0\n'))

    async def run_simulation(self, interval, movement_range, black_sheep_id, escape_probability):
        """Ejecuta simulación continua con Random Walk natural"""
        uri = 'ws://localhost:8000/ws/telemetria/'

        # Estado de la oveja negra
        black_sheep = None
        black_sheep_escaped = False
        
        # Cache de signos vitales por animal
        vital_signs_cache = {}
        
        # Cache de coordenadas de geocercas (para detectar cambios)
        self.geofence_coords_cache = {}

        cycle_count = 0

        try:
            async with websockets.connect(uri) as websocket:
                self.stdout.write(self.style.SUCCESS('✓ Conectado a WebSocket\n'))

                # Inicializar oveja negra
                black_sheep = await self.initialize_black_sheep(black_sheep_id)
                if black_sheep:
                    self.stdout.write(
                        self.style.WARNING(f'🐑 OVEJA NEGRA designada: {black_sheep["collar_id"]} ({black_sheep["tipo_animal"]})\n')
                    )

                while True:
                    cycle_count += 1
                    start_time = time.time()

                    self.stdout.write(self.style.SUCCESS(f'\n━━━ CICLO #{cycle_count} ━━━'))

                    # Obtener todos los animales y geocercas
                    animales_data = await self.get_animals_with_geofences()
                    placeholder_geofence = await self.get_placeholder_geofence()

                    if not animales_data and not placeholder_geofence:
                        self.stdout.write(self.style.WARNING('⚠️  No hay animales ni geocercas en el sistema'))
                        await asyncio.sleep(interval)
                        continue

                    # Contadores
                    exitosos = 0
                    fuera_limites = 0
                    sin_geocerca = 0
                    errores = 0
                    reposicionados = 0

                    # Procesar cada animal
                    for animal_data in animales_data:
                        collar_id = animal_data['collar_id']
                        tipo_animal = animal_data['tipo_animal']
                        geocerca_asignada = animal_data['geocerca']
                        display_id = animal_data['display_id']

                        try:
                            # Determinar geocerca efectiva
                            if geocerca_asignada:
                                geofence_data = geocerca_asignada
                                is_placeholder = False
                            elif placeholder_geofence:
                                geofence_data = placeholder_geofence
                                is_placeholder = True
                            else:
                                sin_geocerca += 1
                                self.stdout.write(
                                    self.style.WARNING(f'⚠️  {display_id}: Sin geocerca y sin placeholder')
                                )
                                continue

                            # Preparar geometría
                            polygon_coords = [(c['lng'], c['lat']) for c in geofence_data['coordenadas']]
                            polygon = Polygon(polygon_coords)
                            centroid = polygon.centroid
                            
                            # Calcular hash de coordenadas para detectar cambios
                            coords_hash = self.calculate_coords_hash(geofence_data['coordenadas'])

                            # Obtener posición actual
                            current_position = await self.get_last_position(collar_id)
                            
                            needs_repositioning = False
                            reposition_reason = ""
                            
                            if current_position:
                                lat_actual = current_position['latitud']
                                lng_actual = current_position['longitud']
                                
                                # Verificar si cambió la geocerca O sus coordenadas
                                change_info = await self.geofence_changed(collar_id, geofence_data['id'], coords_hash)
                                
                                # También verificar si está FUERA de su geocerca actual
                                punto_check = Point(lng_actual, lat_actual)
                                esta_dentro = polygon.contains(punto_check)
                                
                                if change_info['changed'] or not esta_dentro:
                                    needs_repositioning = True
                                    if change_info['changed']:
                                        reposition_reason = change_info['reason']
                                    else:
                                        reposition_reason = 'Fuera de geocerca asignada'
                                    
                                    self.stdout.write(
                                        self.style.SUCCESS(f'🔄 {display_id}: {reposition_reason} - Reposicionando...')
                                    )
                                    lat_actual, lng_actual = self.get_safe_position_in_geofence(polygon, centroid)
                                    reposicionados += 1
                                    
                                    # Actualizar cache
                                    self.geofence_coords_cache[geofence_data['id']] = coords_hash
                            else:
                                # Primera vez - posicionar en geocerca
                                lat_actual, lng_actual = self.get_safe_position_in_geofence(polygon, centroid)
                                needs_repositioning = True
                                reposition_reason = "Primera posición"
                                # Inicializar cache
                                self.geofence_coords_cache[geofence_data['id']] = coords_hash

                            # Determinar si es la oveja negra
                            is_black_sheep = (black_sheep and collar_id == black_sheep['collar_id'])

                            # ALGORITMO DE MOVIMIENTO (solo si no se reposicionó)
                            if not needs_repositioning:
                                if is_black_sheep and not black_sheep_escaped:
                                    # Oveja negra: posible intento de escape
                                    if random.random() < escape_probability:
                                        # INTENTO DE ESCAPE
                                        lat_nueva, lng_nueva = self.escape_movement(
                                            lat_actual, lng_actual, polygon, centroid, movement_range
                                        )
                                        black_sheep_escaped = True
                                        self.stdout.write(
                                            self.style.ERROR(f'🏃 {display_id} (OVEJA NEGRA) está intentando ESCAPAR!')
                                        )
                                    else:
                                        # Oveja negra moviéndose normal
                                        lat_nueva, lng_nueva = self.random_walk_movement(
                                            lat_actual, lng_actual, polygon, movement_range
                                        )
                                elif is_black_sheep and black_sheep_escaped:
                                    # Oveja negra escapada: continuar alejándose
                                    lat_nueva, lng_nueva = self.continue_escape(
                                        lat_actual, lng_actual, polygon, centroid, movement_range
                                    )
                                    
                                    # Pequeña probabilidad de retorno
                                    if random.random() < 0.05:  # 5% de retorno por ciclo
                                        black_sheep_escaped = False
                                        lat_nueva, lng_nueva = self.get_safe_position_in_geofence(polygon, centroid)
                                        self.stdout.write(
                                            self.style.SUCCESS(f'🔙 {display_id} (OVEJA NEGRA) ha REGRESADO')
                                        )
                                else:
                                    # Animal normal: Random Walk puro
                                    lat_nueva, lng_nueva = self.random_walk_movement(
                                        lat_actual, lng_actual, polygon, movement_range
                                    )
                            else:
                                # Mantener posición reposicionada
                                lat_nueva, lng_nueva = lat_actual, lng_actual

                            # Generar/actualizar signos vitales
                            if collar_id not in vital_signs_cache:
                                temp, fc = self.get_base_vital_signs(tipo_animal)
                                vital_signs_cache[collar_id] = {'temperatura': temp, 'frecuencia': fc}
                            else:
                                temp = self.vary_vital_sign(
                                    vital_signs_cache[collar_id]['temperatura'], 
                                    0.2, 37.0, 41.0
                                )
                                fc = self.vary_vital_sign(
                                    vital_signs_cache[collar_id]['frecuencia'],
                                    5, 30, 120
                                )
                                vital_signs_cache[collar_id] = {'temperatura': temp, 'frecuencia': fc}

                            # Preparar datos de telemetría
                            telemetria = {
                                'collar_id': collar_id,
                                'latitud': round(lat_nueva, 6),
                                'longitud': round(lng_nueva, 6),
                                'temperatura_corporal': round(temp, 1),
                                'frecuencia_cardiaca': int(fc)
                            }

                            # Enviar telemetría
                            await websocket.send(json.dumps(telemetria))

                            # Verificar si está dentro o fuera
                            punto_actual = Point(lng_nueva, lat_nueva)
                            dentro = polygon.contains(punto_actual)

                            if dentro or is_placeholder:
                                exitosos += 1
                                status_emoji = '📍' if not is_placeholder else '📌'
                                status_text = 'OK' if not is_placeholder else 'PLACEHOLDER'
                            else:
                                fuera_limites += 1
                                status_emoji = '⚠️'
                                status_text = 'FUERA'

                            # Mostrar info
                            sheep_marker = ' 🐑⚫' if is_black_sheep and black_sheep_escaped else ' 🐑' if is_black_sheep else ''
                            reposition_marker = ' 🔄' if needs_repositioning else ''
                            self.stdout.write(
                                f'  {status_emoji} {display_id}{sheep_marker}{reposition_marker}: '
                                f'{status_text} | Temp: {temp:.1f}°C | FC: {int(fc)} lpm | '
                                f'Geocerca: {geofence_data["nombre"]}'
                            )

                            # Leer respuesta
                            try:
                                response = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                                data = json.loads(response)
                                if 'alertas' in data and data['alertas']:
                                    self.stdout.write(
                                        self.style.WARNING(f'    ⚠️  ALERTAS: {len(data["alertas"])} generadas')
                                    )
                            except asyncio.TimeoutError:
                                pass

                            # Pequeña pausa entre animales
                            await asyncio.sleep(0.3)

                        except Exception as e:
                            errores += 1
                            self.stdout.write(
                                self.style.ERROR(f'  ✗ {display_id}: Error - {str(e)}')
                            )
                            import traceback
                            self.stdout.write(self.style.ERROR(traceback.format_exc()))

                    # Resumen del ciclo
                    self.stdout.write(self.style.SUCCESS(f'\n�� RESUMEN:'))
                    self.stdout.write(f'   ✓ Exitosos: {exitosos}')
                    if reposicionados > 0:
                        self.stdout.write(self.style.SUCCESS(f'   🔄 Reposicionados: {reposicionados}'))
                    if fuera_limites > 0:
                        self.stdout.write(self.style.WARNING(f'   ⚠️  Fuera de límites: {fuera_limites}'))
                    if sin_geocerca > 0:
                        self.stdout.write(self.style.WARNING(f'   📌 Sin geocerca: {sin_geocerca}'))
                    if errores > 0:
                        self.stdout.write(self.style.ERROR(f'   ✗ Errores: {errores}'))

                    # Esperar hasta completar intervalo
                    elapsed = time.time() - start_time
                    wait_time = max(0, interval - elapsed)
                    if wait_time > 0:
                        self.stdout.write(f'\n⏳ Esperando {wait_time:.1f} segundos...')
                        await asyncio.sleep(wait_time)

        except websockets.exceptions.WebSocketException as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error WebSocket: {e}'))
            self.stdout.write(self.style.WARNING('Verifica que el servidor Django esté ejecutándose'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Error inesperado: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

    def calculate_coords_hash(self, coordenadas):
        """Calcula hash de las coordenadas para detectar cambios"""
        coords_str = json.dumps(coordenadas, sort_keys=True)
        return hashlib.md5(coords_str.encode()).hexdigest()

    @sync_to_async
    def initialize_black_sheep(self, black_sheep_id):
        """Inicializa la oveja negra (designada o aleatoria)"""
        if black_sheep_id:
            try:
                animal = Animal.objects.get(collar_id=black_sheep_id)
                return {
                    'collar_id': animal.collar_id,
                    'tipo_animal': animal.tipo_animal,
                    'display_id': animal.display_id
                }
            except Animal.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  No se encontró animal con ID {black_sheep_id}')
                )
        
        # Selección aleatoria
        animales = list(Animal.objects.all())
        if animales:
            animal = random.choice(animales)
            return {
                'collar_id': animal.collar_id,
                'tipo_animal': animal.tipo_animal,
                'display_id': animal.display_id
            }
        
        return None

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
    def get_placeholder_geofence(self):
        """Obtiene la primera geocerca disponible como placeholder"""
        geocerca = Geocerca.objects.filter(activa=True).first()
        if geocerca:
            return {
                'id': geocerca.id,
                'nombre': f'{geocerca.nombre} (Placeholder)',
                'coordenadas': geocerca.coordenadas
            }
        return None

    @sync_to_async
    def get_last_position(self, collar_id):
        """Obtiene la última posición registrada de un animal"""
        telemetria = Telemetria.objects.filter(
            animal__collar_id=collar_id
        ).order_by('-timestamp').first()
        
        if telemetria:
            return {
                'latitud': telemetria.latitud,
                'longitud': telemetria.longitud,
                'geocerca_id': telemetria.animal.geocerca_id if telemetria.animal.geocerca else None
            }
        return None

    @sync_to_async
    def geofence_changed(self, collar_id, current_geofence_id, current_coords_hash):
        """
        Verifica si la geocerca del animal cambió O si las coordenadas de la geocerca cambiaron
        Retorna dict con 'changed' (bool) y 'reason' (str)
        """
        # Obtener el animal actualizado de la BD (no de telemetría antigua)
        try:
            animal = Animal.objects.select_related('geocerca').get(collar_id=collar_id)
        except Animal.DoesNotExist:
            return {'changed': False, 'reason': ''}
        
        # Obtener última telemetría
        last_pos = Telemetria.objects.filter(
            animal__collar_id=collar_id
        ).order_by('-timestamp').first()
        
        if not last_pos:
            return {'changed': True, 'reason': 'Primera posición'}
        
        # Verificar cambio de geocerca (animal reasignado)
        # Comparar con el animal ACTUAL de la BD, no con la telemetría antigua
        actual_geofence_id = animal.geocerca_id if animal.geocerca else None
        
        if actual_geofence_id != current_geofence_id:
            return {'changed': True, 'reason': 'Geocerca reasignada'}
        
        # Verificar cambio en coordenadas de la geocerca (geocerca movida)
        if hasattr(self, 'geofence_coords_cache'):
            cached_hash = self.geofence_coords_cache.get(current_geofence_id)
            if cached_hash and cached_hash != current_coords_hash:
                return {'changed': True, 'reason': 'Coordenadas de geocerca modificadas'}
        
        return {'changed': False, 'reason': ''}

    def get_safe_position_in_geofence(self, polygon, centroid):
        """
        Obtiene una posición segura dentro de la geocerca.
        Usado para inicialización o cuando un animal cambia de geocerca.
        """
        # Posicionar cerca del centroide pero con algo de variación
        lat = centroid.y + random.uniform(-0.0001, 0.0001)
        lng = centroid.x + random.uniform(-0.0001, 0.0001)
        
        # Verificar que esté dentro
        punto = Point(lng, lat)
        if polygon.contains(punto):
            return lat, lng
        
        # Si no está dentro, usar directamente el centroide
        return centroid.y, centroid.x

    def random_walk_movement(self, lat, lng, polygon, movement_range):
        """RANDOM WALK PURO - Sin tendencia al centro"""
        delta_lat = random.uniform(-movement_range, movement_range)
        delta_lng = random.uniform(-movement_range, movement_range)
        
        nueva_lat = lat + delta_lat
        nueva_lng = lng + delta_lng
        
        punto_nuevo = Point(nueva_lng, nueva_lat)
        
        if polygon.contains(punto_nuevo):
            return nueva_lat, nueva_lng
        else:
            rebote_lat = lat - delta_lat * 0.5
            rebote_lng = lng - delta_lng * 0.5
            
            punto_rebote = Point(rebote_lng, rebote_lat)
            
            if polygon.contains(punto_rebote):
                return rebote_lat, rebote_lng
            else:
                return lat, lng

    def escape_movement(self, lat, lng, polygon, centroid, movement_range):
        """Movimiento de ESCAPE para la oveja negra"""
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
        delta_lat = vector_lat * movement_range * escape_factor
        delta_lng = vector_lng * movement_range * escape_factor
        
        nueva_lat = lat + delta_lat
        nueva_lng = lng + delta_lng
        
        return nueva_lat, nueva_lng

    def continue_escape(self, lat, lng, polygon, centroid, movement_range):
        """Continuar alejándose después de escapar"""
        vector_lat = lat - centroid.y
        vector_lng = lng - centroid.x
        
        magnitude = (vector_lat**2 + vector_lng**2) ** 0.5
        if magnitude > 0:
            vector_lat /= magnitude
            vector_lng /= magnitude
        
        escape_factor = random.uniform(1.5, 2.5)
        delta_lat = vector_lat * movement_range * escape_factor
        delta_lng = vector_lng * movement_range * escape_factor
        
        delta_lat += random.uniform(-movement_range, movement_range) * 0.5
        delta_lng += random.uniform(-movement_range, movement_range) * 0.5
        
        nueva_lat = lat + delta_lat
        nueva_lng = lng + delta_lng
        
        return nueva_lat, nueva_lng

    def get_base_vital_signs(self, tipo_animal):
        """Retorna signos vitales base según tipo de animal"""
        vital_ranges = {
            'OVINO': {
                'temperatura': (38.5, 39.5),
                'frecuencia': (70, 90)
            },
            'BOVINO': {
                'temperatura': (38.0, 39.0),
                'frecuencia': (60, 80)
            },
            'EQUINO': {
                'temperatura': (37.5, 38.5),
                'frecuencia': (28, 40)
            }
        }
        
        ranges = vital_ranges.get(tipo_animal, vital_ranges['OVINO'])
        
        temp = round(random.uniform(*ranges['temperatura']), 1)
        fc = random.randint(*ranges['frecuencia'])
        
        return temp, fc

    def vary_vital_sign(self, current_value, variation, min_val, max_val):
        """Aplica variación natural a un signo vital"""
        if isinstance(current_value, int):
            delta = random.randint(-int(variation), int(variation))
            new_value = current_value + delta
        else:
            delta = random.uniform(-variation, variation)
            new_value = current_value + delta
        
        return max(min_val, min(max_val, new_value))
