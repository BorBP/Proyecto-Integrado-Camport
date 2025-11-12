# 🚀 CAMPORT V4.0 - Guía Rápida

## 🆕 ¿Qué hay de nuevo en V4.0?

| Mejora | Descripción |
|--------|-------------|
| 🐄 **Rebaño Completo** | Simula TODOS los animales en cada ciclo |
| ⏱️ **Movimiento Realista** | Intervalo de 20 segundos (configurable) |
| 🔄 **Consulta Dinámica** | Estado EN VIVO de geocercas en cada ciclo |
| 📡 **Auto-Adaptación** | Reacciona a cambios SIN reiniciar |

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
# Más lento (30 segundos - ideal para demos)
python manage.py simulate_collars --interval 30

# Normal (20 segundos - default)
python manage.py simulate_collars --interval 20

# Más rápido (10 segundos - testing)
python manage.py simulate_collars --interval 10
```

---

## 📊 Interpretando la Salida

### Inicio del Simulador
```
======================================================================
🐄 CAMPORT V4.0 - SIMULADOR DE REBAÑO COMPLETO 🐄
======================================================================
⏱️  Intervalo: 20 segundos (movimiento realista)
📏 Rango movimiento: 0.0002 grados
🔄 Consulta dinámica de geocercas en cada ciclo
======================================================================

✓ Conectado a WebSocket
```

### Durante un Ciclo
```
======================================================================
📡 CICLO #5 - Consultando estado EN VIVO del rebaño...
======================================================================
🐄 Rebaño detectado: 6 animales con geocerca asignada

  🟢 [1/6] BOVINO-001: (-38.843, -72.306) en "Zona Norte" | T:38.5°C FC:75lpm
  🟢 [2/6] BOVINO-002: (-38.842, -72.305) en "Zona Norte" | T:38.8°C FC:82lpm
  🟢 [3/6] BOVINO-003: (-38.842, -72.305) en "Zona Sur" | T:39.1°C FC:68lpm
  🎯 [4/6] EQUINO-001: INICIALIZADO en centroide de "Zona Este"
  🟢 [5/6] OVINO-001: (-38.844, -72.304) en "Zona Norte" | T:39.0°C FC:85lpm
      🚨 ALERTA: Taquicardia detectada en OVINO-001: 122 lpm
  🟢 [6/6] OVINO-002: (-38.843, -72.303) en "Zona Sur" | T:38.7°C FC:78lpm

📊 Resumen del Ciclo #5:
   ✓ Procesados: 6/6
   🎯 Inicializados: 1

⏳ Ciclo #5 completado. Esperando 20 segundos...
   (Movimiento lento y realista del ganado)
```

**Iconos:**
- 🟢 = Animal procesado OK
- 🎯 = Animal recién inicializado
- 🚨 = Alerta generada
- ⏳ = Esperando próximo ciclo

---

## 🎯 Características Clave

### 1. Consulta Dinámica EN VIVO

**¿Qué significa?**
- En cada ciclo, el simulador consulta la BD
- Obtiene la lista ACTUALIZADA de animales
- Ve los cambios de geocerca en tiempo real

**Ejemplo práctico:**
```
CICLO #1:
  BOVINO-001 → Zona A

[Admin reasigna BOVINO-001 a Zona B]

CICLO #2:
  BOVINO-001 → Zona B  ← ✅ Cambio detectado automáticamente!
```

---

### 2. Procesamiento de Rebaño Completo

**Antes (V3.0):**
- Procesaba animales uno por uno
- No optimizado para escala

**Ahora (V4.0):**
```
🐄 Rebaño detectado: 50 animales con geocerca asignada

[1/50] Animal 1...
[2/50] Animal 2...
...
[50/50] Animal 50...

✓ Procesados: 50/50
```

**Escalabilidad:**
- 10 animales: ~2 segundos/ciclo
- 50 animales: ~10 segundos/ciclo
- 100 animales: ~20 segundos/ciclo

---

### 3. Movimiento Lento y Realista

**Configuración:**

| Intervalo | Uso | Observación |
|-----------|-----|-------------|
| 30 seg | Demos/Presentaciones | Muy observable |
| 20 seg | Operación normal | **Default** |
| 10 seg | Testing | Más dinámico |

**Cambiar velocidad:**
```bash
# Lento
python manage.py simulate_collars --interval 30

# Rápido
python manage.py simulate_collars --interval 10
```

---

## 🔧 Parámetros Disponibles

### --interval
**Descripción:** Segundos entre ciclos de simulación

**Default:** 20

**Ejemplos:**
```bash
python manage.py simulate_collars --interval 25
python manage.py simulate_collars --interval 15
```

---

### --movement-range
**Descripción:** Amplitud del movimiento en grados

**Default:** 0.0002

**Ejemplos:**
```bash
# Movimiento muy pequeño
python manage.py simulate_collars --movement-range 0.0001

# Movimiento más amplio
python manage.py simulate_collars --movement-range 0.0004
```

---

## 💡 Casos de Uso Comunes

### Caso 1: Agregar Nuevos Animales

**Sin detener el simulador:**

1. Ir al Panel Admin
2. Crear nuevo animal (ej: BOVINO-010)
3. Asignar geocerca al animal
4. Esperar próximo ciclo

**Resultado:**
```
📡 CICLO #15 - Consultando estado EN VIVO...
🐄 Rebaño detectado: 7 animales  ← +1 nuevo!

  ...
  🎯 [7/7] BOVINO-010: INICIALIZADO en "Zona Norte"
```

✅ **No requiere reinicio del simulador**

---

### Caso 2: Cambiar Geocerca de Animal

**Sin detener el simulador:**

1. Panel Admin → Editar BOVINO-005
2. Cambiar geocerca de "Zona A" a "Zona B"
3. Guardar
4. Esperar próximo ciclo

**Resultado:**
```
📡 CICLO #8 - Consultando estado EN VIVO...

  🟢 [5/10] BOVINO-005: (...) en "Zona B"  ← ✅ Cambiado!
```

✅ **Adaptación automática**

---

### Caso 3: Demostración a Clientes

**Configuración ideal:**
```bash
python manage.py simulate_collars --interval 30 --movement-range 0.0001
```

**Beneficios:**
- Movimiento muy observable (30 seg)
- Pasos pequeños y precisos
- Fácil de seguir en presentación

---

## 🐛 Solución de Problemas

### ❌ "No hay animales con geocerca asignada"

**Causa:** Ningún animal tiene geocerca

**Solución:**
1. Panel Admin → Gestión de Ganado
2. Editar animales
3. Asignar geocerca a cada uno
4. Guardar

**Próximo ciclo:** ✅ Animales detectados

---

### ❌ "Error WebSocket"

**Causa:** Backend no está corriendo

**Solución:**
```bash
# Terminal separado
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

### ❌ Movimiento muy rápido/lento

**Para ajustar:**
```bash
# Más lento
python manage.py simulate_collars --interval 30

# Más rápido
python manage.py simulate_collars --interval 10
```

---

## 📈 Monitoreo en Tiempo Real

### En el Simulador (Terminal)
```
📡 CICLO #X - Consultando estado EN VIVO...
🟢 [N/Total] ANIMAL: (lat, lng) en "GEOCERCA"
📊 Resumen: X procesados
```

### En el Frontend (Navegador)
1. Abrir http://localhost:3000
2. Login
3. Ver mapa con animales moviéndose lentamente
4. Campana (🔔) para alertas

### En Django Admin
1. http://localhost:8000/admin
2. Ver tabla Telemetria
3. Nuevos registros cada 20 segundos

---

## ✅ Checklist de Operación

Antes de iniciar producción:

- [ ] Backend corriendo (`python manage.py runserver`)
- [ ] Frontend corriendo (`npm start`)
- [ ] Todos los animales tienen geocerca asignada
- [ ] Geocercas tienen coordenadas válidas
- [ ] Intervalo configurado (default 20 seg está bien)
- [ ] Simulador iniciado

Durante operación:

- [ ] Ver logs del simulador para confirmar ciclos
- [ ] Verificar mapa actualizado en frontend
- [ ] Probar cambio de geocerca (debe detectarse)
- [ ] Probar agregar animal (debe aparecer)

---

## 🎓 Tips y Trucos

### Tip 1: Intervalo Óptimo por Uso

```bash
# Presentaciones/Demos
--interval 30

# Uso normal
--interval 20  # Default

# Development/Testing
--interval 10
```

### Tip 2: Combinación de Parámetros

```bash
# Demostración perfecta
python manage.py simulate_collars --interval 30 --movement-range 0.00015

# Operación estándar
python manage.py simulate_collars

# Testing rápido
python manage.py simulate_collars --interval 5 --movement-range 0.0003
```

### Tip 3: Monitoreo de Recursos

```powershell
# En otra terminal
Get-Process python | Select-Object CPU, WorkingSet
```

### Tip 4: Logs Limpios

Para reducir verbosidad, puedes redirigir:
```bash
python manage.py simulate_collars > sim.log 2>&1
```

---

## 📞 Comandos de Referencia Rápida

```bash
# Iniciar con defaults
python manage.py simulate_collars

# Ver ayuda
python manage.py help simulate_collars

# Personalizado
python manage.py simulate_collars --interval 25 --movement-range 0.00025

# Detener
Ctrl + C

# Ver estado de animales
python check_animals.py

# Reiniciar posiciones
python reset_animals.py
```

---

## 🔗 Documentación Relacionada

- **CAMBIOS-V4.md** - Documentación técnica completa
- **CAMBIOS-V3.md** - Contexto de pastoreo virtual
- **CAMBIOS-V2.md** - Contexto de geocercas múltiples

---

**Versión:** CAMPORT V4.0
**Última Actualización:** 11 de Noviembre, 2025
**Estado:** ✅ Producción

---

¡Disfruta del realismo de V4.0! 🐄⏱️🔄
