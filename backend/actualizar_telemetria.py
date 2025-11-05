import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Telemetria

print("📡 Actualizando telemetría de animales...")
print()

# Centro de la nueva geocerca
centro_lat = -38.8444
centro_lng = -72.2946

# Eliminar telemetría anterior
Telemetria.objects.all().delete()
print("✓ Telemetría anterior eliminada")

# Crear nueva telemetría para cada animal
animales = Animal.objects.all()
for animal in animales:
    for i in range(5):
        Telemetria.objects.create(
            animal=animal,
            latitud=centro_lat + random.uniform(-0.002, 0.002),
            longitud=centro_lng + random.uniform(-0.003, 0.003),
            temperatura_corporal=random.uniform(38.0, 39.5),
            frecuencia_cardiaca=random.randint(60, 100)
        )
    print(f"✓ Telemetría actualizada para {animal.collar_id}")

print()
print("✅ Telemetría actualizada con nuevas coordenadas!")
print(f"   Ubicación: La Araucanía, Chile")
print(f"   Centro: Lat {centro_lat}, Lng {centro_lng}")
