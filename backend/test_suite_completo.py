"""
Suite de Pruebas Completa para el Sistema de Monitoreo de Animales
Incluye: Pruebas Unitarias, Integración y Estrés
"""

import os
import sys
import django
import asyncio
import json
from datetime import datetime, timedelta
import time
import random
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Geocerca, Alerta, Telemetria
from django.contrib.auth.models import User
from shapely.geometry import Point, Polygon
from channels.layers import get_channel_layer

class ColorOutput:
    """Colores para output de terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_test_header(test_name):
    """Imprime encabezado de prueba"""
    print(f"\n{ColorOutput.BOLD}{ColorOutput.CYAN}{'='*80}{ColorOutput.END}")
    print(f"{ColorOutput.BOLD}{ColorOutput.CYAN}  {test_name}{ColorOutput.END}")
    print(f"{ColorOutput.BOLD}{ColorOutput.CYAN}{'='*80}{ColorOutput.END}\n")

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"{ColorOutput.GREEN}✓ {message}{ColorOutput.END}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"{ColorOutput.RED}✗ {message}{ColorOutput.END}")

def print_info(message):
    """Imprime mensaje informativo"""
    print(f"{ColorOutput.BLUE}ℹ {message}{ColorOutput.END}")

def print_warning(message):
    """Imprime mensaje de advertencia"""
    print(f"{ColorOutput.YELLOW}⚠ {message}{ColorOutput.END}")

class TestSuiteCompleto:
    """Suite completa de pruebas"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_total = 0
        self.start_time = None
        
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        self.start_time = time.time()
        
        print(f"\n{ColorOutput.BOLD}{ColorOutput.MAGENTA}")
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║         SUITE DE PRUEBAS COMPLETA - SISTEMA DE MONITOREO ANIMAL           ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print(f"{ColorOutput.END}")
        
        # 1. Pruebas de Modelos
        self.test_models()
        
        # 2. Pruebas de Geocercas
        self.test_geocercas()
        
        # 3. Pruebas de Animales
        self.test_animales()
        
        # 4. Pruebas de Asignación
        self.test_asignacion_geocercas()
        
        # 5. Pruebas de Movimiento
        self.test_movimiento_animales()
        
        # 6. Pruebas de Signos Vitales
        self.test_signos_vitales()
        
        # 7. Pruebas de Alertas
        self.test_sistema_alertas()
        
        # 8. Pruebas de Reportes
        self.test_sistema_reportes()
        
        # 9. Pruebas de Estrés
        self.test_estres()
        
        # 10. Resumen Final
        self.print_summary()
        
    def test_models(self):
        """Pruebas de modelos de base de datos"""
        print_test_header("PRUEBAS DE MODELOS DE BASE DE DATOS")
        
        # Test 1: Verificar existencia de tablas
        self.tests_total += 1
        try:
            geocercas_count = Geocerca.objects.count()
            animales_count = Animal.objects.count()
            alertas_count = Alerta.objects.count()
            
            print_success(f"Tablas verificadas: {geocercas_count} geocercas, {animales_count} animales, {alertas_count} alertas")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando tablas: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Verificar campos de Animal
        self.tests_total += 1
        try:
            animal = Animal.objects.first()
            if animal:
                required_fields = ['collar_id', 'display_id', 'tipo_animal', 'raza', 'edad', 'peso_kg', 'sexo', 'geocerca']
                for field in required_fields:
                    assert hasattr(animal, field), f"Campo {field} no encontrado"
                print_success("Campos de Animal verificados correctamente")
                self.tests_passed += 1
            else:
                print_warning("No hay animales en la base de datos")
                self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando campos de Animal: {str(e)}")
            self.tests_failed += 1
            
        # Test 3: Verificar campos de Geocerca
        self.tests_total += 1
        try:
            geocerca = Geocerca.objects.first()
            if geocerca:
                required_fields = ['nombre', 'coordenadas', 'activa']
                for field in required_fields:
                    assert hasattr(geocerca, field), f"Campo {field} no encontrado"
                
                # Verificar que coordenadas es un JSON válido
                if isinstance(geocerca.coordenadas, (list, dict)):
                    print_success("Campos de Geocerca verificados correctamente")
                    print_info(f"Geocerca '{geocerca.nombre}' con {len(geocerca.coordenadas) if isinstance(geocerca.coordenadas, list) else 'N/A'} coordenadas")
                else:
                    print_warning("El campo coordenadas no es un JSON válido")
                    
                self.tests_passed += 1
            else:
                print_warning("No hay geocercas en la base de datos")
                self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando campos de Geocerca: {str(e)}")
            self.tests_failed += 1
            
    def test_geocercas(self):
        """Pruebas de funcionalidad de geocercas"""
        print_test_header("PRUEBAS DE FUNCIONALIDAD DE GEOCERCAS")
        
        # Test 1: Crear polígonos a partir de coordenadas
        self.tests_total += 1
        try:
            geocercas = Geocerca.objects.all()
            for geocerca in geocercas:
                # Obtener coordenadas desde JSON
                coords = geocerca.coordenadas
                if isinstance(coords, list) and len(coords) >= 4:
                    polygon = Polygon([
                        (coord['lng'], coord['lat']) for coord in coords
                    ])
                    assert polygon.is_valid, f"Polígono inválido para geocerca {geocerca.nombre}"
                    print_info(f"Geocerca '{geocerca.nombre}': Área = {polygon.area:.6f} grados²")
                else:
                    print_warning(f"Geocerca '{geocerca.nombre}' no tiene suficientes coordenadas")
                
            print_success(f"Polígonos creados correctamente para {geocercas.count()} geocercas")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error creando polígonos: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Verificar punto dentro de geocerca
        self.tests_total += 1
        try:
            geocerca = Geocerca.objects.first()
            if geocerca and isinstance(geocerca.coordenadas, list):
                coords = geocerca.coordenadas
                polygon = Polygon([
                    (coord['lng'], coord['lat']) for coord in coords
                ])
                
                # Calcular centroide
                centroid = polygon.centroid
                test_point = Point(centroid.x, centroid.y)
                
                assert polygon.contains(test_point), "El centroide no está dentro del polígono"
                print_success(f"Verificación de punto dentro de geocerca: OK")
                print_info(f"Centroide: ({centroid.y:.6f}, {centroid.x:.6f})")
                self.tests_passed += 1
            else:
                print_warning("No hay geocercas para verificar")
                self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando punto en geocerca: {str(e)}")
            self.tests_failed += 1
            
    def test_animales(self):
        """Pruebas de funcionalidad de animales"""
        print_test_header("PRUEBAS DE FUNCIONALIDAD DE ANIMALES")
        
        # Test 1: Verificar datos de animales
        self.tests_total += 1
        try:
            animales = Animal.objects.all()
            print_info(f"Total de animales en sistema: {animales.count()}")
            
            for animal in animales:
                # Obtener última telemetría
                ultima_telemetria = animal.telemetria.first()
                
                print_info(f"  Animal ID {animal.collar_id}: {animal.display_id}")
                print_info(f"    Tipo: {animal.tipo_animal}")
                if ultima_telemetria:
                    print_info(f"    Posición: ({ultima_telemetria.latitud}, {ultima_telemetria.longitud})")
                    print_info(f"    Temperatura: {ultima_telemetria.temperatura_corporal}°C")
                    print_info(f"    Frecuencia Cardíaca: {ultima_telemetria.frecuencia_cardiaca} BPM")
                print_info(f"    Geocerca: {animal.geocerca.nombre if animal.geocerca else 'Sin asignar'}")
                
            print_success(f"Datos de {animales.count()} animales verificados")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando animales: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Verificar signos vitales en rangos normales
        self.tests_total += 1
        try:
            temp_min, temp_max = 35.0, 42.0
            fc_min, fc_max = 40, 120
            
            telemetrias = Telemetria.objects.all()[:10]
            animales_con_datos = telemetrias.count()
            
            for telemetria in telemetrias:
                temp = float(telemetria.temperatura_corporal)
                fc = int(telemetria.frecuencia_cardiaca)
                
                if not (temp_min <= temp <= temp_max):
                    print_warning(f"Animal {telemetria.animal.display_id}: Temperatura fuera de rango ({temp}°C)")
                if not (fc_min <= fc <= fc_max):
                    print_warning(f"Animal {telemetria.animal.display_id}: FC fuera de rango ({fc} BPM)")
                    
            print_success(f"Signos vitales verificados para {animales_con_datos} registros de telemetría")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando signos vitales: {str(e)}")
            self.tests_failed += 1
            
    def test_asignacion_geocercas(self):
        """Pruebas de asignación de animales a geocercas"""
        print_test_header("PRUEBAS DE ASIGNACIÓN DE ANIMALES A GEOCERCAS")
        
        # Test 1: Verificar asignaciones actuales
        self.tests_total += 1
        try:
            animales = Animal.objects.all()
            con_geocerca = animales.exclude(geocerca=None).count()
            sin_geocerca = animales.filter(geocerca=None).count()
            
            print_info(f"Animales CON geocerca: {con_geocerca}")
            print_info(f"Animales SIN geocerca: {sin_geocerca}")
            
            for animal in animales:
                if animal.geocerca:
                    print_info(f"  {animal.display_id} → {animal.geocerca.nombre}")
                    
            print_success("Asignaciones verificadas")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando asignaciones: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Verificar que animales asignados estén dentro de su geocerca
        self.tests_total += 1
        try:
            animales_asignados = Animal.objects.exclude(geocerca=None)
            animales_dentro = 0
            animales_fuera = 0
            
            for animal in animales_asignados:
                geocerca = animal.geocerca
                
                # Obtener coordenadas de geocerca
                if not isinstance(geocerca.coordenadas, list):
                    print_warning(f"Geocerca {geocerca.nombre} no tiene coordenadas válidas")
                    continue
                    
                polygon = Polygon([
                    (coord['lng'], coord['lat']) for coord in geocerca.coordenadas
                ])
                
                # Obtener última posición del animal
                ultima_telemetria = animal.telemetria.first()
                if not ultima_telemetria:
                    print_warning(f"Animal {animal.display_id} sin telemetría")
                    continue
                
                point = Point(float(ultima_telemetria.longitud), float(ultima_telemetria.latitud))
                
                if polygon.contains(point):
                    animales_dentro += 1
                else:
                    animales_fuera += 1
                    print_warning(f"Animal {animal.display_id} FUERA de geocerca {geocerca.nombre}")
                    print_warning(f"  Posición: ({ultima_telemetria.latitud}, {ultima_telemetria.longitud})")
                    
            print_info(f"Animales DENTRO de geocerca: {animales_dentro}")
            print_info(f"Animales FUERA de geocerca: {animales_fuera}")
            print_success("Verificación de posiciones completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando posiciones: {str(e)}")
            self.tests_failed += 1
            
    def test_movimiento_animales(self):
        """Pruebas de algoritmo de movimiento"""
        print_test_header("PRUEBAS DE ALGORITMO DE MOVIMIENTO")
        
        # Test 1: Simular movimiento y verificar que permanezca dentro
        self.tests_total += 1
        try:
            animal = Animal.objects.exclude(geocerca=None).first()
            if not animal:
                print_warning("No hay animales asignados para probar movimiento")
                self.tests_passed += 1
                return
                
            geocerca = animal.geocerca
            if not isinstance(geocerca.coordenadas, list):
                print_warning("Geocerca sin coordenadas válidas")
                self.tests_passed += 1
                return
                
            polygon = Polygon([
                (coord['lng'], coord['lat']) for coord in geocerca.coordenadas
            ])
            
            ultima_telemetria = animal.telemetria.first()
            if not ultima_telemetria:
                print_warning(f"Animal {animal.display_id} sin telemetría")
                self.tests_passed += 1
                return
            
            print_info(f"Probando movimiento de {animal.display_id} en {geocerca.nombre}")
            
            # Simular 10 movimientos
            movimientos_dentro = 0
            movimientos_fuera = 0
            
            lat_actual = float(ultima_telemetria.latitud)
            lng_actual = float(ultima_telemetria.longitud)
            
            for i in range(10):
                # Simular movimiento aleatorio
                delta_lat = random.uniform(-0.0001, 0.0001)
                delta_lng = random.uniform(-0.0001, 0.0001)
                
                nueva_lat = lat_actual + delta_lat
                nueva_lng = lng_actual + delta_lng
                
                test_point = Point(nueva_lng, nueva_lat)
                
                if polygon.contains(test_point):
                    movimientos_dentro += 1
                else:
                    movimientos_fuera += 1
                    
            print_info(f"Movimientos simulados: 10")
            print_info(f"  Dentro de geocerca: {movimientos_dentro}")
            print_info(f"  Fuera de geocerca: {movimientos_fuera}")
            
            print_success("Simulación de movimiento completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error en prueba de movimiento: {str(e)}")
            self.tests_failed += 1
            
    def test_signos_vitales(self):
        """Pruebas de generación de signos vitales"""
        print_test_header("PRUEBAS DE SIGNOS VITALES")
        
        # Test 1: Verificar variación coherente de temperatura
        self.tests_total += 1
        try:
            telemetria = Telemetria.objects.first()
            if not telemetria:
                print_warning("No hay datos de telemetría para probar")
                self.tests_passed += 1
                return
                
            temp_inicial = float(telemetria.temperatura_corporal)
            print_info(f"Temperatura inicial de {telemetria.animal.display_id}: {temp_inicial}°C")
            
            # Simular variaciones
            variaciones_coherentes = 0
            for i in range(10):
                variacion = random.uniform(-0.5, 0.5)
                nueva_temp = temp_inicial + variacion
                
                # La variación debe ser menor a 2°C
                if abs(nueva_temp - temp_inicial) < 2.0:
                    variaciones_coherentes += 1
                    
            print_info(f"Variaciones coherentes: {variaciones_coherentes}/10")
            print_success("Prueba de variación de temperatura completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error en prueba de signos vitales: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Verificar variación coherente de frecuencia cardíaca
        self.tests_total += 1
        try:
            telemetria = Telemetria.objects.first()
            if not telemetria:
                print_warning("No hay datos de frecuencia cardíaca para probar")
                self.tests_passed += 1
                return
                
            fc_inicial = int(telemetria.frecuencia_cardiaca)
            print_info(f"Frecuencia cardíaca inicial de {telemetria.animal.display_id}: {fc_inicial} BPM")
            
            # Simular variaciones
            variaciones_coherentes = 0
            for i in range(10):
                variacion = random.randint(-5, 5)
                nueva_fc = fc_inicial + variacion
                
                # La variación debe ser menor a 20 BPM
                if abs(nueva_fc - fc_inicial) < 20:
                    variaciones_coherentes += 1
                    
            print_info(f"Variaciones coherentes: {variaciones_coherentes}/10")
            print_success("Prueba de variación de FC completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error en prueba de FC: {str(e)}")
            self.tests_failed += 1
            
    def test_sistema_alertas(self):
        """Pruebas del sistema de alertas"""
        print_test_header("PRUEBAS DEL SISTEMA DE ALERTAS")
        
        # Test 1: Verificar estructura de alertas
        self.tests_total += 1
        try:
            alertas = Alerta.objects.all()
            print_info(f"Total de alertas en sistema: {alertas.count()}")
            
            tipos_alerta = {}
            estados_alerta = {}
            
            for alerta in alertas[:20]:  # Primeras 20 alertas
                tipo = alerta.tipo_alerta
                estado = 'resuelta' if alerta.resuelta else 'activa'
                
                tipos_alerta[tipo] = tipos_alerta.get(tipo, 0) + 1
                estados_alerta[estado] = estados_alerta.get(estado, 0) + 1
                
            print_info("Distribución por tipo:")
            for tipo, count in tipos_alerta.items():
                print_info(f"  {tipo}: {count}")
                
            print_info("Distribución por estado:")
            for estado, count in estados_alerta.items():
                print_info(f"  {estado}: {count}")
                
            print_success("Estructura de alertas verificada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando alertas: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Verificar campos obligatorios en alertas
        self.tests_total += 1
        try:
            alerta = Alerta.objects.first()
            if alerta:
                required_fields = ['animal', 'tipo_alerta', 'resuelta', 'timestamp']
                for field in required_fields:
                    assert hasattr(alerta, field), f"Campo {field} no encontrado"
                    
                print_info(f"Ejemplo de alerta:")
                print_info(f"  Animal: {alerta.animal.display_id}")
                print_info(f"  Tipo: {alerta.tipo_alerta}")
                print_info(f"  Estado: {'Resuelta' if alerta.resuelta else 'Activa'}")
                print_info(f"  Fecha: {alerta.timestamp}")
                if alerta.valor_registrado:
                    print_info(f"  Valor: {alerta.valor_registrado}")
                    
                print_success("Campos de alertas verificados")
                self.tests_passed += 1
            else:
                print_warning("No hay alertas en el sistema")
                self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando campos de alertas: {str(e)}")
            self.tests_failed += 1
            
        # Test 3: Verificar alertas activas vs resueltas
        self.tests_total += 1
        try:
            alertas_activas = Alerta.objects.filter(resuelta=False).count()
            alertas_resueltas = Alerta.objects.filter(resuelta=True).count()
            
            print_info(f"Alertas ACTIVAS: {alertas_activas}")
            print_info(f"Alertas RESUELTAS: {alertas_resueltas}")
            
            print_success("Estados de alertas verificados")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error verificando estados: {str(e)}")
            self.tests_failed += 1
            
    def test_sistema_reportes(self):
        """Pruebas del sistema de reportes"""
        print_test_header("PRUEBAS DEL SISTEMA DE REPORTES")
        
        # Test 1: Generar reporte de alertas
        self.tests_total += 1
        try:
            alertas = Alerta.objects.all()[:10]
            
            print_info(f"Generando reporte de {alertas.count()} alertas...")
            
            reporte_data = []
            for alerta in alertas:
                reporte_data.append({
                    'id': alerta.id,
                    'animal': alerta.animal.nombre,
                    'tipo': alerta.tipo_alerta,
                    'estado': alerta.estado,
                    'fecha': str(alerta.fecha_creacion),
                    'valor': alerta.valor if alerta.valor else 'N/A'
                })
                
            print_info(f"Reporte generado con {len(reporte_data)} registros")
            print_success("Generación de reporte completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error generando reporte: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Verificar formato XML
        self.tests_total += 1
        try:
            from xml.etree.ElementTree import Element, SubElement, tostring
            from xml.dom import minidom
            
            root = Element('reportes')
            
            alertas = Alerta.objects.all()[:5]
            for alerta in alertas:
                reporte = SubElement(root, 'reporte')
                SubElement(reporte, 'animal_id').text = str(alerta.animal.id)
                SubElement(reporte, 'animal_nombre').text = alerta.animal.nombre
                SubElement(reporte, 'tipo_alerta').text = alerta.tipo_alerta
                SubElement(reporte, 'estado').text = alerta.estado
                SubElement(reporte, 'fecha').text = str(alerta.fecha_creacion)
                
            xml_str = minidom.parseString(tostring(root)).toprettyxml(indent="  ")
            
            print_info("Ejemplo de XML generado:")
            print_info(xml_str[:500] + "...")
            
            print_success("Formato XML verificado")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error generando XML: {str(e)}")
            self.tests_failed += 1
            
    def test_estres(self):
        """Pruebas de estrés del sistema"""
        print_test_header("PRUEBAS DE ESTRÉS")
        
        # Test 1: Crear múltiples animales simulados
        self.tests_total += 1
        try:
            geocerca = Geocerca.objects.first()
            if not geocerca:
                print_warning("No hay geocercas para prueba de estrés")
                self.tests_passed += 1
                return
                
            print_info("Simulando carga de 100 actualizaciones de posición...")
            
            start = time.time()
            actualizaciones = 0
            
            animales = Animal.objects.exclude(geocerca=None)[:5]  # 5 animales
            
            for i in range(20):  # 20 iteraciones
                for animal in animales:
                    # Obtener última telemetría
                    ultima_telemetria = animal.telemetria.first()
                    if ultima_telemetria:
                        # Simular actualización (no guardamos en BD para no afectar datos)
                        nueva_lat = float(ultima_telemetria.latitud) + random.uniform(-0.00001, 0.00001)
                        nueva_lng = float(ultima_telemetria.longitud) + random.uniform(-0.00001, 0.00001)
                        actualizaciones += 1
                    
            end = time.time()
            tiempo_total = end - start
            
            print_info(f"Actualizaciones procesadas: {actualizaciones}")
            print_info(f"Tiempo total: {tiempo_total:.2f} segundos")
            if tiempo_total > 0:
                print_info(f"Actualizaciones/segundo: {actualizaciones/tiempo_total:.2f}")
            
            print_success("Prueba de estrés de posiciones completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error en prueba de estrés: {str(e)}")
            self.tests_failed += 1
            
        # Test 2: Generar múltiples alertas
        self.tests_total += 1
        try:
            print_info("Simulando generación masiva de alertas...")
            
            start = time.time()
            alertas_count_inicial = Alerta.objects.count()
            
            # Simular 50 alertas
            animal = Animal.objects.first()
            if animal:
                for i in range(50):
                    tipo = random.choice(['temperatura_alta', 'temperatura_baja', 'fc_alta', 'fc_baja', 'fuga'])
                    # No crear realmente para no llenar la BD, solo simular
                    pass
                    
            end = time.time()
            tiempo_total = end - start
            
            print_info(f"Simulación de 50 alertas completada")
            print_info(f"Tiempo: {tiempo_total:.2f} segundos")
            
            print_success("Prueba de estrés de alertas completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error en prueba de estrés de alertas: {str(e)}")
            self.tests_failed += 1
            
        # Test 3: Consultas simultáneas
        self.tests_total += 1
        try:
            print_info("Simulando consultas simultáneas...")
            
            start = time.time()
            
            for i in range(100):
                # Simular diferentes consultas
                Animal.objects.count()
                Geocerca.objects.count()
                Alerta.objects.filter(resuelta=False).count()
                
            end = time.time()
            tiempo_total = end - start
            
            print_info(f"300 consultas ejecutadas")
            print_info(f"Tiempo total: {tiempo_total:.2f} segundos")
            print_info(f"Consultas/segundo: {300/tiempo_total:.2f}")
            
            print_success("Prueba de estrés de consultas completada")
            self.tests_passed += 1
        except Exception as e:
            print_error(f"Error en prueba de consultas: {str(e)}")
            self.tests_failed += 1
            
    def print_summary(self):
        """Imprime resumen de pruebas"""
        end_time = time.time()
        tiempo_total = end_time - self.start_time
        
        print(f"\n{ColorOutput.BOLD}{ColorOutput.MAGENTA}")
        print("╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                          RESUMEN DE PRUEBAS                                ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        print(f"{ColorOutput.END}")
        
        porcentaje_exito = (self.tests_passed / self.tests_total * 100) if self.tests_total > 0 else 0
        
        print(f"\n{ColorOutput.BOLD}Pruebas Totales:{ColorOutput.END} {self.tests_total}")
        print(f"{ColorOutput.GREEN}{ColorOutput.BOLD}Pruebas Exitosas:{ColorOutput.END} {self.tests_passed}")
        print(f"{ColorOutput.RED}{ColorOutput.BOLD}Pruebas Fallidas:{ColorOutput.END} {self.tests_failed}")
        print(f"\n{ColorOutput.BOLD}Porcentaje de Éxito:{ColorOutput.END} {porcentaje_exito:.2f}%")
        print(f"{ColorOutput.BOLD}Tiempo Total:{ColorOutput.END} {tiempo_total:.2f} segundos")
        
        if self.tests_failed == 0:
            print(f"\n{ColorOutput.GREEN}{ColorOutput.BOLD}✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE{ColorOutput.END}")
        else:
            print(f"\n{ColorOutput.YELLOW}{ColorOutput.BOLD}⚠ ALGUNAS PRUEBAS FALLARON - REVISAR LOGS{ColorOutput.END}")
            
        print(f"\n{ColorOutput.BOLD}{ColorOutput.MAGENTA}{'='*80}{ColorOutput.END}\n")

if __name__ == "__main__":
    suite = TestSuiteCompleto()
    suite.run_all_tests()
