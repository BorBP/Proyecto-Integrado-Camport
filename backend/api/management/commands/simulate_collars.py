"""
Management Command: simulate_collars
Versión 6.0 - CAMPORT - GRAVEDAD DE CENTROIDE

Características V6.0:
- Algoritmo de "Gravedad de Centroide" (Centroid Gravity)
- Movimiento proactivo hacia el centro de la geocerca
- Adaptación automática a cambios de límites de geocerca
- Migración natural del rebaño a nuevos centros

Características Heredadas (V5.0):
- Sistema de "Fuga y Retorno" Aleatorio
- Formato de temperatura con 1 decimal
- Ejecución inmediata del primer ciclo
- Simulación de REBAÑO COMPLETO
- Intervalo LENTO y REALISTA
- Adherencia DINÁMICA a geocercas
- Integración WebSocket

Autor: CAMPORT Team
Fecha: Noviembre 2025
"""

import asyncio
import websockets
import json
import random
import time
from django.core.management.base import BaseCommand
from asgiref.sync import sync_to_async
from shapely.geometry import Point, Polygon
from api.models import Animal, Telemetria, Geocerca


class Command(BaseCommand):
    help = 'Simulador CAMPORT V6.0 - Gravedad de Centroide y Migración Natural'

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
            default=0.0002,
            help='Rango de movimiento aleatorio (default: 0.0002 grados)'
        )
        parser.add_argument(
            '--escape-interval',
            type=int,
            default=60,
            help='Segundos entre fugas aleatorias (default: 60)'
        )
        parser.add_argument(
            '--return-interval',
            type=int,
            default=30,
            help='Segundos antes de que animal fugado regrese (default: 30)'
        )
        parser.add_argument(
            '--gravity-factor',
            type=float,
            default=0.2,
            help='Factor de atracción al centroide 0.0-1.0 (default: 0.2)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        movement_range = options['movement_range']
        escape_interval = options['escape_interval']
        return_interval = options['return_interval']
        gravity_factor = options['gravity_factor']

        self.stdout.write(self.style.SUCCESS('=' * 85))
        self.stdout.write(self.style.SUCCESS('🐄 CAMPORT V6.0 - GRAVEDAD DE CENTROIDE Y MIGRACIÓN NATURAL 🐄'))
        self.stdout.write(self.style.SUCCESS('=' * 85))
        self.stdout.write(f'⏱️  Intervalo: {interval} segundos')
        self.stdout.write(f'📏 Rango movimiento: {movement_range} grados')
        self.stdout.write(f'🔄 Consulta dinámica de geocercas en cada ciclo')
        self.stdout.write(self.style.WARNING(f'🚨 Fugas aleatorias: cada {escape_interval} segundos'))
        self.stdout.write(self.style.WARNING(f'🏠 Retorno automático: después de {return_interval} segundos'))
        self.stdout.write(self.style.SUCCESS(f'🧲 Gravedad de centroide: {gravity_factor * 100:.0f}% atracción'))
        self.stdout.write(f'🎯 Temperatura: formato con 1 decimal (realista)')
        self.stdout.write(self.style.SUCCESS('=' * 85 + '\n'))

        try:
            asyncio.run(self.run_simulation(
                interval, movement_range, escape_interval, return_interval, gravity_factor
            ))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⏹️  Simulación detenida por el usuario'))
            self.stdout.write(self.style.SUCCESS('Gracias por usar CAMPORT V6.0\n'))

    async def run_simulation(self, interval, movement_range, escape_interval, 
                            return_interval, gravity_factor):
        """Ejecuta simulación continua con gravedad de centroide"""
        uri = 'ws://localhost:8000/ws/telemetria/'
        
        # Variables de Estado para Fugas (V5)
        last_escape_time = time.time()
        escaped_animal_id = None
        escape_return_time = None
        escaped_animal_name = None
        
        cycle_count = 0
        
        try:
            async with websockets.connect(uri) as websocket:
                self.stdout.write(self.style.SUCCESS('✓ Conectado a WebSocket\n'))
                
                while True:
                    cycle_count += 1
                    current_time = time.time()
                    
                    # --- GESTIÓN DE EVENTOS DE FUGA (V5) ---
                    
                    # Comprobar Retorno
                    if escaped_animal_id is not None and current_time >= escape_return_time:
                        self.stdout.write(
                            self.style.SUCCESS(f'\n🏠 Animal {escaped_animal_name} ha REGRESADO a su geocerca')
                        )
                        escaped_animal_id = None
                        escape_return_time = None
                        escaped_animal_name = None
                    
                    # Obtener animales
                    animales = await sync_to_async(list)(
                        Animal.objects.filter(geocerca__isnull=False)
                                      .select_related('geocerca')
                                      .order_by('display_id')
                    )
                    
                    # Comprobar Fuga
                    if escaped_animal_id is None and current_time - last_escape_time >= escape_interval:
                        if len(animales) > 0:
                            random_animal = random.choice(animales)
                            escaped_animal_id = random_animal.collar_id
                            escaped_animal_name = await sync_to_async(
                                lambda: random_animal.display_id or random_animal.collar_id
                            )()
                            escape_return_time = current_time + return_interval
                            last_escape_time = current_time
                            
                            self.stdout.write(
                                self.style.ERROR(f'\n🚨 FUGA INICIADA: {escaped_animal_name} escapando de su geocerca!')
                            )
                            self.stdout.write(
                                self.style.WARNING(f'   Retornará automáticamente en {return_interval} segundos...\n')
                            )
                    
                    # --- CICLO DE SIMULACIÓN ---
                    self.stdout.write(self.style.SUCCESS(f'\n{"="*85}'))
                    self.stdout.write(self.style.SUCCESS(f'📡 CICLO #{cycle_count} - Consultando estado EN VIVO del rebaño...'))
                    
                    if escaped_animal_id:
                        self.stdout.write(
                            self.style.ERROR(f'⚠️  Estado de Fuga: {escaped_animal_name} está FUERA de perímetro')
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'{"="*85}'))
                    
                    await self.simulate_herd_cycle(
                        websocket, movement_range, cycle_count, 
                        escaped_animal_id, animales, gravity_factor
                    )
                    
                    # Sleep al FINAL del bucle
                    self.stdout.write(
                        self.style.WARNING(f'\n⏳ Ciclo #{cycle_count} completado. Esperando {interval} segundos...')
                    )
                    self.stdout.write(
                        self.style.WARNING(f'   (Movimiento lento y realista del ganado con gravedad de centroide)\n')
                    )
                    await asyncio.sleep(interval)
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error WebSocket: {e}'))
            self.stdout.write(self.style.WARNING('💡 Asegúrate de que el backend esté corriendo'))

    async def simulate_herd_cycle(self, websocket, movement_range, cycle_count, 
                                   escaped_animal_id, animales, gravity_factor):
        """Simula TODO el rebaño con gravedad de centroide"""
        
        total_animales = len(animales)
        
        if total_animales == 0:
            self.stdout.write(self.style.WARNING('⚠️  No hay animales con geocerca asignada'))
            return
        
        self.stdout.write(f'🐄 Rebaño detectado: {total_animales} animales con geocerca asignada')
        self.stdout.write(f'🧲 Aplicando gravedad de centroide ({gravity_factor * 100:.0f}% atracción)\n')
        
        procesados = 0
        inicializados = 0
        fugados = 0
        errores = 0
        
        for idx, animal in enumerate(animales, 1):
            try:
                if not animal.geocerca or not animal.geocerca.coordenadas:
                    continue
                
                geocerca_nombre = await sync_to_async(lambda: animal.geocerca.nombre)()
                
                # Obtener polígono
                coords = await sync_to_async(lambda: animal.geocerca.coordenadas)()
                polygon = Polygon([(c['lng'], c['lat']) for c in coords])
                centroid = polygon.centroid
                
                # Verificar inicialización
                tiene_telemetria = await sync_to_async(animal.telemetria.exists)()
                
                is_escaped = animal.collar_id == escaped_animal_id
                
                if not tiene_telemetria:
                    # Inicializar en centroide
                    lat_inicial = centroid.y
                    lng_inicial = centroid.x
                    temp_inicial, fc_inicial = self.get_base_vital_signs(animal.tipo_animal)
                    
                    inicializados += 1
                    self.stdout.write(
                        f'  🎯 [{idx}/{total_animales}] {animal.display_id}: '
                        f'INICIALIZADO en centroide de "{geocerca_nombre}"'
                    )
                else:
                    # Obtener última posición
                    last_t = await sync_to_async(animal.telemetria.first)()
                    lat_actual = await sync_to_async(lambda: last_t.latitud)()
                    lng_actual = await sync_to_async(lambda: last_t.longitud)()
                    temp_actual = await sync_to_async(lambda: last_t.temperatura_corporal)()
                    fc_actual = await sync_to_async(lambda: last_t.frecuencia_cardiaca)()
                    
                    # REQUERIMIENTO V6: Lógica de Movimiento con Gravedad
                    if is_escaped:
                        # FORZAR FUGA (V5) - Sin gravedad
                        new_lat, new_lng = self.force_escape_coordinates(
                            polygon, centroid, lat_actual, lng_actual
                        )
                        fugados += 1
                        status_icon = '🔴'
                    else:
                        # MOVIMIENTO CON GRAVEDAD DE CENTROIDE (V6)
                        new_lat, new_lng = self.calculate_centroid_gravity_move(
                            lat_actual, lng_actual, polygon, centroid, 
                            movement_range, gravity_factor
                        )
                        status_icon = '🟢'
                    
                    # Temperatura con 1 decimal (V5)
                    temp_inicial = round(self.vary_vital_sign(temp_actual, 0.2, 37.0, 40.5), 1)
                    fc_inicial = int(self.vary_vital_sign(fc_actual, 5, 40, 125))
                    
                    lat_inicial = new_lat
                    lng_inicial = new_lng
                    
                    # Calcular distancia al centroide para logs
                    dist_to_center = self.calculate_distance(
                        lat_actual, lng_actual, centroid.y, centroid.x
                    )
                    
                    # Log de estado
                    if is_escaped:
                        self.stdout.write(
                            f'  {status_icon} [{idx}/{total_animales}] {animal.display_id}: '
                            f'({lat_inicial:.6f}, {lng_inicial:.6f}) '
                            f'🚨 FUGADO de "{geocerca_nombre}" | T:{temp_inicial}°C FC:{fc_inicial}lpm'
                        )
                    else:
                        self.stdout.write(
                            f'  {status_icon} [{idx}/{total_animales}] {animal.display_id}: '
                            f'({lat_inicial:.6f}, {lng_inicial:.6f}) '
                            f'en "{geocerca_nombre}" | Dist:{dist_to_center:.4f}° | T:{temp_inicial}°C FC:{fc_inicial}lpm'
                        )
                
                # Enviar por WebSocket
                data = {
                    'collar_id': animal.collar_id,
                    'latitud': lat_inicial,
                    'longitud': lng_inicial,
                    'temperatura_corporal': temp_inicial,
                    'frecuencia_cardiaca': fc_inicial
                }
                
                await websocket.send(json.dumps(data))
                
                # Recibir respuesta con alertas
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=0.3)
                    resp_data = json.loads(response)
                    
                    if 'alertas' in resp_data and resp_data['alertas']:
                        for alerta in resp_data['alertas']:
                            self.stdout.write(
                                self.style.WARNING(f'      🚨 ALERTA: {alerta["mensaje"]}')
                            )
                except asyncio.TimeoutError:
                    pass
                
                procesados += 1
                await asyncio.sleep(0.1)
                
            except Exception as e:
                errores += 1
                collar_id = await sync_to_async(lambda: animal.collar_id)()
                self.stdout.write(
                    self.style.ERROR(f'  ✗ [{idx}/{total_animales}] Error en {collar_id}: {e}')
                )
        
        # Resumen del ciclo
        self.stdout.write(f'\n📊 Resumen del Ciclo #{cycle_count}:')
        self.stdout.write(f'   ✓ Procesados: {procesados}/{total_animales}')
        if inicializados > 0:
            self.stdout.write(f'   🎯 Inicializados: {inicializados}')
        if fugados > 0:
            self.stdout.write(self.style.ERROR(f'   🔴 Fugados: {fugados}'))
        if errores > 0:
            self.stdout.write(self.style.ERROR(f'   ✗ Errores: {errores}'))

    def calculate_centroid_gravity_move(self, lat, lng, polygon, centroid, 
                                        movement_range, gravity_factor):
        """
        REQUERIMIENTO V6: Algoritmo de Gravedad de Centroide
        
        Combina dos fuerzas:
        1. Fuerza de Paseo (Aleatoria) - 80% por defecto
        2. Fuerza de Atracción (Centroide) - 20% por defecto
        
        Esto crea un movimiento natural que tiende hacia el centro.
        """
        # --- PASO 1: Calcular Vector de Atracción (Pull Vector) ---
        vector_hacia_centroide_x = centroid.x - lng
        vector_hacia_centroide_y = centroid.y - lat
        
        # --- PASO 2: Calcular Vector de Paseo (Random Vector) ---
        random_delta_x = random.uniform(-movement_range, movement_range)
        random_delta_y = random.uniform(-movement_range, movement_range)
        
        # --- PASO 3: Combinar Vectores ---
        # gravity_factor define cuánta atracción hay (default 0.2 = 20%)
        # 1 - gravity_factor = componente aleatorio (default 0.8 = 80%)
        random_factor = 1.0 - gravity_factor
        
        movimiento_x = (random_delta_x * random_factor) + (vector_hacia_centroide_x * gravity_factor)
        movimiento_y = (random_delta_y * random_factor) + (vector_hacia_centroide_y * gravity_factor)
        
        # --- PASO 4: Calcular Posición Propuesta ---
        lng_propuesto = lng + movimiento_x
        lat_propuesta = lat + movimiento_y
        
        # --- PASO 5: Verificar Límites (Muros de Rebote) ---
        punto_propuesto = Point(lng_propuesto, lat_propuesta)
        
        if polygon.contains(punto_propuesto):
            # Movimiento aceptado - está dentro
            return lat_propuesta, lng_propuesto
        else:
            # MURO DE REBOTE - Aplicar corrección adicional hacia centroide
            # Esto es una medida de seguridad si la gravedad no fue suficiente
            
            # Calcular corrección más fuerte hacia el centro
            correction_factor = 0.5  # 50% de movimiento hacia centroide
            
            corrected_lat = lat + (vector_hacia_centroide_y * correction_factor)
            corrected_lng = lng + (vector_hacia_centroide_x * correction_factor)
            
            punto_corregido = Point(corrected_lng, corrected_lat)
            
            if polygon.contains(punto_corregido):
                return corrected_lat, corrected_lng
            else:
                # Si aún está fuera, quedarse en posición actual
                # (raro con gravedad, pero posible con geocercas muy pequeñas)
                return lat, lng

    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """Calcula distancia euclidiana simple entre dos puntos"""
        return ((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) ** 0.5

    def force_escape_coordinates(self, polygon, centroid, lat_actual, lng_actual):
        """
        FUERZA al animal a salir de la geocerca (V5).
        NO aplica gravedad - solo para fugas.
        """
        # Calcular vector desde centroide hacia posición actual
        vector_lat = lat_actual - centroid.y
        vector_lng = lng_actual - centroid.x
        
        # Si está en centroide, usar dirección aleatoria
        if abs(vector_lat) < 0.00001 and abs(vector_lng) < 0.00001:
            vector_lat = 0.001 * random.choice([1, -1])
            vector_lng = 0.001 * random.choice([1, -1])
        
        # Amplificar vector para forzar salida (x20-30)
        escape_factor = random.uniform(20, 30)
        
        escaped_lat = centroid.y + (vector_lat * escape_factor)
        escaped_lng = centroid.x + (vector_lng * escape_factor)
        
        # Verificar que esté REALMENTE fuera
        escape_point = Point(escaped_lng, escaped_lat)
        if polygon.contains(escape_point):
            # Si aún dentro, amplificar más
            escaped_lat = centroid.y + (vector_lat * escape_factor * 2)
            escaped_lng = centroid.x + (vector_lng * escape_factor * 2)
        
        return escaped_lat, escaped_lng

    def get_base_vital_signs(self, tipo_animal):
        """Retorna signos vitales base según tipo de animal (V5)"""
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
        """Aplica variación natural a un signo vital (V5)"""
        if isinstance(current_value, int):
            delta = random.randint(-int(variation), int(variation))
            new_value = current_value + delta
        else:
            delta = random.uniform(-variation, variation)
            new_value = current_value + delta
        
        return max(min_val, min(max_val, new_value))
