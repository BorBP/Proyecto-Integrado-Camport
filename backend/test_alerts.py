"""
Script de diagnóstico para verificar el sistema de alertas.
Verifica:
1. Conexión WebSocket
2. Creación de alertas en BD
3. Cooldown funcionando correctamente
4. Variación entre animales
"""

import asyncio
import websockets
import json
import django
import os
import sys

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Alerta, AlertaUsuario


async def test_alerts():
    """Prueba el sistema de alertas"""
    uri = "ws://localhost:8000/ws/telemetria/"
    
    print("="*80)
    print(" DIAGNÓSTICO DEL SISTEMA DE ALERTAS")
    print("="*80)
    
    # Verificar estado inicial de la BD
    print("\n[1] Estado Inicial de la BD:")
    print(f"  - Animales totales: {Animal.objects.count()}")
    print(f"  - Animales con geocerca: {Animal.objects.exclude(geocerca=None).count()}")
    print(f"  - Alertas existentes: {Alerta.objects.count()}")
    print(f"  - AlertasUsuario existentes: {AlertaUsuario.objects.count()}")
    
    animales = Animal.objects.select_related('geocerca').all()
    print("\n[2] Detalle de Animales:")
    for animal in animales:
        geo_nombre = animal.geocerca.nombre if animal.geocerca else "SIN GEOCERCA"
        print(f"  - {animal.display_id} ({animal.collar_id}): {geo_nombre}")
    
    try:
        print("\n[3] Conectando a WebSocket...")
        async with websockets.connect(uri) as websocket:
            print("  ✓ Conexión establecida\n")
            
            # Limpiar alertas anteriores para diagnóstico
            alertas_iniciales = Alerta.objects.count()
            
            print("[4] Enviando telemetría de prueba...")
            print("  Enviando datos con FIEBRE para OVINO-001 (si tiene geocerca)...")
            
            # Test 1: Fiebre
            telemetria_fiebre = {
                'collar_id': 'OVINO-1',  # Tiene geocerca
                'latitud': -38.8440,
                'longitud': -72.2946,
                'temperatura_corporal': 41.0,  # FIEBRE
                'frecuencia_cardiaca': 75
            }
            
            await websocket.send(json.dumps(telemetria_fiebre))
            response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            resp_data = json.loads(response)
            print(f"  → Respuesta: {resp_data}")
            
            await asyncio.sleep(2)
            
            # Verificar alerta creada
            nuevas_alertas = Alerta.objects.count() - alertas_iniciales
            print(f"\n[5] Alertas creadas: {nuevas_alertas}")
            
            if nuevas_alertas > 0:
                ultima_alerta = Alerta.objects.latest('timestamp')
                print(f"  ✓ Última alerta:")
                print(f"    - Tipo: {ultima_alerta.tipo_alerta}")
                print(f"    - Mensaje: {ultima_alerta.mensaje}")
                print(f"    - Animal: {ultima_alerta.animal.collar_id}")
                print(f"    - Timestamp: {ultima_alerta.timestamp}")
                
                # Verificar AlertaUsuario
                alertas_usuario = AlertaUsuario.objects.filter(alerta=ultima_alerta)
                print(f"  ✓ AlertasUsuario creadas: {alertas_usuario.count()}")
                for au in alertas_usuario:
                    print(f"    - Usuario: {au.usuario.username}, Leído: {au.leido}")
            else:
                print("  ❌ NO se creó ninguna alerta")
            
            # Test 2: Intentar enviar misma alerta (debe estar en cooldown)
            print("\n[6] Probando cooldown (re-enviar misma alerta)...")
            await websocket.send(json.dumps(telemetria_fiebre))
            response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            resp_data = json.loads(response)
            print(f"  → Respuesta: {resp_data}")
            
            alertas_despues = Alerta.objects.count()
            if alertas_despues == (alertas_iniciales + nuevas_alertas):
                print("  ✓ Cooldown funcionando: NO se creó alerta duplicada")
            else:
                print("  ❌ Cooldown NO funcionando: se creó alerta duplicada")
            
            # Test 3: Alerta de BPM
            print("\n[7] Probando alerta de BPM alto...")
            telemetria_bpm = {
                'collar_id': 'BOVINO-002',  # Tiene geocerca
                'latitud': -38.8445,
                'longitud': -72.2950,
                'temperatura_corporal': 38.5,
                'frecuencia_cardiaca': 125  # AGITACIÓN
            }
            
            await websocket.send(json.dumps(telemetria_bpm))
            response = await asyncio.wait_for(websocket.recv(), timeout=2.0)
            resp_data = json.loads(response)
            print(f"  → Respuesta: {resp_data}")
            
            await asyncio.sleep(1)
            
            alertas_finales = Alerta.objects.count()
            print(f"\n[8] Total de alertas en BD: {alertas_finales}")
            print(f"  - Alertas de TEMPERATURA: {Alerta.objects.filter(tipo_alerta='TEMPERATURA').count()}")
            print(f"  - Alertas de FRECUENCIA: {Alerta.objects.filter(tipo_alerta='FRECUENCIA').count()}")
            print(f"  - Alertas de PERIMETRO: {Alerta.objects.filter(tipo_alerta='PERIMETRO').count()}")
            
            print("\n[9] Últimas 5 alertas creadas:")
            ultimas = Alerta.objects.order_by('-timestamp')[:5]
            for alerta in ultimas:
                print(f"  - {alerta.timestamp.strftime('%H:%M:%S')} | {alerta.tipo_alerta:12s} | {alerta.animal.display_id:12s} | {alerta.mensaje[:50]}")
            
            print("\n" + "="*80)
            print(" DIAGNÓSTICO COMPLETADO")
            print("="*80)
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🔍 Iniciando diagnóstico del sistema de alertas...")
    print("Asegúrate de que el backend de Django esté corriendo en puerto 8000\n")
    
    try:
        asyncio.run(test_alerts())
    except KeyboardInterrupt:
        print("\n⏹️  Diagnóstico cancelado")
