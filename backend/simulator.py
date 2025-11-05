import asyncio
import websockets
import json
import random
from datetime import datetime

# Lista de animales a simular (La Araucanía, Chile)
ANIMALES = [
    {'collar_id': 'OVINO-001', 'tipo_animal': 'OVINO', 'lat_base': -38.8440, 'lng_base': -72.2946},
    {'collar_id': 'OVINO-002', 'tipo_animal': 'OVINO', 'lat_base': -38.8445, 'lng_base': -72.2950},
    {'collar_id': 'BOVINO-001', 'tipo_animal': 'BOVINO', 'lat_base': -38.8450, 'lng_base': -72.2955},
    {'collar_id': 'BOVINO-002', 'tipo_animal': 'BOVINO', 'lat_base': -38.8442, 'lng_base': -72.2940},
    {'collar_id': 'EQUINO-001', 'tipo_animal': 'EQUINO', 'lat_base': -38.8448, 'lng_base': -72.2935},
]

async def simulate_telemetry():
    uri = "ws://localhost:8000/ws/telemetria/"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"✓ Conectado al servidor WebSocket")
            
            while True:
                # Simular datos para cada animal
                for animal in ANIMALES:
                    # Generar datos aleatorios dentro de rangos normales
                    telemetria = {
                        'collar_id': animal['collar_id'],
                        'latitud': animal['lat_base'] + random.uniform(-0.003, 0.003),
                        'longitud': animal['lng_base'] + random.uniform(-0.003, 0.003),
                        'temperatura_corporal': round(random.uniform(38.0, 39.5), 2),
                        'frecuencia_cardiaca': random.randint(60, 100)
                    }
                    
                    # Enviar datos
                    await websocket.send(json.dumps(telemetria))
                    print(f"📡 Enviado: {animal['collar_id']} - Temp: {telemetria['temperatura_corporal']}°C, FC: {telemetria['frecuencia_cardiaca']} lpm")
                    
                    # Recibir respuesta
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                        data = json.loads(response)
                        if 'alertas' in data and data['alertas']:
                            print(f"⚠️  ALERTAS: {data['alertas']}")
                    except asyncio.TimeoutError:
                        pass
                    
                    # Esperar un poco entre animales
                    await asyncio.sleep(1)
                
                # Esperar antes del siguiente ciclo
                print(f"\n⏳ Esperando 5 segundos para el próximo ciclo...\n")
                await asyncio.sleep(5)
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando simulador de telemetría...")
    print("Presiona Ctrl+C para detener\n")
    asyncio.run(simulate_telemetry())
