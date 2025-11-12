# 🎯 CAMPORT V3.0 - Actualización del Simulador con Pastoreo Virtual

## 📋 Resumen Ejecutivo

**Sistema:** CAMPORT (Sistema de Monitoreo de Ganado en Tiempo Real)
**Versión:** 3.0.0
**Fecha de Actualización:** 11 de Noviembre, 2025
**Estado:** ✅ **COMPLETADO Y FUNCIONAL**

---

## 🚀 Cambios Principales

### Antes (V2.0)
- ❌ Simulación con movimiento aleatorio simple ("random walk")
- ❌ Animales escapaban frecuentemente de la geocerca
- ❌ Alertas de perímetro constantes e innecesarias
- ❌ Sin inicialización inteligente de posiciones

### Ahora (V3.0)
- ✅ **Inicialización en el centroide** de la geocerca asignada
- ✅ **Algoritmo de "Pastoreo Virtual"** que mantiene animales dentro
- ✅ **Corrección automática de límites** cuando se acercan al borde
- ✅ **Movimiento realista** con comportamiento natural
- ✅ **Alertas de perímetro raras** solo en emergencias simuladas

---

## 🎯 Funcionalidades Implementadas

### 1. Inicialización en el Centroide

**Comportamiento:**
- Al iniciar el simulador, verifica cada animal
- Si NO tiene telemetría previa Y tiene geocerca asignada:
  - Calcula el centroide del polígono de la geocerca
  - Crea el primer registro de telemetría en esa posición
  - Asigna signos vitales base según el tipo de animal

**Código clave:**
```python
def initialize_animals_at_centroids(self):
    for animal in animals:
        if not animal.telemetria.exists():
            if animal.geocerca and animal.geocerca.coordenadas:
                # Crear polígono y calcular centroide
                polygon = Polygon([(c['lng'], c['lat']) for c in coords])
                centroid = polygon.centroid
                
                # Crear telemetría inicial
                Telemetria.objects.create(
                    animal=animal,
                    latitud=centroid.y,
                    longitud=centroid.x,
                    temperatura_corporal=vital_signs['temperatura'],
                    frecuencia_cardiaca=vital_signs['frecuencia']
                )
```

---

### 2. Algoritmo de Pastoreo Virtual

**Estrategia: Propuesta y Corrección**

#### Paso 1: Proponer Movimiento
```python
# Generar movimiento aleatorio desde posición actual
delta_lat = random.uniform(-movement_range, movement_range)
delta_lng = random.uniform(-movement_range, movement_range)

lat_propuesta = lat_actual + delta_lat
lng_propuesta = lng_actual + delta_lng
```

#### Paso 2: Verificar Límites
```python
# Crear punto y verificar si está dentro del polígono
punto_propuesto = Point(lng_propuesta, lat_propuesta)

if polygon.contains(punto_propuesto):
    # ✓ Movimiento válido - permanece dentro
    return lat_propuesta, lng_propuesta
```

#### Paso 3: Corrección (si sale)
```python
else:
    # ✗ Movimiento inválido - corregir hacia el centroide
    
    # Calcular vector desde posición actual hacia el centroide
    vector_lat = centroid.y - lat_actual
    vector_lng = centroid.x - lng_actual
    
    # Aplicar corrección (30% del movimiento hacia el centro)
    correction_factor = 0.3
    
    new_lat = lat_actual + (vector_lat * correction_factor * movement_range / 0.0003)
    new_lng = lng_actual + (vector_lng * correction_factor * movement_range / 0.0003)
    
    return new_lat, new_lng
```

**Resultado:**
- Animales se mueven libremente DENTRO de la geocerca
- Al acercarse al borde, son "empujados" suavemente hacia el centro
- Comportamiento natural de pastoreo contenido

---

## 📁 Archivos Creados/Modificados

### Archivos Nuevos (3)
1. ✅ `backend/api/management/__init__.py`
2. ✅ `backend/api/management/commands/__init__.py`
3. ✅ `backend/api/management/commands/simulate_collars.py` (PRINCIPAL)

### Scripts Auxiliares (3)
1. ✅ `backend/check_animals.py` - Verificar estado de animales
2. ✅ `backend/reset_animals.py` - Reiniciar posiciones al centroide
3. ✅ `backend/CAMBIOS-V3.md` - Este documento

---

## 🔧 Uso del Simulador

### Comandos Disponibles

#### Ejecutar Simulador Normal
```bash
cd backend
.\venv\Scripts\Activate.ps1
python manage.py simulate_collars
```

#### Con Parámetros Personalizados
```bash
# Intervalo de 2 segundos
python manage.py simulate_collars --interval 2

# Rango de movimiento más amplio
python manage.py simulate_collars --movement-range 0.0005

# Combinado
python manage.py simulate_collars --interval 2 --movement-range 0.0005
```

#### Ver Ayuda
```bash
python manage.py help simulate_collars
```

---

## 📊 Parámetros del Simulador

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `--interval` | 5 | Intervalo entre actualizaciones (segundos) |
| `--movement-range` | 0.0003 | Rango de movimiento aleatorio (grados) |

**Ejemplos de uso:**

```bash
# Simulación rápida (1 segundo)
python manage.py simulate_collars --interval 1

# Movimiento más amplio
python manage.py simulate_collars --movement-range 0.0008

# Simulación lenta y precisa
python manage.py simulate_collars --interval 10 --movement-range 0.0001
```

---

## 🧪 Verificación y Testing

### Script: check_animals.py

**Uso:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python check_animals.py
```

**Salida esperada:**
```
Total animales: 6

OVINO-001:
  - Telemetría: Sí
  - Geocerca: Perímetro Principal
  - Última posición: (-38.843223, -72.305359)
  - Dentro de geocerca: ✓ SÍ

BOVINO-001:
  - Telemetría: Sí
  - Geocerca: Perímetro Principal
  - Última posición: (-38.843223, -72.305359)
  - Dentro de geocerca: ✓ SÍ
...
```

---

### Script: reset_animals.py

**Propósito:** Reiniciar todos los animales al centroide de sus geocercas

**Uso:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python reset_animals.py
```

**Cuándo usar:**
- Después de cambios en coordenadas de geocercas
- Cuando animales están fuera de límites
- Para resetear la simulación desde cero
- Al cambiar geocercas asignadas

**Salida esperada:**
```
🔄 Reiniciando posiciones de animales al centroide de sus geocercas...

✓ OVINO-001: Reiniciado en centroide de "Perímetro Principal"
  Telemetría eliminada: 867 registros
  Nueva posición: (-38.843223, -72.305359)

✅ Reinicio completado!
```

---

## 📈 Resultados de la Simulación

### Observaciones de Testing

**Prueba 1: Inicialización**
```
🚀 Iniciando simulador de collares GPS v3.0
⏱️  Intervalo: 3 segundos
📏 Rango de movimiento: 0.0003 grados

📍 Fase de Inicialización...
  ✓ BOVINO-003 inicializado en centroide de "Perímetro Principal"

✅ 1 animal(es) inicializado(s) en sus centroides
```

**Prueba 2: Movimiento Sin Alertas**
```
🐄 Iniciando simulación de movimiento...

🟢 BOVINO-001: (-38.843394, -72.305238) Temp: 38.6°C FC: 71 lpm
🟢 BOVINO-002: (-38.843395, -72.305121) Temp: 38.4°C FC: 66 lpm
🟢 BOVINO-003: (-38.843112, -72.305534) Temp: 38.4°C FC: 70 lpm
🟢 EQUINO-001: (-38.843240, -72.305290) Temp: 38.5°C FC: 72 lpm
🟢 OVINO-001: (-38.843333, -72.305159) Temp: 38.3°C FC: 69 lpm
🟢 OVINO-002: (-38.843211, -72.305368) Temp: 38.5°C FC: 75 lpm
```

**Resultado:** ✅ **CERO alertas de perímetro** durante la simulación normal

---

## 🎓 Detalles Técnicos

### Signos Vitales Base por Tipo de Animal

```python
vital_ranges = {
    'OVINO': {
        'temperatura': (38.5, 39.5),
        'frecuencia': (70, 90)
    },
    'BOVINO': {
        'temperatura': (38.0, 39.0),
        'frecuencia': (60, 80)
    },
    'EQUINO': {
        'temperatura': (37.5, 38.5),
        'frecuencia': (28, 40)
    }
}
```

### Variación de Signos Vitales

**Temperatura:**
- Variación: ±0.2°C por ciclo
- Límites: 37.0°C - 40.0°C
- Alerta fiebre: > 40.0°C
- Alerta hipotermia: < 37.5°C

**Frecuencia Cardíaca:**
- Variación: ±5 lpm por ciclo
- Límites: 40 - 120 lpm
- Alerta taquicardia: > 120 lpm
- Alerta bradicardia: < 40 lpm

---

## 🔍 Algoritmo de Corrección Detallado

### Factor de Corrección

```python
correction_factor = 0.3  # 30% del vector hacia el centroide
```

**Explicación:**
- Valor bajo (0.1-0.2): Corrección suave, movimiento más libre
- Valor medio (0.3-0.5): Balance entre libertad y contención
- Valor alto (0.6-0.9): Corrección fuerte, animales muy cerca del centro

### Cálculo del Vector

```python
# Vector desde posición actual al centroide
vector_lat = centroid.y - lat_actual
vector_lng = centroid.x - lng_actual

# Aplicar corrección proporcional al rango de movimiento
new_lat = lat_actual + (vector_lat * correction_factor * movement_range / 0.0003)
new_lng = lng_actual + (vector_lng * correction_factor * movement_range / 0.0003)
```

**Por qué funciona:**
- Siempre empuja hacia el centro
- Proporcional a la distancia del centroide
- Escalado con el rango de movimiento
- Previene salidas accidentales

---

## 🐛 Troubleshooting

### Problema 1: Animales fuera de geocerca

**Síntoma:**
```
🚨 ALERTA: ⚠️ Animal OVINO-001 fuera de geocerca "Perímetro Principal"
```

**Solución:**
```bash
# Reiniciar posiciones
python reset_animals.py

# Verificar
python check_animals.py
```

---

### Problema 2: Animales no se mueven

**Síntoma:** Las coordenadas no cambian entre ciclos

**Causas posibles:**
- `movement_range` muy pequeño
- Animales exactamente en el centroide
- Corrección muy fuerte

**Solución:**
```bash
# Aumentar rango de movimiento
python manage.py simulate_collars --movement-range 0.0008
```

---

### Problema 3: Demasiadas alertas de vitales

**Síntoma:** Alertas constantes de temperatura o frecuencia

**Causas posibles:**
- Valores iniciales fuera de rango
- Variación acumulativa

**Solución:**
```bash
# Reiniciar con signos vitales base
python reset_animals.py

# Ajustar límites en el código si es necesario
```

---

## 📊 Comparación de Versiones

| Aspecto | V2.0 | V3.0 |
|---------|------|------|
| **Inicialización** | Aleatoria | Centroide de geocerca |
| **Movimiento** | Random walk | Pastoreo virtual |
| **Límites** | Sin verificación | Corrección automática |
| **Alertas perímetro** | Frecuentes | Raras (solo emergencias) |
| **Realismo** | Bajo | Alto |
| **Management Command** | No existía | `simulate_collars` |
| **Signos vitales** | Aleatorios | Por tipo + variación natural |

---

## 💡 Casos de Uso

### Caso 1: Demostración del Sistema

**Objetivo:** Mostrar sistema funcionando sin alertas falsas

**Comando:**
```bash
python manage.py simulate_collars --interval 5
```

**Resultado esperado:**
- Movimiento suave y natural
- Sin alertas de perímetro
- Signos vitales estables

---

### Caso 2: Testing de Alertas

**Objetivo:** Probar sistema de alertas con eventos reales

**Paso 1:** Iniciar simulador
```bash
python manage.py simulate_collars --interval 3
```

**Paso 2:** Simular emergencia (endpoint existente)
```bash
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-001/perimetro/
```

**Resultado esperado:**
- Alerta de perímetro generada
- WebSocket envía notificación
- Frontend muestra alerta

---

### Caso 3: Pruebas de Performance

**Objetivo:** Verificar rendimiento con actualizaciones rápidas

**Comando:**
```bash
python manage.py simulate_collars --interval 1 --movement-range 0.0002
```

**Métricas a observar:**
- Uso de CPU
- Tiempos de respuesta del API
- Latencia de WebSocket

---

## 🔮 Mejoras Futuras (Fuera de V3.0)

### Algoritmos Avanzados

1. **Comportamiento de Manada**
   - Animales se agrupan naturalmente
   - Líder y seguidores
   - Distancia mínima entre individuos

2. **Patrones Circadianos**
   - Más activos durante el día
   - Descanso nocturno
   - Variación de vitales según hora

3. **Zonas Preferidas**
   - Áreas de agua
   - Zonas de sombra
   - Puntos de alimentación

4. **Memoria de Rutas**
   - Caminos frecuentes
   - Evitar áreas problemáticas
   - Rutas optimizadas

---

## 📞 Comandos Rápidos de Referencia

```bash
# Iniciar simulador normal
python manage.py simulate_collars

# Simulador rápido
python manage.py simulate_collars --interval 1

# Verificar estado
python check_animals.py

# Reiniciar posiciones
python reset_animals.py

# Ayuda
python manage.py help simulate_collars

# Detener: Ctrl+C
```

---

## ✅ Checklist de Validación

### Funcionalidades Core
- [x] Inicialización en centroide funciona
- [x] Algoritmo de pastoreo virtual implementado
- [x] Corrección de límites activa
- [x] Sin alertas falsas de perímetro
- [x] Signos vitales por tipo de animal
- [x] Variación natural de vitales
- [x] Management command registrado
- [x] Parámetros configurables

### Testing
- [x] Todos los animales dentro de geocerca
- [x] Movimiento natural observado
- [x] Scripts auxiliares funcionando
- [x] Sin errores en logs
- [x] Performance aceptable

### Documentación
- [x] README completo
- [x] Ejemplos de uso
- [x] Troubleshooting
- [x] Comandos de referencia

---

## 🎉 Conclusión

La actualización a **CAMPORT V3.0** ha sido completada exitosamente. El simulador ahora:

✅ **Inicializa inteligentemente** los animales en el centro de su geocerca
✅ **Simula pastoreo realista** manteniendo animales dentro de límites
✅ **Previene alertas falsas** de perímetro
✅ **Genera signos vitales naturales** según tipo de animal
✅ **Es altamente configurable** con parámetros de línea de comandos

**El sistema está listo para demostraciones y producción.**

---

**Fecha:** 11 de Noviembre, 2025
**Versión:** CAMPORT V3.0.0
**Estado:** ✅ **PRODUCCIÓN**

---

## 🚀 ¡Gracias por usar CAMPORT!

Sistema de Monitoreo de Ganado en Tiempo Real
Desarrollado con ❤️ para la gestión eficiente y realista del ganado
