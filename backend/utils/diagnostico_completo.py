#!/usr/bin/env python
"""
Script de diagnóstico completo del sistema CAMPORT
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Geocerca, Alerta, Telemetria, AlertaUsuario
from django.contrib.auth import get_user_model
from shapely.geometry import Point, Polygon

User = get_user_model()

print("=" * 80)
print("DIAGNÓSTICO COMPLETO DEL SISTEMA CAMPORT")
print("=" * 80)

# 1. Usuarios
print("\n📊 USUARIOS EN EL SISTEMA:")
print("-" * 80)
usuarios = User.objects.all()
for user in usuarios:
    print(f"  👤 {user.username} - Email: {user.email} - Staff: {user.is_staff}")
print(f"  Total: {usuarios.count()} usuarios")

# 2. Geocercas
print("\n🗺️  GEOCERCAS CONFIGURADAS:")
print("-" * 80)
geocercas = Geocerca.objects.all()
for geo in geocercas:
    animales_count = Animal.objects.filter(geocerca=geo).count()
    print(f"  ID {geo.id}: {geo.nombre}")
    print(f"     - Activa: {geo.activa}")
    print(f"     - Puntos: {len(geo.coordenadas)}")
    print(f"     - Animales asignados: {animales_count}")
    print(f"     - Coordenadas:")
    for i, coord in enumerate(geo.coordenadas):
        print(f"       Punto {i+1}: Lat {coord['lat']:.6f}, Lng {coord['lng']:.6f}")
    print()
print(f"  Total: {geocercas.count()} geocercas")

# 3. Animales
print("\n🐄 ANIMALES REGISTRADOS:")
print("-" * 80)
animales = Animal.objects.all()
for animal in animales:
    geocerca_nombre = animal.geocerca.nombre if animal.geocerca else "⚠️  SIN GEOCERCA"
    ultima_telemetria = Telemetria.objects.filter(animal=animal).order_by('-timestamp').first()
    
    print(f"  {animal.display_id} ({animal.collar_id}) - {animal.tipo_animal}")
    print(f"     - Geocerca: {geocerca_nombre}")
    
    if ultima_telemetria:
        print(f"     - Última posición: Lat {ultima_telemetria.latitud:.6f}, Lng {ultima_telemetria.longitud:.6f}")
        print(f"     - Temperatura: {ultima_telemetria.temperatura_corporal}°C")
        print(f"     - Frecuencia: {ultima_telemetria.frecuencia_cardiaca} BPM")
        print(f"     - Timestamp: {ultima_telemetria.timestamp}")
        
        # Verificar si está dentro de su geocerca
        if animal.geocerca:
            coords = [(c['lng'], c['lat']) for c in animal.geocerca.coordenadas]
            polygon = Polygon(coords)
            point = Point(ultima_telemetria.longitud, ultima_telemetria.latitud)
            dentro = polygon.contains(point)
            print(f"     - Estado: {'✅ DENTRO de geocerca' if dentro else '🚨 FUERA de geocerca'}")
    else:
        print(f"     - ⚠️  Sin datos de telemetría")
    print()
print(f"  Total: {animales.count()} animales")

# 4. Alertas
print("\n🚨 ALERTAS DEL SISTEMA:")
print("-" * 80)
alertas_recientes = Alerta.objects.all().order_by('-timestamp')[:10]
for alerta in alertas_recientes:
    print(f"  [{alerta.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {alerta.tipo_alerta}")
    print(f"     - Animal: {alerta.animal.display_id} ({alerta.animal.collar_id})")
    print(f"     - Mensaje: {alerta.mensaje}")
    print(f"     - Resuelta: {'Sí' if alerta.resuelta else 'No'}")
    
    # Contar usuarios notificados
    usuarios_notificados = AlertaUsuario.objects.filter(alerta=alerta).count()
    usuarios_leidos = AlertaUsuario.objects.filter(alerta=alerta, leido=True).count()
    print(f"     - Usuarios notificados: {usuarios_notificados} ({usuarios_leidos} leídas)")
    print()

total_alertas = Alerta.objects.count()
alertas_resueltas = Alerta.objects.filter(resuelta=True).count()
alertas_pendientes = Alerta.objects.filter(resuelta=False).count()

print(f"  Total alertas: {total_alertas}")
print(f"  Resueltas: {alertas_resueltas}")
print(f"  Pendientes: {alertas_pendientes}")

# 5. Alertas por tipo
print("\n📊 DISTRIBUCIÓN DE ALERTAS POR TIPO:")
print("-" * 80)
for tipo in ['TEMPERATURA', 'FRECUENCIA', 'PERIMETRO']:
    count = Alerta.objects.filter(tipo_alerta=tipo).count()
    print(f"  {tipo}: {count} alertas")

# 6. Problemas detectados
print("\n⚠️  PROBLEMAS DETECTADOS:")
print("-" * 80)
problemas_encontrados = False

# Animales sin geocerca
animales_sin_geocerca = Animal.objects.filter(geocerca__isnull=True)
if animales_sin_geocerca.exists():
    print(f"  ❌ {animales_sin_geocerca.count()} animales SIN geocerca asignada:")
    for animal in animales_sin_geocerca:
        print(f"     - {animal.display_id} ({animal.collar_id})")
    problemas_encontrados = True

# Geocercas sin animales
for geo in geocercas:
    count = Animal.objects.filter(geocerca=geo).count()
    if count == 0:
        print(f"  ⚠️  Geocerca '{geo.nombre}' sin animales asignados")
        problemas_encontrados = True

# Animales fuera de geocerca
for animal in animales:
    if animal.geocerca:
        ultima_tel = Telemetria.objects.filter(animal=animal).order_by('-timestamp').first()
        if ultima_tel:
            coords = [(c['lng'], c['lat']) for c in animal.geocerca.coordenadas]
            polygon = Polygon(coords)
            point = Point(ultima_tel.longitud, ultima_tel.latitud)
            if not polygon.contains(point):
                print(f"  🚨 {animal.display_id} está FUERA de su geocerca '{animal.geocerca.nombre}'")
                print(f"     Posición: Lat {ultima_tel.latitud:.6f}, Lng {ultima_tel.longitud:.6f}")
                problemas_encontrados = True

if not problemas_encontrados:
    print("  ✅ No se detectaron problemas en la configuración")

print("\n" + "=" * 80)
print("DIAGNÓSTICO COMPLETADO")
print("=" * 80)
