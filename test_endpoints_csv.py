#!/usr/bin/env python
"""
Script para probar los endpoints de exportación CSV
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def get_token():
    """Obtener token de autenticación"""
    print_section("🔑 AUTENTICACIÓN")
    
    # Intentar login
    response = requests.post(f"{BASE_URL}/token/", json={
        "username": "admin",
        "password": "admin"
    })
    
    if response.status_code == 200:
        token = response.json()['access']
        print("✓ Autenticación exitosa")
        print(f"  Token: {token[:50]}...")
        return token
    else:
        print(f"❌ Error de autenticación: {response.status_code}")
        print(f"   {response.text}")
        return None

def test_exportar_csv(token):
    """Probar endpoint de exportación CSV completa"""
    print_section("📥 PRUEBA: Exportar CSV Completo")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/reportes/exportar_csv/", headers=headers)
        
        if response.status_code == 200:
            print("✓ Exportación exitosa")
            print(f"  Content-Type: {response.headers.get('Content-Type')}")
            print(f"  Content-Disposition: {response.headers.get('Content-Disposition')}")
            print(f"  Tamaño: {len(response.content)} bytes")
            
            # Guardar archivo
            filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  Archivo guardado: {filename}")
            
            # Mostrar preview
            print("\n📄 PREVIEW (primeras 5 líneas):")
            lines = response.text.split('\n')[:5]
            for i, line in enumerate(lines):
                print(f"  {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def test_exportar_csv_filtrado(token):
    """Probar endpoint de exportación CSV filtrada"""
    print_section("📥 PRUEBA: Exportar CSV Filtrado")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Filtro: solo alertas de temperatura
    filtros = {
        "tipo_alerta": "TEMPERATURA"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/reportes/exportar_csv_filtrado/",
            headers=headers,
            json=filtros
        )
        
        if response.status_code == 200:
            print("✓ Exportación filtrada exitosa")
            print(f"  Filtro aplicado: {filtros}")
            print(f"  Content-Type: {response.headers.get('Content-Type')}")
            print(f"  Tamaño: {len(response.content)} bytes")
            
            # Guardar archivo
            filename = f"test_export_filtrado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  Archivo guardado: {filename}")
            
            # Mostrar preview
            print("\n📄 PREVIEW (primeras 5 líneas):")
            lines = response.text.split('\n')[:5]
            for i, line in enumerate(lines):
                print(f"  {i+1}: {line[:100]}{'...' if len(line) > 100 else ''}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def test_get_reportes(token):
    """Obtener lista de reportes"""
    print_section("📊 PRUEBA: Obtener Lista de Reportes")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/reportes/", headers=headers)
        
        if response.status_code == 200:
            reportes = response.json()
            print(f"✓ Reportes obtenidos: {len(reportes)}")
            
            # Mostrar detalles de los primeros 3
            for i, reporte in enumerate(reportes[:3], 1):
                print(f"\n  Reporte #{i}:")
                print(f"    ID: {reporte['id']}")
                print(f"    Animal: {reporte['alerta_detalle']['animal_collar']}")
                print(f"    Tipo: {reporte['alerta_detalle']['tipo_alerta']}")
                print(f"    Exportado: {reporte['exportado']}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print_section("🧪 PRUEBAS DE ENDPOINTS CSV")
    print("Servidor: http://localhost:8000")
    print("Usuario: admin")
    
    # 1. Autenticación
    token = get_token()
    if not token:
        print("\n❌ No se pudo obtener token. Asegúrate de que:")
        print("  1. El servidor Django está corriendo")
        print("  2. Las credenciales son correctas")
        return
    
    # 2. Obtener reportes
    test_get_reportes(token)
    
    # 3. Exportar CSV completo
    success1 = test_exportar_csv(token)
    
    # 4. Exportar CSV filtrado
    success2 = test_exportar_csv_filtrado(token)
    
    # Resumen
    print_section("📊 RESUMEN DE PRUEBAS")
    print(f"✓ Autenticación: {'✅' if token else '❌'}")
    print(f"✓ Exportar CSV completo: {'✅' if success1 else '❌'}")
    print(f"✓ Exportar CSV filtrado: {'✅' if success2 else '❌'}")
    
    if token and success1 and success2:
        print_section("✅ TODAS LAS PRUEBAS PASARON")
    else:
        print_section("❌ ALGUNAS PRUEBAS FALLARON")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
