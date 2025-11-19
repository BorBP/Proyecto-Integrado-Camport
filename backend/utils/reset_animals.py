import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Telemetria
from shapely.geometry import Polygon

print("🔄 Reiniciando posiciones de animales al centroide de sus geocercas...\n")

animals = Animal.objects.all()

for animal in animals:
    if animal.geocerca and animal.geocerca.coordenadas:
        # Eliminar telemetría existente
        deleted_count = animal.telemetria.all().delete()[0]
        
        # Crear polígono y calcular centroide
        coords = animal.geocerca.coordenadas
        polygon = Polygon([(c['lng'], c['lat']) for c in coords])
        centroid = polygon.centroid
        
        # Crear nueva telemetría en el centroide
        Telemetria.objects.create(
            animal=animal,
            latitud=centroid.y,
            longitud=centroid.x,
            temperatura_corporal=38.5,
            frecuencia_cardiaca=70
        )
        
        print(f'✓ {animal.display_id or animal.collar_id}: Reiniciado en centroide de "{animal.geocerca.nombre}"')
        print(f'  Telemetría eliminada: {deleted_count} registros')
        print(f'  Nueva posición: ({centroid.y:.6f}, {centroid.x:.6f})\n')
    else:
        print(f'⚠ {animal.collar_id}: Sin geocerca asignada - se omite\n')

print("✅ Reinicio completado!")
