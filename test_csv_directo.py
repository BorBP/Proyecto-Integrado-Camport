#!/usr/bin/env python
"""
Prueba directa de generación CSV sin pasar por HTTP
"""
import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')

import django
django.setup()

from django.test import RequestFactory
from api.views import ReporteViewSet
from api.models import User
from rest_framework.test import force_authenticate

def test_csv_endpoint():
    """Prueba directa del endpoint CSV"""
    
    print("=" * 80)
    print("PRUEBA DIRECTA DE ENDPOINT CSV")
    print("=" * 80)
    
    # Crear request factory
    factory = RequestFactory()
    
    # Crear request GET
    request = factory.get('/api/reportes/exportar_csv/')
    
    # Autenticar con usuario admin
    user = User.objects.get(username='admin')
    force_authenticate(request, user=user)
    
    # Crear vista
    view = ReporteViewSet.as_view({'get': 'exportar_csv'})
    
    # Ejecutar
    print("\n✓ Ejecutando endpoint exportar_csv...")
    response = view(request)
    
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Content-Type: {response.get('Content-Type')}")
    print(f"✓ Content-Disposition: {response.get('Content-Disposition')}")
    
    # Verificar contenido (HttpResponse ya tiene el contenido)
    content = response.content.decode('utf-8')
    lines = content.split('\n')
    
    print(f"\n✓ Tamaño del CSV: {len(content)} bytes")
    print(f"✓ Líneas: {len(lines)}")
    
    print("\n📄 CONTENIDO CSV:")
    print("-" * 80)
    for i, line in enumerate(lines[:10]):
        if line.strip():
            print(f"{i+1}: {line}")
    
    # Guardar archivo
    filename = "test_direct_export.csv"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"\n✓ Archivo guardado: {filename}")
    
    print("\n" + "=" * 80)
    print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 80)

if __name__ == '__main__':
    try:
        test_csv_endpoint()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
