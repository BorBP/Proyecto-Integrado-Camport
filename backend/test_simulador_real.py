"""
Script de Diagnóstico en Tiempo Real del Simulador
Verifica que el simulador esté funcionando correctamente
"""

import os
import sys
import django
import time
import asyncio
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Geocerca, Alerta, Telemetria
from shapely.geometry import Point, Polygon

class ColorOutput:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{ColorOutput.BOLD}{ColorOutput.CYAN}{'='*80}{ColorOutput.END}")
    print(f"{ColorOutput.BOLD}{ColorOutput.CYAN}{text:^80}{ColorOutput.END}")
    print(f"{ColorOutput.BOLD}{ColorOutput.CYAN}{'='*80}{ColorOutput.END}\n")

def print_success(text):
    print(f"{ColorOutput.GREEN}✓ {text}{ColorOutput.END}")

def print_error(text):
    print(f"{ColorOutput.RED}✗ {text}{ColorOutput.END}")

def print_warning(text):
    print(f"{ColorOutput.YELLOW}⚠ {text}{ColorOutput.END}")

def print_info(text):
    print(f"{ColorOutput.BLUE}ℹ {text}{ColorOutput.END}")

def verificar_simulador_corriendo():
    """Verifica si el simulador está generando datos"""
    print_header("VERIFICACIÓN DE SIMULADOR EN TIEMPO REAL")
    
    # 1. Contar telemetrías iniciales
    telemetrias_inicial = Telemetria.objects.count()
    alertas_inicial = Alerta.objects.count()
    
    print_info(f"Telemetrías en BD (inicial): {telemetrias_inicial}")
    print_info(f"Alertas en BD (inicial): {alertas_inicial}")
    
    # Obtener la última telemetría
    ultima_telemetria = Telemetria.objects.first()
    if ultima_telemetria:
        print_info(f"Última telemetría: {ultima_telemetria.animal.display_id} a las {ultima_telemetria.timestamp}")
        ultima_fecha = ultima_telemetria.timestamp
        
        # Calcular tiempo desde última actualización
        ahora = datetime.now(ultima_fecha.tzinfo)
        diferencia = (ahora - ultima_fecha).total_seconds()
        
        if diferencia < 5:
            print_success(f"Simulador ACTIVO (última actualización hace {diferencia:.1f} segundos)")
        elif diferencia < 30:
            print_warning(f"Simulador posiblemente activo (última actualización hace {diferencia:.1f} segundos)")
        else:
            print_error(f"Simulador NO ACTIVO (última actualización hace {diferencia:.1f} segundos)")
    else:
        print_error("No hay telemetría en la base de datos")
    
    print("\n" + "="*80)
    print_info("Esperando 10 segundos para verificar nuevas actualizaciones...")
    print("="*80 + "\n")
    
    time.sleep(10)
    
    # 2. Contar telemetrías después de esperar
    telemetrias_final = Telemetria.objects.count()
    alertas_final = Alerta.objects.count()
    
    nuevas_telemetrias = telemetrias_final - telemetrias_inicial
    nuevas_alertas = alertas_final - alertas_inicial
    
    print_info(f"Telemetrías en BD (final): {telemetrias_final}")
    print_info(f"Alertas en BD (final): {alertas_final}")
    
    print(f"\n{ColorOutput.BOLD}Resultados:{ColorOutput.END}")
    
    if nuevas_telemetrias > 0:
        print_success(f"Se generaron {nuevas_telemetrias} nuevas telemetrías")
    else:
        print_error("NO se generaron nuevas telemetrías - SIMULADOR DETENIDO")
    
    if nuevas_alertas > 0:
        print_success(f"Se generaron {nuevas_alertas} nuevas alertas")
    else:
        print_info("No se generaron nuevas alertas (esto es normal)")
    
    return nuevas_telemetrias > 0

def verificar_datos_coherentes():
    """Verifica que los datos sean coherentes"""
    print_header("VERIFICACIÓN DE COHERENCIA DE DATOS")
    
    # 1. Verificar que los animales estén dentro de sus geocercas
    print_info("Verificando posiciones de animales...")
    
    animales = Animal.objects.exclude(geocerca=None)
    dentro = 0
    fuera = 0
    
    for animal in animales:
        geocerca = animal.geocerca
        if not isinstance(geocerca.coordenadas, list):
            continue
            
        polygon = Polygon([
            (coord['lng'], coord['lat']) for coord in geocerca.coordenadas
        ])
        
        ultima_telemetria = animal.telemetria.first()
        if not ultima_telemetria:
            continue
        
        point = Point(float(ultima_telemetria.longitud), float(ultima_telemetria.latitud))
        
        if polygon.contains(point):
            dentro += 1
            print_success(f"{animal.display_id} DENTRO de {geocerca.nombre}")
        else:
            fuera += 1
            print_error(f"{animal.display_id} FUERA de {geocerca.nombre}")
            print_info(f"  Posición: ({ultima_telemetria.latitud:.6f}, {ultima_telemetria.longitud:.6f})")
    
    print(f"\n{ColorOutput.BOLD}Resumen de posiciones:{ColorOutput.END}")
    print_info(f"Animales DENTRO: {dentro}")
    print_info(f"Animales FUERA: {fuera}")
    
    # 2. Verificar signos vitales
    print(f"\n{ColorOutput.BOLD}Verificando signos vitales...{ColorOutput.END}")
    
    telemetrias_recientes = Telemetria.objects.all()[:10]
    
    temp_normal = 0
    temp_anormal = 0
    fc_normal = 0
    fc_anormal = 0
    
    for telem in telemetrias_recientes:
        # Temperatura normal: 35-42°C
        if 35.0 <= telem.temperatura_corporal <= 42.0:
            temp_normal += 1
        else:
            temp_anormal += 1
            print_warning(f"{telem.animal.display_id}: Temp = {telem.temperatura_corporal}°C")
        
        # FC normal: 40-120 BPM
        if 40 <= telem.frecuencia_cardiaca <= 120:
            fc_normal += 1
        else:
            fc_anormal += 1
            print_warning(f"{telem.animal.display_id}: FC = {telem.frecuencia_cardiaca} BPM")
    
    print(f"\n{ColorOutput.BOLD}Resumen de signos vitales:{ColorOutput.END}")
    print_info(f"Temperaturas normales: {temp_normal}/{temp_normal + temp_anormal}")
    print_info(f"Frecuencias cardíacas normales: {fc_normal}/{fc_normal + fc_anormal}")

def verificar_alertas():
    """Verifica el sistema de alertas"""
    print_header("VERIFICACIÓN DE SISTEMA DE ALERTAS")
    
    alertas_recientes = Alerta.objects.all()[:10]
    
    if not alertas_recientes:
        print_warning("No hay alertas en el sistema")
        return
    
    print_info(f"Últimas {alertas_recientes.count()} alertas:")
    
    tipos = {}
    for alerta in alertas_recientes:
        tipo = alerta.tipo_alerta
        tipos[tipo] = tipos.get(tipo, 0) + 1
        
        estado = "RESUELTA" if alerta.resuelta else "ACTIVA"
        color = ColorOutput.GREEN if alerta.resuelta else ColorOutput.RED
        
        print(f"  {color}[{estado}]{ColorOutput.END} {alerta.animal.display_id}: {tipo}")
        print(f"    Fecha: {alerta.timestamp}")
        if alerta.valor_registrado:
            print(f"    Valor: {alerta.valor_registrado}")
    
    print(f"\n{ColorOutput.BOLD}Distribución por tipo:{ColorOutput.END}")
    for tipo, count in tipos.items():
        print_info(f"  {tipo}: {count}")
    
    # Alertas activas vs resueltas
    activas = Alerta.objects.filter(resuelta=False).count()
    resueltas = Alerta.objects.filter(resuelta=True).count()
    
    print(f"\n{ColorOutput.BOLD}Estado de alertas:{ColorOutput.END}")
    print_info(f"Activas: {activas}")
    print_info(f"Resueltas: {resueltas}")

def verificar_intervalos():
    """Verifica los intervalos de actualización"""
    print_header("VERIFICACIÓN DE INTERVALOS DE ACTUALIZACIÓN")
    
    print_info("Analizando últimas 30 telemetrías por animal...")
    
    animales = Animal.objects.all()
    
    for animal in animales:
        telemetrias = list(animal.telemetria.all()[:30])
        
        if len(telemetrias) < 2:
            print_warning(f"{animal.display_id}: Datos insuficientes")
            continue
        
        # Calcular intervalo promedio
        intervalos = []
        for i in range(len(telemetrias) - 1):
            t1 = telemetrias[i].timestamp
            t2 = telemetrias[i+1].timestamp
            diferencia = abs((t1 - t2).total_seconds())
            intervalos.append(diferencia)
        
        if intervalos:
            intervalo_promedio = sum(intervalos) / len(intervalos)
            print_info(f"{animal.display_id}: Intervalo promedio = {intervalo_promedio:.2f} segundos")

def main():
    """Función principal"""
    print(f"\n{ColorOutput.BOLD}{ColorOutput.MAGENTA}")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║           DIAGNÓSTICO EN TIEMPO REAL DEL SIMULADOR                        ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")
    print(f"{ColorOutput.END}")
    
    try:
        # 1. Verificar si el simulador está corriendo
        simulador_activo = verificar_simulador_corriendo()
        
        # 2. Verificar coherencia de datos
        verificar_datos_coherentes()
        
        # 3. Verificar alertas
        verificar_alertas()
        
        # 4. Verificar intervalos
        verificar_intervalos()
        
        # Resumen final
        print_header("RESUMEN FINAL")
        
        if simulador_activo:
            print_success("✓ El simulador está FUNCIONANDO correctamente")
        else:
            print_error("✗ El simulador NO está funcionando")
            print_info("  Ejecuta el simulador con: python manage.py simulate_collars_v8")
        
        print(f"\n{ColorOutput.BOLD}{ColorOutput.MAGENTA}{'='*80}{ColorOutput.END}\n")
        
    except Exception as e:
        print_error(f"Error durante el diagnóstico: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
