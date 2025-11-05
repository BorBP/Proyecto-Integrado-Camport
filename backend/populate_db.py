import os
import django
import random
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')
django.setup()

from api.models import User, Animal, Geocerca, Telemetria

def create_users():
    # Crear usuario admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create(
            username='admin',
            email='admin@ganado.com',
            RUT='12345678-9',
            domicilio='Calle Principal 123',
            sexo='M',
            fecha_nacimiento=datetime(1985, 5, 15).date(),
            is_staff=True,
            is_superuser=True
        )
        admin.set_password('admin123')
        admin.save()
        print(f'✓ Usuario admin creado')
    
    # Crear usuario trabajador
    if not User.objects.filter(username='trabajador').exists():
        trabajador = User.objects.create(
            username='trabajador',
            email='trabajador@ganado.com',
            RUT='98765432-1',
            domicilio='Calle Secundaria 456',
            sexo='F',
            fecha_nacimiento=datetime(1990, 8, 20).date(),
            is_staff=False
        )
        trabajador.set_password('trabajador123')
        trabajador.save()
        print(f'✓ Usuario trabajador creado')

def create_geocerca():
    # Eliminar geocercas existentes para actualizarlas
    Geocerca.objects.all().delete()
    
    admin = User.objects.get(username='admin')
    # Geocerca en la Región de La Araucanía, Chile
    geocerca = Geocerca.objects.create(
        nombre='Perímetro Principal',
        coordenadas=[
            {'lat': -38.84233, 'lng': -72.29892},
            {'lat': -38.84733, 'lng': -72.29888},
            {'lat': -38.84746, 'lng': -72.29030},
            {'lat': -38.84148, 'lng': -72.29019},
        ],
        creado_por=admin,
        activa=True
    )
    print(f'✓ Geocerca creada con nuevas coordenadas')

def create_animals():
    admin = User.objects.get(username='admin')
    
    animales_data = [
        {'collar_id': 'OVINO-001', 'tipo_animal': 'OVINO', 'raza': 'Suffolk', 'edad': 2, 'peso_kg': 65.5, 'sexo': 'H', 'color': 'Blanco'},
        {'collar_id': 'OVINO-002', 'tipo_animal': 'OVINO', 'raza': 'Merino', 'edad': 3, 'peso_kg': 70.2, 'sexo': 'M', 'color': 'Blanco'},
        {'collar_id': 'BOVINO-001', 'tipo_animal': 'BOVINO', 'raza': 'Angus', 'edad': 4, 'peso_kg': 450.0, 'sexo': 'H', 'color': 'Negro'},
        {'collar_id': 'BOVINO-002', 'tipo_animal': 'BOVINO', 'raza': 'Hereford', 'edad': 3, 'peso_kg': 420.5, 'sexo': 'M', 'color': 'Marrón'},
        {'collar_id': 'EQUINO-001', 'tipo_animal': 'EQUINO', 'raza': 'Criollo', 'edad': 5, 'peso_kg': 380.0, 'sexo': 'M', 'color': 'Café'},
    ]
    
    # Centro de la nueva geocerca: aproximadamente -38.8444, -72.2946
    centro_lat = -38.8444
    centro_lng = -72.2946
    
    for animal_data in animales_data:
        if not Animal.objects.filter(collar_id=animal_data['collar_id']).exists():
            animal = Animal.objects.create(**animal_data, agregado_por=admin)
            print(f'✓ Animal {animal.collar_id} creado')
            
            # Crear telemetría inicial para cada animal (dentro del nuevo perímetro)
            for i in range(5):
                Telemetria.objects.create(
                    animal=animal,
                    latitud=centro_lat + random.uniform(-0.002, 0.002),
                    longitud=centro_lng + random.uniform(-0.003, 0.003),
                    temperatura_corporal=random.uniform(38.0, 39.5),
                    frecuencia_cardiaca=random.randint(60, 100)
                )
            print(f'✓ Telemetría inicial creada para {animal.collar_id}')

if __name__ == '__main__':
    print('Poblando base de datos...')
    create_users()
    create_geocerca()
    create_animals()
    print('\n✅ Base de datos poblada exitosamente!')
    print('\nCredenciales de acceso:')
    print('Admin: username=admin, password=admin123')
    print('Trabajador: username=trabajador, password=trabajador123')
