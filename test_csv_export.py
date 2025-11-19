#!/usr/bin/env python
"""
Script de prueba para verificar la exportación CSV
"""
import sys
import os

# Agregar el directorio backend al path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')

import django
django.setup()

from api.models import Reporte, Alerta, Animal, User
from django.utils import timezone
import csv
import io

def test_csv_generation():
    """Prueba la generación de CSV con datos de ejemplo"""
    print("=" * 80)
    print("PRUEBA DE EXPORTACIÓN CSV")
    print("=" * 80)
    
    # Obtener reportes
    reportes = Reporte.objects.all().select_related('alerta', 'alerta__animal', 'generado_por')
    print(f"\n✓ Total de reportes en BD: {reportes.count()}")
    
    if reportes.count() == 0:
        print("⚠️  No hay reportes para exportar. Creando datos de ejemplo...")
        # Aquí podrías crear datos de ejemplo si lo necesitas
        return
    
    # Crear CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Encabezados
    writer.writerow([
        'ID Reporte',
        'Collar ID',
        'Display ID',
        'Tipo Animal',
        'Tipo Alerta',
        'Mensaje',
        'Valor Registrado',
        'Fecha Alerta',
        'Fecha Resolución',
        'Fecha Generación',
        'Generado Por',
        'Observaciones',
        'Exportado'
    ])
    
    # Datos
    for reporte in reportes[:5]:  # Solo mostrar primeros 5
        writer.writerow([
            reporte.id,
            reporte.alerta.animal.collar_id,
            reporte.alerta.animal.display_id or '',
            reporte.alerta.animal.tipo_animal,
            reporte.alerta.tipo_alerta,
            reporte.alerta.mensaje,
            reporte.alerta.valor_registrado if reporte.alerta.valor_registrado else '',
            reporte.alerta.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            reporte.alerta.fecha_resolucion.strftime('%Y-%m-%d %H:%M:%S') if reporte.alerta.fecha_resolucion else '',
            reporte.fecha_generacion.strftime('%Y-%m-%d %H:%M:%S'),
            reporte.generado_por.username if reporte.generado_por else '',
            reporte.observaciones or '',
            'Sí' if reporte.exportado else 'No'
        ])
    
    # Mostrar resultado
    output.seek(0)
    csv_content = output.getvalue()
    
    print("\n" + "=" * 80)
    print("CONTENIDO CSV GENERADO (primeros 5 registros):")
    print("=" * 80)
    print(csv_content)
    
    # Verificar estructura
    lines = csv_content.split('\n')
    print("\n" + "=" * 80)
    print("ESTADÍSTICAS:")
    print("=" * 80)
    print(f"✓ Líneas totales: {len(lines) - 1}")  # -1 por línea vacía al final
    print(f"✓ Registros de datos: {len(lines) - 2}")  # -2 por encabezado y línea vacía
    print(f"✓ Columnas: {len(lines[0].split(','))}")
    
    print("\n" + "=" * 80)
    print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 80)

if __name__ == '__main__':
    try:
        test_csv_generation()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
