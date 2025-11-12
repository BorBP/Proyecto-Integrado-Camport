import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import Animal, Geocerca
from shapely.geometry import Polygon, Point

# Obtener todos los animales
animals = Animal.objects.all()

print(f'Total animales: {animals.count()}\n')

for animal in animals:
    has_telemetria = animal.telemetria.exists()
    geocerca_name = animal.geocerca.nombre if animal.geocerca else "Sin asignar"
    
    print(f'{animal.display_id or animal.collar_id}:')
    print(f'  - Telemetría: {"Sí" if has_telemetria else "No"}')
    print(f'  - Geocerca: {geocerca_name}')
    
    if has_telemetria:
        last_t = animal.telemetria.first()
        print(f'  - Última posición: ({last_t.latitud:.6f}, {last_t.longitud:.6f})')
        
        if animal.geocerca and animal.geocerca.coordenadas:
            coords = animal.geocerca.coordenadas
            polygon = Polygon([(c['lng'], c['lat']) for c in coords])
            point = Point(last_t.longitud, last_t.latitud)
            dentro = polygon.contains(point)
            print(f'  - Dentro de geocerca: {"✓ SÍ" if dentro else "✗ NO"}')
    
    print()
