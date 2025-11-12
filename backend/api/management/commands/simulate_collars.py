"""
Management Command: simulate_collars
Versión 4.0 - CAMPORT - SIMULADOR DE REBAÑO COMPLETO

Características V4.0:
- Simulación de REBAÑO COMPLETO (todos los animales en cada ciclo)
- Intervalo LENTO y REALISTA (20-30 segundos por defecto)
- Adherencia DINÁMICA y ESTRICTA a geocercas
- Consulta estado EN VIVO en cada ciclo
- Reacción automática a cambios de asignación de geocercas
- Integración WebSocket para actualizaciones en tiempo real

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
    help = 'Simulador CAMPORT V4.0 - Rebaño Completo con Adherencia Dinámica a Geocercas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=20,
            help='Intervalo de actualización en segundos (default: 20 - realista)'
        )
        parser.add_argument(
            '--movement-range',
            type=float,
            default=0.0002,
            help='Rango de movimiento aleatorio (default: 0.0002 grados - lento)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        movement_range = options['movement_range']

        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('🐄 CAMPORT V4.0 - SIMULADOR DE REBAÑO COMPLETO 🐄'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(f'⏱️  Intervalo: {interval} segundos (movimiento realista)')
        self.stdout.write(f'📏 Rango movimiento: {movement_range} grados')
        self.stdout.write(f'🔄 Consulta dinámica de geocercas en cada ciclo')
        self.stdout.write(self.style.SUCCESS('=' * 70 + '\n'))

        try:
            asyncio.run(self.run_simulation(interval, movement_range))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⏹️  Simulación detenida por el usuario'))
            self.stdout.write(self.style.SUCCESS('Gracias por usar CAMPORT V4.0\n'))

    async def run_simulation(self, interval, movement_range):
        """Ejecuta simulación continua con WebSocket"""
        uri = 'ws://localhost:8000/ws/telemetria/'
        cycle_count = 0
        
        try:
            async with websockets.connect(uri) as websocket:
                self.stdout.write(self.style.SUCCESS('✓ Conectado a WebSocket\n'))
                
                while True:
                    cycle_count += 1
                    self.stdout.write(self.style.SUCCESS(f'\n{"="*70}'))
                    self.stdout.write(self.style.SUCCESS(f'📡 CICLO #{cycle_count} - Consultando estado EN VIVO del rebaño...'))
                    self.stdout.write(self.style.SUCCESS(f'{"="*70}'))
                    
                    # REQUERIMIENTO 3: Adherencia Dinámica - Consultar estado EN VIVO
                    await self.simulate_herd_cycle(websocket, movement_range, cycle_count)
                    
                    # REQUERIMIENTO 2: Intervalo Lento y Realista
                    self.stdout.write(self.style.WARNING(f'\n⏳ Ciclo #{cycle_count} completado. Esperando {interval} segundos...'))
                    self.stdout.write(self.style.WARNING(f'   (Movimiento lento y realista del ganado)\n'))
                    await asyncio.sleep(interval)
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error WebSocket: {e}'))
            self.stdout.write(self.style.WARNING('💡 Asegúrate de que el backend esté corriendo en http://localhost:8000'))

    async def simulate_herd_cycle(self, websocket, movement_range, cycle_count):
        """
        REQUERIMIENTO 1: Simula TODO el rebaño en un ciclo
        REQUERIMIENTO 3: Obtiene estado EN VIVO de la BD
        """
        # Consultar TODOS los animales con geocerca asignada (estado EN VIVO)
        animales = await sync_to_async(list)(
            Animal.objects.filter(geocerca__isnull=False)
                          .select_related('geocerca')
                          .order_by('display_id')
        )
        
        total_animales = len(animales)
        
        if total_animales == 0:
            self.stdout.write(self.style.WARNING('⚠️  No hay animales con geocerca asignada'))
            self.stdout.write(self.style.WARNING('   Asigna geocercas a los animales desde el Panel Admin'))
            return
        
        self.stdout.write(f'🐄 Rebaño detectado: {total_animales} animales con geocerca asignada\n')
        
        # Estadísticas del ciclo
        procesados = 0
        inicializados = 0
        errores = 0
        
        # REQUERIMIENTO 1: Procesar TODOS los animales del rebaño
        for idx, animal in enumerate(animales, 1):
            try:
                # Verificar que tiene geocerca (doble verificación de seguridad)
                if not animal.geocerca or not animal.geocerca.coordenadas:
                    continue
                
                geocerca_nombre = await sync_to_async(lambda: animal.geocerca.nombre)()
                
                # Obtener polígono de Shapely
                coords = await sync_to_async(lambda: animal.geocerca.coordenadas)()
                polygon = Polygon([(c['lng'], c['lat']) for c in coords])
                centroid = polygon.centroid
                
                # Verificar si necesita inicialización
                tiene_telemetria = await sync_to_async(animal.telemetria.exists)()
                
                if not tiene_telemetria:
                    # LÓGICA V3: Inicialización en Centroide
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
                    
                    # LÓGICA V3: Pastoreo Virtual
                    lat_inicial = await sync_to_async(lambda: last_t.latitud)()
                    lng_inicial = await sync_to_async(lambda: last_t.longitud)()
                    
                    # Calcular nueva posición con pastoreo virtual
                    new_lat, new_lng = self.calculate_virtual_grazing_move(
                        lat_inicial, lng_inicial, polygon, centroid, movement_range
                    )
                    
                    # Generar signos vitales con variación
                    temp_actual = await sync_to_async(lambda: last_t.temperatura_corporal)()
                    fc_actual = await sync_to_async(lambda: last_t.frecuencia_cardiaca)()
                    
                    temp_inicial = self.vary_vital_sign(temp_actual, 0.2, 37.0, 40.5)
                    fc_inicial = int(self.vary_vital_sign(fc_actual, 5, 40, 125))
                    
                    lat_inicial = new_lat
                    lng_inicial = new_lng
                
                # Enviar por WebSocket
                data = {
                    'collar_id': animal.collar_id,
                    'latitud': lat_inicial,
                    'longitud': lng_inicial,
                    'temperatura_corporal': temp_inicial,
                    'frecuencia_cardiaca': fc_inicial
                }
                
                await websocket.send(json.dumps(data))
                
                # Intentar recibir respuesta con alertas
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
                
                # Log de estado
                if tiene_telemetria:
                    self.stdout.write(
                        f'  🟢 [{idx}/{total_animales}] {animal.display_id}: '
                        f'({lat_inicial:.6f}, {lng_inicial:.6f}) '
                        f'en "{geocerca_nombre}" | T:{temp_inicial:.1f}°C FC:{fc_inicial}lpm'
                    )
                
                procesados += 1
                
                # Pequeña pausa entre animales para no saturar
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
        if errores > 0:
            self.stdout.write(self.style.ERROR(f'   ✗ Errores: {errores}'))

    def calculate_virtual_grazing_move(self, lat, lng, polygon, centroid, movement_range):
        """
        Algoritmo de Pastoreo Virtual V3:
        - Propone movimiento aleatorio
        - Si sale de geocerca, corrige hacia centroide
        - Mantiene animal dentro de límites
        """
        # Proponer movimiento aleatorio
        new_lat = lat + random.uniform(-movement_range, movement_range)
        new_lng = lng + random.uniform(-movement_range, movement_range)
        
        point = Point(new_lng, new_lat)
        
        # Verificar si está dentro
        if polygon.contains(point):
            return new_lat, new_lng
        else:
            # Corrección hacia centroide (30% del vector)
            vector_lat = centroid.y - lat
            vector_lng = centroid.x - lng
            
            correction_factor = 0.3
            corrected_lat = lat + (vector_lat * correction_factor * movement_range / 0.0002)
            corrected_lng = lng + (vector_lng * correction_factor * movement_range / 0.0002)
            
            corrected_point = Point(corrected_lng, corrected_lat)
            
            if polygon.contains(corrected_point):
                return corrected_lat, corrected_lng
            else:
                # Si corrección falla, mantener posición
                return lat, lng

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
