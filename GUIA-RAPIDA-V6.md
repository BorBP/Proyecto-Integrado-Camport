# 🚀 CAMPORT V6.0 - Guía Rápida

## 🆕 ¿Qué hay de nuevo en V6.0?

| Mejora | Descripción |
|--------|-------------|
| 🧲 **Gravedad de Centroide** | Atracción natural hacia el centro de la geocerca |
| 🌊 **Migración Automática** | Adaptación a cambios de límites de geocerca |
| 📊 **Distancia Visible** | Muestra qué tan lejos está cada animal del centro |
| ⚙️ **Factor Configurable** | Control del nivel de atracción (0%-100%) |

---

## ⚡ Inicio Rápido

### Opción 1: Script PowerShell
```powershell
.\start-simulator.ps1
```

### Opción 2: Comando Directo
```bash
cd backend
.\venv\Scripts\Activate.ps1
python manage.py simulate_collars
```

### Opción 3: Personalizado
```bash
# Gravedad normal (20%)
python manage.py simulate_collars --gravity-factor 0.2

# Gravedad fuerte (40%)
python manage.py simulate_collars --gravity-factor 0.4

# Sin gravedad (solo V5.0)
python manage.py simulate_collars --gravity-factor 0.0
```

---

## 📊 Interpretando la Salida

### Inicio del Simulador
```
=====================================================================================
🐄 CAMPORT V6.0 - GRAVEDAD DE CENTROIDE Y MIGRACIÓN NATURAL 🐄
=====================================================================================
⏱️  Intervalo: 20 segundos
🧲 Gravedad de centroide: 20% atracción  ← ¡NUEVO!
=====================================================================================
```

### Durante Operación
```
📡 CICLO #3 - Consultando estado EN VIVO del rebaño...
🐄 Rebaño detectado: 6 animales
🧲 Aplicando gravedad de centroide (20% atracción)

  🟢 [1/6] BOVINO-001: (-38.843, -72.305) en "Zona Norte" | Dist:0.0001° | T:38.8°C
  🟢 [2/6] BOVINO-002: (-38.843, -72.306) en "Zona Norte" | Dist:0.0003° | T:39.1°C
  🟢 [3/6] OVINO-001: (-38.844, -72.304) en "Zona Sur" | Dist:0.0002° | T:39.4°C
                                                            ↑
                                                    Distancia al centro
```

### Interpretación de Distancias
```
Dist:0.0000° → En el centro exacto
Dist:0.0001° → Muy cerca del centro
Dist:0.0003° → Alejándose
Dist:0.0005° → Lejos (pero con gravedad regresará)
```

---

## 🎯 Características Clave

### 1. Gravedad de Centroide

**¿Qué es?**
Una fuerza virtual que atrae a los animales hacia el centro de su geocerca.

**¿Cómo funciona?**
```
Movimiento = (80% Aleatorio) + (20% Hacia Centro)
```

**Beneficio:**
- Los animales tienden a concentrarse
- No se alejan demasiado del centro
- Comportamiento más natural

---

### 2. Migración Automática

**Escenario:** Admin expande una geocerca

**Antes (V5.0):**
```
Centro viejo: (-38.840, -72.300)
Animales: Siguen en (-38.840, -72.300)
Centro nuevo: (-38.850, -72.310)
Resultado: Animales lejos del nuevo centro
```

**Ahora (V6.0):**
```
Centro nuevo: (-38.850, -72.310)
Ciclo #1: Animales empiezan a moverse hacia nuevo centro
Ciclo #5: Mitad del camino
Ciclo #10: Llegaron al nuevo centro
Resultado: Migración automática y gradual
```

---

### 3. Factor de Gravedad Configurable

**Controla qué tan fuerte es la atracción:**

```bash
--gravity-factor 0.0   # Sin gravedad (0%)
--gravity-factor 0.1   # Gravedad sutil (10%)
--gravity-factor 0.2   # Normal (20%) ← Default
--gravity-factor 0.3   # Notable (30%)
--gravity-factor 0.5   # Fuerte (50%)
--gravity-factor 1.0   # Máxima (100%)
```

---

## 🔧 Parámetros

### --gravity-factor (Nuevo en V6.0)
**Descripción:** Nivel de atracción al centroide (0.0 a 1.0)

**Default:** 0.2 (20%)

**Ejemplos:**
```bash
# Exploración mayor, poca concentración
python manage.py simulate_collars --gravity-factor 0.1

# Balance ideal (default)
python manage.py simulate_collars --gravity-factor 0.2

# Concentración fuerte
python manage.py simulate_collars --gravity-factor 0.5
```

---

## 💡 Configuraciones Recomendadas

### Para Operación Normal
```bash
python manage.py simulate_collars --gravity-factor 0.2
```
**Uso:** Operación diaria, comportamiento realista

---

### Para Demos de Migración
```bash
python manage.py simulate_collars \
  --interval 10 \
  --gravity-factor 0.3
```
**Uso:** Mostrar cómo los animales migran cuando se cambia geocerca

---

### Para Simular Concentración (Arreo)
```bash
python manage.py simulate_collars \
  --gravity-factor 0.5 \
  --movement-range 0.0001
```
**Uso:** Simular agrupación de ganado

---

### Sin Gravedad (Comportamiento V5.0)
```bash
python manage.py simulate_collars --gravity-factor 0.0
```
**Uso:** Movimiento puramente aleatorio

---

## 🎬 Caso de Uso: Demo de Migración

**Preparación:**
1. Iniciar simulador con gravedad normal
2. Esperar 2-3 ciclos para que animales se dispersen un poco
3. En Panel Admin, expandir geocerca
4. Observar migración gradual

**Configuración:**
```bash
python manage.py simulate_collars \
  --interval 10 \
  --gravity-factor 0.25
```

**Durante demo:**
1. Mostrar animales dispersos en mapa
2. Expandir geocerca desde admin
3. Ver en logs cómo las distancias cambian
4. Ver en mapa cómo migran hacia nuevo centro
5. En ~5-10 ciclos, estarán en nuevo centro

---

## 📊 Observando la Gravedad

### En Logs del Simulador
```
Ciclo #1:
  BOVINO-001: Dist:0.0001°
  BOVINO-002: Dist:0.0002°

Ciclo #2:
  BOVINO-001: Dist:0.0003°  ← Alejándose
  BOVINO-002: Dist:0.0001°  ← Acercándose

Ciclo #3:
  BOVINO-001: Dist:0.0002°  ← Regresando (gravedad)
  BOVINO-002: Dist:0.0002°  ← Estable
```

### En el Mapa (Frontend)
- Animales se mueven alrededor del centro
- No se concentran en un solo punto
- Mantienen distribución natural
- Pero siempre cerca del centro

---

## 🐛 Solución de Problemas

### ❌ "Animales muy dispersos"

**Síntoma:** Animales en todos los rincones de la geocerca

**Solución:**
```bash
# Aumentar gravedad
python manage.py simulate_collars --gravity-factor 0.4
```

---

### ❌ "Animales muy concentrados"

**Síntoma:** Todos en el mismo punto

**Solución:**
```bash
# Reducir gravedad
python manage.py simulate_collars --gravity-factor 0.1

# O aumentar movimiento
python manage.py simulate_collars \
  --gravity-factor 0.2 \
  --movement-range 0.0003
```

---

### ❌ "No veo efecto de gravedad"

**Verificar:**
```bash
# Asegurarse de que gravity-factor > 0
python manage.py simulate_collars --gravity-factor 0.2

# Ver en logs:
🧲 Gravedad de centroide: 20% atracción  ← Debe aparecer
```

---

## ✅ Checklist de Testing

Verificar que funciona:
- [ ] Logs muestran "Gravedad de centroide: X%"
- [ ] Cada animal tiene "Dist:X.XXXX°"
- [ ] Distancias fluctúan naturalmente
- [ ] Al cambiar geocerca, animales migran
- [ ] Con gravity-factor 0.5, se concentran rápido
- [ ] Con gravity-factor 0.0, se comporta como V5.0

---

## 🎓 Tips y Trucos

### Tip 1: Gravedad por Tipo de Operación
```bash
# Pastoreo libre
--gravity-factor 0.15

# Pastoreo normal
--gravity-factor 0.20

# Concentración moderada
--gravity-factor 0.30

# Arreo/Agrupación
--gravity-factor 0.50
```

### Tip 2: Combinar con Otros Parámetros
```bash
# Demo perfecta
python manage.py simulate_collars \
  --interval 10 \
  --gravity-factor 0.25 \
  --escape-interval 45 \
  --movement-range 0.00025
```

### Tip 3: Ver Efecto de Migración
```bash
# Iniciar con gravedad normal
python manage.py simulate_collars --gravity-factor 0.2

# Durante ejecución, ir a Admin y modificar vértices de geocerca
# Ver en logs cómo cambian las distancias
```

### Tip 4: Gravedad Extrema (Solo Testing)
```bash
# Máxima gravedad - movimiento directo al centro
python manage.py simulate_collars --gravity-factor 1.0

# Sin gravedad - solo rebotes
python manage.py simulate_collars --gravity-factor 0.0
```

---

## 📞 Comandos de Referencia Rápida

```bash
# Default (gravedad 20%)
python manage.py simulate_collars

# Gravedad personalizada
python manage.py simulate_collars --gravity-factor 0.3

# Ver ayuda completa
python manage.py help simulate_collars

# Script PowerShell
.\start-simulator.ps1

# Detener
Ctrl + C
```

---

## 🔗 Documentación Relacionada

- **CAMBIOS-V6.md** - Documentación técnica completa
- **CAMBIOS-V5.md** - Contexto de fugas aleatorias
- **CAMBIOS-V4.md** - Contexto de rebaño completo
- **HISTORIAL-VERSIONES.md** - Evolución V1→V6

---

**Versión:** CAMPORT V6.0  
**Última Actualización:** 11 de Noviembre, 2025  
**Estado:** ✅ Producción

---

¡Disfruta de la migración natural con V6.0! 🐄🧲🌊🚀
