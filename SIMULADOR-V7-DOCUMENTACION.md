# 🐑 CAMPORT V7.0 - MOTOR DE SIMULACIÓN REFACTORIZADO

**Versión:** 7.0 - Random Walk Natural & Oveja Negra  
**Estado:** ✅ Production Ready  
**Fecha:** Noviembre 2025

---

## 📋 REQUERIMIENTOS IMPLEMENTADOS

### ✅ 1. Random Walk Puro
- **Eliminada** la gravedad de centroide de V6.0
- Movimiento **100% aleatorio** en todas direcciones
- Sin tendencia al centro de la geocerca
- Algoritmo de **bouncing physics** en los bordes

### ✅ 2. La Oveja Negra
- **Un animal específico** con comportamiento diferente
- Tendencia algorítmica a **intentar escapar**
- Probabilidad configurable de escape (default: 15%)
- El resto de animales **respetan siempre los límites**

### ✅ 3. Abstracción de Geocerca
- **Sin hardcodeo** de ubicaciones específicas
- Compatible con **cualquier geocerca del mundo**
- Acepta objeto Geocerca con coordenadas dinámicas
- Sistema de coordenadas completamente abstracto

### ✅ 4. Adaptabilidad Dinámica
- **Recálculo automático** al cambiar de geocerca
- Si animal cambia de Geocerca A → Geocerca B:
  - Coordenadas se recalculan inmediatamente
  - Posicionamiento seguro dentro de nueva geocerca
  - Verificación en cada ciclo

### ✅ 5. Sistema de Placeholder
- Animales **sin geocerca asignada**:
  - Aparecen estáticamente en primera geocerca disponible
  - Marcados como "PLACEHOLDER" en logs
  - Posición fija hasta asignación real

---

## 🎮 USO DEL SIMULADOR

### Inicio Rápido

```powershell
# Opción 1: Script automático
.\start-simulator-v7.ps1

# Opción 2: Manual
cd backend
.\venv\Scripts\Activate.ps1
python manage.py simulate_collars_v7
```

### Parámetros Disponibles

```bash
# Intervalo de actualización (segundos)
python manage.py simulate_collars_v7 --interval 20

# Rango de movimiento (grados)
python manage.py simulate_collars_v7 --movement-range 0.0003

# Designar oveja negra específica
python manage.py simulate_collars_v7 --black-sheep OVINO-001

# Probabilidad de escape (0.0 a 1.0)
python manage.py simulate_collars_v7 --escape-probability 0.15

# Combinación de parámetros
python manage.py simulate_collars_v7 --interval 15 --black-sheep BOVINO-002 --escape-probability 0.2
```

---

## 🔬 ALGORITMOS IMPLEMENTADOS

### 1. Random Walk Movement (Animales Normales)

```python
def random_walk_movement(self, lat, lng, polygon, movement_range):
    """
    Movimiento errático sin tendencia al centro.
    
    Características:
    - Delta aleatorio en lat/lng: [-range, +range]
    - Bouncing physics si sale de límites
    - Sin atracción gravitatoria
    """
    delta_lat = random.uniform(-movement_range, movement_range)
    delta_lng = random.uniform(-movement_range, movement_range)
    
    nueva_pos = (lat + delta_lat, lng + delta_lng)
    
    if dentro_de_geocerca(nueva_pos):
        return nueva_pos
    else:
        # Rebote: invertir dirección
        return (lat - delta_lat * 0.5, lng - delta_lng * 0.5)
```

### 2. Escape Movement (Oveja Negra)

```python
def escape_movement(self, lat, lng, polygon, centroid, movement_range):
    """
    Movimiento dirigido HACIA AFUERA de la geocerca.
    
    Características:
    - Vector desde centroide → posición actual
    - Amplificación 3-5x del rango normal
    - Objetivo: salir de los límites
    """
    vector = calcular_vector_escape(lat, lng, centroid)
    escape_factor = random.uniform(3, 5)
    
    delta = vector * movement_range * escape_factor
    return (lat + delta_lat, lng + delta_lng)
```

### 3. Adaptación a Cambio de Geocerca

```python
async def geofence_changed(self, collar_id, current_geofence_id):
    """
    Detecta cambio de geocerca y reposiciona animal.
    
    Flujo:
    1. Consultar última telemetría
    2. Comparar geocerca_id anterior vs actual
    3. Si cambió → get_safe_position_in_geofence()
    4. Posicionar cerca del centroide de nueva geocerca
    """
```

---

## 📊 COMPARATIVA DE VERSIONES

| Característica | V6.0 (Anterior) | V7.0 (Nueva) |
|----------------|-----------------|--------------|
| **Algoritmo** | Gravedad de Centroide | Random Walk Puro |
| **Tendencia** | Hacia el centro | Sin tendencia |
| **Oveja Negra** | Fugas temporales aleatorias | Animal específico persistente |
| **Geocerca** | Hardcodeado | Totalmente abstracto |
| **Adaptabilidad** | Manual | Automática |
| **Placeholder** | No implementado | ✅ Implementado |

---

## 🎯 COMPORTAMIENTOS OBSERVABLES

### Animales Normales
- Movimiento errático dentro de geocerca
- Rebote natural en bordes
- Nunca salen de límites
- Distribución aleatoria en el espacio

### Oveja Negra
- **Antes de escape:** Igual que animales normales
- **Durante escape:** Movimiento dirigido hacia afuera
- **Después de escape:** Continúa alejándose
- **Retorno:** 5% probabilidad por ciclo de volver

### Sistema Placeholder
- Animales sin geocerca → Primera geocerca disponible
- Posición fija (no se mueven)
- Marcador especial: 📌 PLACEHOLDER
- Al asignar geocerca → Comienzan movimiento normal

---

## 🔧 CONFIGURACIÓN RECOMENDADA

### Para Desarrollo/Testing
```bash
python manage.py simulate_collars_v7 \
  --interval 10 \
  --movement-range 0.0005 \
  --escape-probability 0.3
```
- Ciclos rápidos (10s)
- Movimiento amplio (visualización clara)
- Escapes frecuentes (testing)

### Para Producción
```bash
python manage.py simulate_collars_v7 \
  --interval 20 \
  --movement-range 0.0003 \
  --escape-probability 0.15
```
- Ciclos realistas (20s)
- Movimiento natural (0.0003° ≈ 30m)
- Escapes ocasionales (15%)

### Para Demos
```bash
python manage.py simulate_collars_v7 \
  --interval 15 \
  --black-sheep OVINO-001 \
  --escape-probability 0.25
```
- Oveja negra específica (predictible)
- Escapes más frecuentes (demo impact)

---

## 🗺️ ABSTRACCIÓN DE GEOCERCAS

El simulador V7.0 es **completamente abstracto**:

### Ejemplo: Chile
```json
{
  "nombre": "Potrero Sur",
  "coordenadas": [
    {"lat": -38.8440, "lng": -72.2946},
    {"lat": -38.8450, "lng": -72.2940},
    ...
  ]
}
```

### Ejemplo: España
```json
{
  "nombre": "Dehesa Norte",
  "coordenadas": [
    {"lat": 40.4168, "lng": -3.7038},
    {"lat": 40.4180, "lng": -3.7020},
    ...
  ]
}
```

### Ejemplo: Australia
```json
{
  "nombre": "Paddock East",
  "coordenadas": [
    {"lat": -33.8688, "lng": 151.2093},
    {"lat": -33.8700, "lng": 151.2100},
    ...
  ]
}
```

**El simulador funciona idénticamente** sin importar la ubicación geográfica.

---

## 🧪 CASOS DE USO

### Caso 1: Animal Cambia de Geocerca

**Escenario:**
1. OVINO-001 está en "Potrero Norte"
2. Usuario lo reasigna a "Potrero Sur"
3. Simulador detecta cambio

**Comportamiento:**
```
🔄 OVINO-001: Geocerca cambiada - Reposicionando...
📍 OVINO-001: OK | Geocerca: Potrero Sur
```

### Caso 2: Oveja Negra Escapa

**Escenario:**
1. BOVINO-002 es la oveja negra
2. Probabilidad 15% por ciclo
3. En ciclo #7 intenta escapar

**Comportamiento:**
```
Ciclo #6: 📍 BOVINO-002 🐑: OK
Ciclo #7: 🏃 BOVINO-002 (OVEJA NEGRA) está intentando ESCAPAR!
Ciclo #8: ⚠️  BOVINO-002 🐑⚫: FUERA
Ciclo #9: ⚠️  BOVINO-002 🐑⚫: FUERA
Ciclo #15: 🔙 BOVINO-002 (OVEJA NEGRA) ha REGRESADO
```

### Caso 3: Animal Sin Geocerca

**Escenario:**
1. EQUINO-001 no tiene geocerca asignada
2. Existe "Potrero Principal" en sistema

**Comportamiento:**
```
📌 EQUINO-001: PLACEHOLDER | Geocerca: Potrero Principal (Placeholder)
```

---

## 📈 MÉTRICAS Y LOGS

### Información por Ciclo

```
━━━ CICLO #42 ━━━
  📍 OVINO-001: OK | Temp: 38.7°C | FC: 75 lpm | Geocerca: Potrero Norte
  📍 OVINO-002: OK | Temp: 39.2°C | FC: 82 lpm | Geocerca: Potrero Norte
  ⚠️  BOVINO-001 🐑⚫: FUERA | Temp: 38.3°C | FC: 68 lpm | Geocerca: Potrero Sur
  📍 BOVINO-002: OK | Temp: 38.5°C | FC: 70 lpm | Geocerca: Potrero Sur
  📌 EQUINO-001: PLACEHOLDER | Temp: 37.8°C | FC: 35 lpm | Geocerca: Potrero Norte (Placeholder)

📊 RESUMEN:
   ✓ Exitosos: 4
   ⚠️  Fuera de límites: 1
   📌 Sin geocerca: 1

⏳ Esperando 18.3 segundos...
```

### Símbolos de Estado

| Símbolo | Significado |
|---------|-------------|
| 📍 | Animal dentro de geocerca |
| ⚠️  | Animal fuera de límites |
| 📌 | Placeholder (sin geocerca) |
| 🐑 | Oveja negra (normal) |
| 🐑⚫ | Oveja negra (escapada) |
| 🔄 | Cambio de geocerca detectado |
| 🏃 | Intento de escape |
| 🔙 | Retorno después de escape |

---

## 🛠️ INTEGRACIÓN CON BACKEND

### Modelo Animal (No Requiere Cambios)

```python
class Animal(models.Model):
    collar_id = models.CharField(max_length=50, unique=True, primary_key=True)
    tipo_animal = models.CharField(max_length=10, choices=TIPO_ANIMAL_CHOICES)
    geocerca = models.ForeignKey('Geocerca', on_delete=models.SET_NULL, null=True, blank=True)
    # ... otros campos
```

**La propiedad `geocerca` ya existe** - No se requieren migraciones.

### Consumer WebSocket (Compatible)

El simulador V7.0 envía el mismo formato de telemetría:

```json
{
  "collar_id": "OVINO-001",
  "latitud": -38.844523,
  "longitud": -72.294876,
  "temperatura_corporal": 38.7,
  "frecuencia_cardiaca": 75
}
```

**Compatible 100%** con el consumer existente.

---

## 🚀 VENTAJAS DE V7.0

### 1. Movimiento Natural
- Random Walk = comportamiento realista
- Sin patrones artificiales
- Distribución uniforme en geocerca

### 2. Oveja Negra Única
- Identificación clara del animal problemático
- Tendencia persistente (no temporal)
- Útil para demostración de alertas

### 3. Portabilidad Global
- Funciona en cualquier país
- Cualquier tamaño de geocerca
- Cualquier número de polígonos

### 4. Mantenibilidad
- Código limpio y documentado
- Parámetros configurables
- Fácil debug y extensión

### 5. Adaptabilidad
- Cambios de geocerca en tiempo real
- Sin necesidad de reinicio
- Migración suave entre zonas

---

## 📝 NOTAS TÉCNICAS

### Precisión de Coordenadas
- **6 decimales** (~0.11 metros)
- Suficiente para visualización
- Balance entre precisión y rendimiento

### Rango de Movimiento
- Default: 0.0003 grados
- Equivalente: ~30 metros por paso
- Configurable según escala de geocerca

### Frecuencia de Actualización
- Default: 20 segundos
- Recomendado: 15-30 segundos
- Menor = Mayor carga en servidor

### Bouncing Physics
- Rebote al 50% de velocidad
- Previene "pegado" a bordes
- Mantiene naturalidad del movimiento

---

## 🎓 CASOS DE ESTUDIO

### Estudio 1: Distribución Espacial

**Hipótesis:** Random Walk produce distribución uniforme  
**Método:** Ejecutar 1000 ciclos, medir densidad  
**Resultado Esperado:** Sin clustering en centro

### Estudio 2: Eficacia de Escape

**Hipótesis:** Oveja negra escapa efectivamente  
**Método:** P=0.15, medir intentos exitosos  
**Resultado Esperado:** ~15% de ciclos con escape

### Estudio 3: Adaptación a Cambio

**Hipótesis:** Reposicionamiento instantáneo  
**Método:** Cambiar geocerca durante simulación  
**Resultado Esperado:** Nuevo ciclo = nueva posición

---

## 🔮 FUTURAS MEJORAS

### V7.1 Propuesta
- [ ] Múltiples ovejas negras configurable
- [ ] Patrones de comportamiento por especie
- [ ] Zonas de atracción (agua, comida)
- [ ] Comportamiento de manada

### V7.2 Propuesta
- [ ] Machine Learning para predecir fugas
- [ ] Historial de rutas
- [ ] Análisis de patrones circadianos
- [ ] Integración con clima

---

## 📞 SOPORTE

### Verificación de Instalación

```powershell
# Verificar archivo
Get-Item backend\api\management\commands\simulate_collars_v7.py

# Probar comando
cd backend
.\venv\Scripts\Activate.ps1
python manage.py help simulate_collars_v7
```

### Troubleshooting Común

**Error: "No module named websockets"**
```bash
pip install websockets
```

**Error: "Connection refused"**
- Verificar que Django esté ejecutándose
- Verificar puerto 8000 disponible

**Error: "No such table: api_animal"**
```bash
python manage.py migrate
python populate_db.py
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

- [x] Eliminar gravedad de centroide
- [x] Implementar Random Walk puro
- [x] Implementar Oveja Negra específica
- [x] Abstracción completa de geocercas
- [x] Adaptabilidad a cambios de geocerca
- [x] Sistema de placeholder
- [x] Bouncing physics en bordes
- [x] Logs informativos
- [x] Parámetros configurables
- [x] Documentación completa

---

## 📄 LICENCIA

Proyecto educativo - CAMPORT Team 2025

---

**¡CAMPORT V7.0 - El simulador más natural y adaptable del mercado!** 🐑✨

---

**Desarrollado con ❤️ por CAMPORT Team**
**Versión:** 7.0.0  
**Última Actualización:** Noviembre 2025
**Estado:** ✅ **PRODUCTION READY**
