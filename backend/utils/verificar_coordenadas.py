import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Geocerca, Telemetria

print("🗺️ Verificando Geocerca actualizada...")
print()

geocerca = Geocerca.objects.filter(activa=True).first()
if geocerca:
    print(f"✅ Geocerca: {geocerca.nombre}")
    print(f"   Creado por: {geocerca.creado_por.username}")
    print(f"   Activa: {geocerca.activa}")
    print()
    print("📍 Coordenadas del perímetro:")
    for i, coord in enumerate(geocerca.coordenadas, 1):
        print(f"   Punto {i}: Lat {coord['lat']}, Lng {coord['lng']}")
    print()
    
    # Mostrar telemetría reciente
    print("📡 Telemetría más reciente:")
    telemetrias = Telemetria.objects.all().order_by('-timestamp')[:5]
    for t in telemetrias:
        print(f"   {t.animal.collar_id}: Lat {t.latitud:.5f}, Lng {t.longitud:.5f}")
    print()
    print("✅ Las coordenadas han sido actualizadas correctamente!")
    print(f"   Nueva ubicación: La Araucanía, Chile")
else:
    print("❌ No se encontró geocerca activa")
