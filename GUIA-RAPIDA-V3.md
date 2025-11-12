# 🚀 CAMPORT V3.0 - Guía Rápida

## 📋 Resumen de 30 Segundos

CAMPORT V3.0 introduce un **simulador inteligente** que mantiene a los animales dentro de sus geocercas usando un algoritmo de **pastoreo virtual**.

## 🆕 ¿Qué Hay de Nuevo?

| Característica | Descripción |
|----------------|-------------|
| 🎯 **Inicialización Centrada** | Animales inician en el centro de su geocerca |
| 🐑 **Pastoreo Virtual** | Movimiento natural que respeta límites |
| 🔄 **Auto-corrección** | Empuja animales hacia el centro al acercarse a bordes |
| 🚨 **Sin Alertas Falsas** | Perímetro solo alerta en emergencias reales |

---

## ⚡ Inicio Rápido

### Opción 1: Script PowerShell (Más Fácil)
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
# Intervalo de 2 segundos, movimiento amplio
python manage.py simulate_collars --interval 2 --movement-range 0.0005
```

---

## 🎮 Comandos Principales

### Iniciar Simulador
```bash
python manage.py simulate_collars
```

### Verificar Estado de Animales
```bash
python check_animals.py
```
**Salida:**
```
OVINO-001:
  - Telemetría: Sí
  - Geocerca: Perímetro Principal
  - Última posición: (-38.843223, -72.305359)
  - Dentro de geocerca: ✓ SÍ
```

### Reiniciar Posiciones
```bash
python reset_animals.py
```
**Cuándo usar:** Cuando animales estén fuera de límites

---

## 🔧 Parámetros Disponibles

```bash
python manage.py simulate_collars [opciones]
```

| Opción | Default | Descripción |
|--------|---------|-------------|
| `--interval` | 5 | Segundos entre actualizaciones |
| `--movement-range` | 0.0003 | Amplitud del movimiento (grados) |

**Ejemplos:**
```bash
# Simulación rápida
python manage.py simulate_collars --interval 1

# Movimiento amplio
python manage.py simulate_collars --movement-range 0.0008

# Combinado
python manage.py simulate_collars --interval 2 --movement-range 0.0005
```

---

## 📊 Interpretando la Salida

### Durante Inicialización
```
🚀 Iniciando simulador de collares GPS v3.0
⏱️  Intervalo: 5 segundos
📏 Rango de movimiento: 0.0003 grados

📍 Fase de Inicialización...
  ✓ BOVINO-003 inicializado en centroide de "Perímetro Principal"

✅ 1 animal(es) inicializado(s) en sus centroides
```

### Durante Simulación Normal (Sin Alertas)
```
🐄 Iniciando simulación de movimiento...

🟢 BOVINO-001: (-38.843394, -72.305238) Temp: 38.6°C FC: 71 lpm
🟢 OVINO-001: (-38.843333, -72.305159) Temp: 38.3°C FC: 69 lpm
```
✅ Indicador verde = Animal con geocerca asignada, dentro de límites

### Cuando Hay Alertas
```
🚨 ALERTA: 🔥 Fiebre detectada en OVINO-001: 40.5°C
🚨 ALERTA: 💓 Taquicardia detectada en BOVINO-002: 125 lpm
🚨 ALERTA: ⚠️ Animal EQUINO-001 fuera de geocerca "Zona Norte"
```

---

## 🎯 Flujo de Trabajo Típico

### 1. Primera Vez (Configuración Inicial)
```bash
# 1. Activar entorno
cd backend
.\venv\Scripts\Activate.ps1

# 2. Asegurarse de que animales tienen geocercas asignadas
# (Desde el Panel Admin en el frontend)

# 3. Reiniciar posiciones (opcional pero recomendado)
python reset_animals.py

# 4. Verificar
python check_animals.py

# 5. Iniciar simulador
python manage.py simulate_collars
```

### 2. Uso Diario
```bash
# Simplemente iniciar
.\start-simulator.ps1

# O con parámetros personalizados
cd backend
.\venv\Scripts\Activate.ps1
python manage.py simulate_collars --interval 3
```

---

## 🐛 Problemas Comunes

### ❌ "Animales fuera de geocerca"

**Síntoma:**
```
🚨 ALERTA: ⚠️ Animal OVINO-001 fuera de geocerca "Perímetro Principal"
```

**Solución:**
```bash
python reset_animals.py
```

---

### ❌ "No se generan alertas de prueba"

**Causa:** El algoritmo funciona correctamente, mantiene animales dentro

**Solución:** Usar endpoint de emergencias simuladas:
```bash
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-001/fiebre/
```

---

### ❌ "Animales no se mueven"

**Causa:** `movement_range` muy pequeño

**Solución:**
```bash
python manage.py simulate_collars --movement-range 0.0008
```

---

## 📈 Monitoreo en Tiempo Real

### Desde el Frontend
1. Abrir http://localhost:3000
2. Login como usuario
3. Ver mapa con animales moviéndose
4. Campana de notificaciones para alertas

### Desde el Backend
- **Terminal:** Ver logs del simulador en tiempo real
- **Admin Django:** http://localhost:8000/admin
  - Ver telemetría
  - Ver alertas
  - Gestionar geocercas

---

## 🧪 Testing del Algoritmo

### Test 1: Inicialización
```bash
# 1. Eliminar telemetría de un animal (en Django Admin o shell)
# 2. Iniciar simulador
python manage.py simulate_collars

# Resultado esperado: Animal inicializado en centroide
```

### Test 2: Pastoreo Virtual
```bash
# 1. Observar movimiento por 1 minuto
# 2. Verificar que NO hay alertas de perímetro
# 3. Verificar con check_animals.py que todos están dentro

python check_animals.py
```

### Test 3: Corrección de Límites
```bash
# Crear geocerca pequeña, observar cómo animales 
# "rebotan" suavemente al acercarse a bordes
python manage.py simulate_collars --movement-range 0.001
```

---

## 💡 Tips y Trucos

### Tip 1: Diferentes Velocidades de Simulación
```bash
# Lento y preciso (para demostraciones)
python manage.py simulate_collars --interval 10

# Normal (uso diario)
python manage.py simulate_collars --interval 5

# Rápido (testing)
python manage.py simulate_collars --interval 1
```

### Tip 2: Combinar con Frontend
```bash
# Terminal 1
.\start-backend.ps1

# Terminal 2
.\start-frontend.ps1

# Terminal 3
.\start-simulator.ps1

# Ahora abrir http://localhost:3000 y ver en tiempo real
```

### Tip 3: Debugging de Movimiento
```bash
# Activar modo verbose para ver más detalles
python manage.py simulate_collars --verbosity 2
```

### Tip 4: Backup Antes de Reiniciar
```bash
# Guardar estado actual
python manage.py dumpdata api.Telemetria > telemetria_backup.json

# Luego reiniciar
python reset_animals.py
```

---

## 📊 Métricas de Éxito

El simulador V3.0 está funcionando correctamente si:

✅ Al iniciar, animales sin telemetría se colocan en centroide
✅ Durante simulación normal, **CERO alertas de perímetro**
✅ Animales se mueven de forma natural y variada
✅ `check_animals.py` muestra todos "✓ SÍ" dentro de geocerca
✅ Signos vitales varían naturalmente sin alertas constantes

---

## 🔗 Documentación Completa

- **CAMBIOS-V3.md** - Documentación técnica completa
- **Actualizacion2.0.md** - Especificaciones originales
- **simulate_collars.py** - Código fuente del simulador

---

## 📞 Comandos de Emergencia

```bash
# Detener simulador
Ctrl + C

# Reiniciar todo desde cero
python reset_animals.py

# Verificar estado
python check_animals.py

# Ver ayuda
python manage.py help simulate_collars

# Restaurar backup
python manage.py loaddata telemetria_backup.json
```

---

## ✅ Checklist de Inicio

Antes de presentar/demostrar:

- [ ] Backend corriendo (`.\start-backend.ps1`)
- [ ] Frontend corriendo (`.\start-frontend.ps1`)
- [ ] Todos los animales tienen geocerca asignada
- [ ] Ejecutado `python reset_animals.py`
- [ ] Verificado con `python check_animals.py`
- [ ] Simulador iniciado (`.\start-simulator.ps1`)
- [ ] No hay alertas de perímetro en la salida

---

**Versión:** CAMPORT V3.0
**Última Actualización:** 11 de Noviembre, 2025
**Estado:** ✅ Producción

---

¡Disfruta del pastoreo virtual! 🐄🐑🐎
