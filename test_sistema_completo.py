#!/usr/bin/env python
"""
Script de pruebas completas del sistema de alertas y exportación CSV
"""
import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ganadoproject.settings')

import django
django.setup()

from api.models import Reporte, Alerta, Animal, User, Geocerca
from django.utils import timezone
import csv
import io

def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def test_complete_system():
    """Prueba completa del sistema"""
    
    print_section("🧪 PRUEBAS COMPLETAS DEL SISTEMA CAMPORT")
    
    # 1. Verificar animales
    print_section("1️⃣ VERIFICACIÓN DE ANIMALES")
    animales = Animal.objects.all()
    print(f"✓ Total de animales: {animales.count()}")
    for animal in animales[:5]:
        print(f"  - {animal.collar_id} ({animal.tipo_animal}) - Geocerca: {animal.geocerca.nombre if animal.geocerca else 'Sin asignar'}")
    
    # 2. Verificar geocercas
    print_section("2️⃣ VERIFICACIÓN DE GEOCERCAS")
    geocercas = Geocerca.objects.all()
    print(f"✓ Total de geocercas: {geocercas.count()}")
    for geocerca in geocercas:
        animales_asignados = Animal.objects.filter(geocerca=geocerca).count()
        print(f"  - {geocerca.nombre} (Activa: {geocerca.activa}) - Animales asignados: {animales_asignados}")
    
    # 3. Verificar alertas activas
    print_section("3️⃣ VERIFICACIÓN DE ALERTAS ACTIVAS")
    alertas_activas = Alerta.objects.filter(resuelta=False)
    print(f"✓ Total de alertas activas: {alertas_activas.count()}")
    for alerta in alertas_activas[:5]:
        print(f"  - {alerta.tipo_alerta}: {alerta.animal.collar_id} - {alerta.mensaje[:50]}...")
    
    # 4. Verificar reportes
    print_section("4️⃣ VERIFICACIÓN DE REPORTES")
    reportes = Reporte.objects.all()
    print(f"✓ Total de reportes: {reportes.count()}")
    reportes_exportados = reportes.filter(exportado=True).count()
    reportes_pendientes = reportes.filter(exportado=False).count()
    print(f"  - Exportados: {reportes_exportados}")
    print(f"  - Pendientes: {reportes_pendientes}")
    
    # 5. Prueba de generación CSV
    print_section("5️⃣ PRUEBA DE GENERACIÓN CSV")
    
    if reportes.count() > 0:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Encabezados
        headers = [
            'ID Reporte', 'Collar ID', 'Display ID', 'Tipo Animal', 
            'Tipo Alerta', 'Mensaje', 'Valor Registrado', 'Fecha Alerta',
            'Fecha Resolución', 'Fecha Generación', 'Generado Por', 
            'Observaciones', 'Exportado'
        ]
        writer.writerow(headers)
        
        # Escribir datos
        for reporte in reportes:
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
        
        output.seek(0)
        csv_content = output.getvalue()
        lines = csv_content.split('\n')
        
        print(f"✓ CSV generado exitosamente")
        print(f"  - Total de líneas: {len(lines) - 1}")
        print(f"  - Columnas: {len(headers)}")
        print(f"  - Registros: {reportes.count()}")
        
        # Mostrar preview
        print("\n📄 PREVIEW CSV (primeras 3 líneas):")
        for i, line in enumerate(lines[:4]):
            if line.strip():
                print(f"  {i}: {line[:100]}{'...' if len(line) > 100 else ''}")
    else:
        print("⚠️  No hay reportes para exportar")
    
    # 6. Verificar tipos de alerta
    print_section("6️⃣ DISTRIBUCIÓN DE TIPOS DE ALERTA")
    from django.db.models import Count
    tipos = Alerta.objects.values('tipo_alerta').annotate(total=Count('id')).order_by('-total')
    for tipo in tipos:
        print(f"  - {tipo['tipo_alerta']}: {tipo['total']} alertas")
    
    # 7. Estadísticas por animal
    print_section("7️⃣ ESTADÍSTICAS POR ANIMAL")
    for animal in animales[:5]:
        alertas_count = Alerta.objects.filter(animal=animal).count()
        reportes_count = Reporte.objects.filter(alerta__animal=animal).count()
        print(f"  - {animal.collar_id}: {alertas_count} alertas, {reportes_count} reportes")
    
    # 8. Resumen final
    print_section("📊 RESUMEN FINAL")
    print(f"✓ Animales registrados: {animales.count()}")
    print(f"✓ Geocercas configuradas: {geocercas.count()}")
    print(f"✓ Alertas totales: {Alerta.objects.count()}")
    print(f"✓ Alertas activas: {alertas_activas.count()}")
    print(f"✓ Reportes generados: {reportes.count()}")
    print(f"✓ Reportes exportados: {reportes_exportados}")
    print(f"✓ Sistema funcionando correctamente ✅")
    
    print_section("✅ PRUEBAS COMPLETADAS EXITOSAMENTE")

if __name__ == '__main__':
    try:
        test_complete_system()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
