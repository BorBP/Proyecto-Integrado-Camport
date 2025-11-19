"""
Diagnóstico del Sistema Camport
================================
Este script verifica el estado actual del sistema sin necesidad de WebSocket
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Telemetria, Alerta, Geocerca, AlertaUsuario
from django.contrib.auth import get_user_model
User = get_user_model()

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def diagnostico_completo():
    """Realiza un diagnóstico completo del sistema"""
    
    print_section("1. VERIFICACIÓN DE USUARIOS")
    usuarios = User.objects.all()
    print(f"Total de usuarios: {usuarios.count()}")
    for user in usuarios:
        print(f"  - {user.username} ({user.email})")
    
    print_section("2. VERIFICACIÓN DE ANIMALES")
    animales = Animal.objects.all()
    print(f"Total de animales: {animales.count()}")
    for animal in animales:
        geocerca_info = f"Geocerca: {animal.geocerca.nombre}" if animal.geocerca else "❌ SIN GEOCERCA"
        print(f"  - {animal.collar_id} | {animal.display_id} | {animal.tipo_animal} | {geocerca_info}")
    
    print_section("3. VERIFICACIÓN DE GEOCERCAS")
    geocercas = Geocerca.objects.all()
    print(f"Total de geocercas: {geocercas.count()}")
    for geocerca in geocercas:
        estado = "✓ ACTIVA" if geocerca.activa else "✗ Inactiva"
        animales_en_geocerca = geocerca.animales.count()
        print(f"  - {geocerca.nombre} | {estado} | {animales_en_geocerca} animales | {len(geocerca.coordenadas)} coords")
    
    print_section("4. VERIFICACIÓN DE TELEMETRÍA")
    telemetria_total = Telemetria.objects.count()
    print(f"Total de registros de telemetría: {telemetria_total}")
    
    if telemetria_total > 0:
        print("\nÚltimos 5 registros por animal:")
        for animal in animales:
            ultimos = Telemetria.objects.filter(animal=animal).order_by('-timestamp')[:5]
            if ultimos.exists():
                ultimo = ultimos.first()
                print(f"\n  {animal.collar_id}:")
                print(f"    Último registro: {ultimo.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"    Posición: ({ultimo.latitud:.5f}, {ultimo.longitud:.5f})")
                print(f"    Temperatura: {ultimo.temperatura_corporal}°C")
                print(f"    Frecuencia: {ultimo.frecuencia_cardiaca} BPM")
                print(f"    Total de registros: {Telemetria.objects.filter(animal=animal).count()}")
    
    print_section("5. VERIFICACIÓN DE ALERTAS")
    alertas_total = Alerta.objects.count()
    alertas_pendientes = Alerta.objects.filter(resuelta=False).count()
    alertas_resueltas = Alerta.objects.filter(resuelta=True).count()
    
    print(f"Total de alertas: {alertas_total}")
    print(f"  - Pendientes: {alertas_pendientes}")
    print(f"  - Resueltas: {alertas_resueltas}")
    
    if alertas_pendientes > 0:
        print("\nAlertas pendientes recientes (últimas 10):")
        alertas = Alerta.objects.filter(resuelta=False).order_by('-timestamp')[:10]
        for alerta in alertas:
            print(f"  - [{alerta.timestamp.strftime('%H:%M:%S')}] {alerta.tipo_alerta} | "
                  f"{alerta.animal.collar_id} | {alerta.mensaje}")
    
    # Alertas por tipo
    print("\nDistribución por tipo:")
    tipos = ['TEMPERATURA', 'FRECUENCIA', 'PERIMETRO']
    for tipo in tipos:
        count = Alerta.objects.filter(tipo_alerta=tipo, resuelta=False).count()
        print(f"  - {tipo}: {count}")
    
    print_section("6. VERIFICACIÓN DE ALERTAS DE USUARIO")
    alertas_usuario_total = AlertaUsuario.objects.count()
    alertas_usuario_no_leidas = AlertaUsuario.objects.filter(leido=False).count()
    print(f"Total de alertas de usuario: {alertas_usuario_total}")
    print(f"  - No leídas: {alertas_usuario_no_leidas}")
    print(f"  - Leídas: {alertas_usuario_total - alertas_usuario_no_leidas}")
    
    print_section("7. RESUMEN Y DIAGNÓSTICO")
    
    problemas = []
    
    # Verificar animales sin geocerca
    animales_sin_geocerca = Animal.objects.filter(geocerca__isnull=True).count()
    if animales_sin_geocerca > 0:
        problemas.append(f"❌ {animales_sin_geocerca} animales SIN GEOCERCA asignada")
        print(f"⚠️  {animales_sin_geocerca} animales sin geocerca - NO generarán alertas de perímetro")
        animales_prob = Animal.objects.filter(geocerca__isnull=True)
        for animal in animales_prob:
            print(f"    - {animal.collar_id}")
    
    # Verificar geocercas inactivas
    geocercas_inactivas = Geocerca.objects.filter(activa=False).count()
    if geocercas_inactivas > 0:
        problemas.append(f"❌ {geocercas_inactivas} geocercas INACTIVAS")
    
    # Verificar si hay telemetría reciente (últimos 5 minutos)
    from django.utils import timezone
    from datetime import timedelta
    hace_5_min = timezone.now() - timedelta(minutes=5)
    telemetria_reciente = Telemetria.objects.filter(timestamp__gte=hace_5_min).count()
    
    if telemetria_reciente == 0 and telemetria_total > 0:
        problemas.append("⚠️  No hay telemetría reciente (últimos 5 minutos)")
        print("⚠️  No se ha recibido telemetría en los últimos 5 minutos")
        print("    Posibles causas:")
        print("    - El simulador no está ejecutándose")
        print("    - El WebSocket no está conectado")
    elif telemetria_reciente > 0:
        print(f"✓ Sistema ACTIVO - {telemetria_reciente} registros de telemetría en los últimos 5 minutos")
    
    if len(problemas) == 0:
        print("\n✅ ¡SISTEMA EN BUEN ESTADO!")
        print("    - Todos los animales tienen geocerca asignada")
        print("    - Las geocercas están activas")
        if telemetria_reciente > 0:
            print("    - El sistema está recibiendo telemetría")
    else:
        print("\n⚠️  PROBLEMAS DETECTADOS:")
        for problema in problemas:
            print(f"    {problema}")
    
    print_section("8. COMANDOS ÚTILES")
    print("Para iniciar el sistema completo:")
    print("  1. Backend:   cd backend && python manage.py runserver")
    print("  2. Simulador: cd backend && python simulator.py")
    print("  3. Frontend:  cd frontend && npm run dev")
    print("\nPara limpiar datos:")
    print("  - Telemetría:  python -c \"from api.models import Telemetria; Telemetria.objects.all().delete()\"")
    print("  - Alertas:     python -c \"from api.models import Alerta; Alerta.objects.all().delete()\"")

if __name__ == "__main__":
    print("\n🔍 DIAGNÓSTICO DEL SISTEMA CAMPORT")
    print("=" * 60)
    diagnostico_completo()
    print("\n")
