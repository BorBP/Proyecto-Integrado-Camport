# 🚀 CAMPORT V5.0 - Guía Rápida

## 🆕 ¿Qué hay de nuevo en V5.0?

| Mejora | Descripción |
|--------|-------------|
| 🚨 **Fugas Aleatorias** | Sistema de escapes controlados cada 60 segundos |
| 🏠 **Retorno Automático** | Animales regresan después de 30 segundos |
| 📊 **Temperatura 1 Decimal** | T:38.8°C en lugar de T:38.7592°C |
| ⚡ **Ejecución Inmediata** | Primer ciclo sin espera |

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
# Demo rápida (fugas cada 30 seg)
python manage.py simulate_collars --escape-interval 30 --return-interval 15

# Normal (fugas cada 60 seg)
python manage.py simulate_collars

# Sin fugas (solo V4.0)
python manage.py simulate_collars --escape-interval 999999
```

---

## 📊 Interpretando la Salida

### Inicio del Simulador
```
================================================================================
🐄 CAMPORT V5.0 - FUGAS ALEATORIAS Y CAOS CONTROLADO 🐄
================================================================================
⏱️  Intervalo: 20 segundos
📏 Rango movimiento: 0.0002 grados
🔄 Consulta dinámica de geocercas en cada ciclo
🚨 Fugas aleatorias: cada 60 segundos
🏠 Retorno automático: después de 30 segundos
🎯 Temperatura: formato con 1 decimal (realista)
================================================================================
```

### Durante Operación Normal
```
📡 CICLO #2 - Consultando estado EN VIVO del rebaño...
🐄 Rebaño detectado: 6 animales

  🟢 [1/6] BOVINO-001: (-38.843, -72.306) en "Zona Norte" | T:38.8°C FC:75lpm
  🟢 [2/6] BOVINO-002: (-38.842, -72.305) en "Zona Norte" | T:39.1°C FC:82lpm
  🟢 [3/6] OVINO-001: (-38.844, -72.304) en "Zona Sur" | T:39.4°C FC:88lpm
```

### Cuando Ocurre una Fuga
```
🚨 FUGA INICIADA: OVINO-002 escapando de su geocerca!
   Retornará automáticamente en 30 segundos...

📡 CICLO #4 - Consultando estado EN VIVO del rebaño...
⚠️  Estado de Fuga: OVINO-002 está FUERA de perímetro
🐄 Rebaño detectado: 6 animales

  🟢 [1/6] BOVINO-001: (-38.843, -72.306) en "Zona Norte" | T:38.7°C FC:77lpm
  🟢 [2/6] BOVINO-002: (-38.842, -72.305) en "Zona Norte" | T:39.2°C FC:80lpm
  🟢 [3/6] OVINO-001: (-38.844, -72.304) en "Zona Sur" | T:39.5°C FC:89lpm
  🔴 [4/6] OVINO-002: (-38.831, -72.238) 🚨 FUGADO de "Zona Sur" | T:38.8°C FC:78lpm
      🚨 ALERTA: Animal OVINO-002 fuera de geocerca "Zona Sur"
  ...

📊 Resumen del Ciclo #4:
   ✓ Procesados: 6/6
   🔴 Fugados: 1
```

### Cuando Animal Retorna
```
🏠 Animal OVINO-002 ha REGRESADO a su geocerca

📡 CICLO #6 - Consultando estado EN VIVO del rebaño...
🐄 Rebaño detectado: 6 animales

  ...
  🟢 [4/6] OVINO-002: (-38.843, -72.304) en "Zona Sur" | T:38.9°C FC:80lpm
```

**Iconos:**
- 🟢 = Animal dentro de geocerca
- 🔴 = Animal FUGADO
- 🚨 = Fuga iniciada / Alerta
- 🏠 = Animal retornado

---

## 🎯 Características Clave

### 1. Fugas Aleatorias Controladas

**¿Cómo funciona?**
- Cada 60 segundos (default), el sistema selecciona un animal aleatorio
- El animal se mueve FUERA de su geocerca
- Se genera una alerta de perímetro
- Después de 30 segundos (default), el animal retorna automáticamente

**Timeline:**
```
0s   → Todos dentro
60s  → FUGA: OVINO-002 escapa
90s  → RETORNO: OVINO-002 regresa
120s → FUGA: BOVINO-001 escapa
150s → RETORNO: BOVINO-001 regresa
...
```

---

### 2. Temperatura con 1 Decimal

**Antes (V4.0):**
```
T:38.7592°C  ← Irreal
T:39.3847°C  ← Confuso
T:37.9123°C  ← Demasiados decimales
```

**Ahora (V5.0):**
```
T:38.8°C  ✅ Realista
T:39.4°C  ✅ Legible
T:37.9°C  ✅ Formato de sensor
```

---

### 3. Ejecución Inmediata

**Comportamiento:**
- Al ejecutar `python manage.py simulate_collars`
- El **Ciclo #1 se ejecuta INMEDIATAMENTE**
- No hay espera inicial
- El `sleep()` ocurre al FINAL de cada ciclo

---

## 🔧 Parámetros Disponibles

### --escape-interval
**Descripción:** Segundos entre fugas aleatorias

**Default:** 60

**Ejemplos:**
```bash
# Fugas frecuentes (demo)
python manage.py simulate_collars --escape-interval 30

# Fugas normales
python manage.py simulate_collars --escape-interval 60

# Fugas ocasionales
python manage.py simulate_collars --escape-interval 180

# Sin fugas
python manage.py simulate_collars --escape-interval 999999
```

---

### --return-interval
**Descripción:** Segundos hasta que animal fugado retorna

**Default:** 30

**Ejemplos:**
```bash
# Retorno rápido (15 seg)
python manage.py simulate_collars --return-interval 15

# Retorno normal (30 seg)
python manage.py simulate_collars --return-interval 30

# Retorno lento (60 seg)
python manage.py simulate_collars --return-interval 60
```

---

### Parámetros V4.0 (Heredados)

```bash
# Intervalo entre ciclos
--interval 20

# Rango de movimiento
--movement-range 0.0002
```

---

## 💡 Configuraciones Recomendadas

### Para Demos a Clientes
```bash
python manage.py simulate_collars \
  --interval 15 \
  --escape-interval 40 \
  --return-interval 20
```
**Resultado:** Fuga cada 40 seg, muy observable

---

### Para Testing
```bash
python manage.py simulate_collars \
  --interval 10 \
  --escape-interval 25 \
  --return-interval 15
```
**Resultado:** Fugas frecuentes, testing rápido

---

### Para Operación Normal
```bash
python manage.py simulate_collars \
  --interval 20 \
  --escape-interval 120 \
  --return-interval 45
```
**Resultado:** Fugas ocasionales, realista

---

### Para Operación Sin Fugas (Solo V4.0)
```bash
python manage.py simulate_collars \
  --interval 20 \
  --escape-interval 999999
```
**Resultado:** Sin fugas, solo pastoreo virtual

---

## 🎬 Caso de Uso: Demo Perfecta

**Preparación:**
1. Iniciar backend y frontend
2. Asignar 4-6 animales a geocercas
3. Abrir frontend en proyector/pantalla grande

**Configuración del simulador:**
```bash
python manage.py simulate_collars \
  --interval 15 \
  --escape-interval 35 \
  --return-interval 20
```

**Durante la demo:**

**Minuto 0:**
- "El sistema está monitoreando el ganado en tiempo real"
- Mostrar mapa con animales moviéndose

**Minuto 0:35:**
- 🚨 FUGA automática
- "¡Alerta! Un animal ha escapado"
- Mostrar campana de notificación
- Ver animal en rojo en mapa

**Minuto 0:55:**
- 🏠 Retorno automático
- "El sistema detectó que el animal retornó"
- Ver animal volver a verde

**Resultado:** Demo dinámica e impactante

---

## 📊 Monitoreo en Tiempo Real

### En el Simulador (Terminal)
```
🚨 FUGA INICIADA: OVINO-002 escapando...
🔴 FUGADO de "Zona Sur"
🏠 Animal OVINO-002 ha REGRESADO
```

### En el Frontend (Navegador)
1. Ver mapa → Animal en rojo moviéndose fuera
2. Campana 🔔 → Alerta de perímetro
3. Panel → Información del animal fugado
4. Después de retorno → Animal vuelve a verde

### En Django Admin
1. Tabla Alertas → Nueva alerta de perímetro
2. Tabla Telemetria → Coordenadas fuera
3. Después de retorno → Coordenadas dentro

---

## 🐛 Solución de Problemas

### ❌ "No se generan fugas"

**Verificar logs:**
```bash
# Debe aparecer cada escape-interval segundos:
🚨 FUGA INICIADA: XXXXX escapando...
```

**Si no aparece:**
```bash
# Reducir escape-interval para testing
python manage.py simulate_collars --escape-interval 20
```

---

### ❌ "Fugas demasiado frecuentes"

**Solución:**
```bash
# Aumentar escape-interval
python manage.py simulate_collars --escape-interval 180
```

---

### ❌ "Animal no retorna"

**Verificar logs:**
```bash
# Debe aparecer después de return-interval:
🏠 Animal XXXXX ha REGRESADO
```

**Si no aparece:** Revisar configuración de return-interval

---

## ✅ Checklist de Demostración

Antes de iniciar:
- [ ] Backend corriendo
- [ ] Frontend corriendo
- [ ] 4-6 animales con geocercas asignadas
- [ ] Simulador con parámetros de demo

Durante demo:
- [ ] Explicar monitoreo en tiempo real
- [ ] Esperar fuga automática
- [ ] Mostrar alerta en frontend
- [ ] Explicar retorno automático
- [ ] Mostrar mapa actualizado

Después:
- [ ] Detener simulador (Ctrl+C)
- [ ] Responder preguntas

---

## 🎓 Tips y Trucos

### Tip 1: Fugas Rápidas para Demos Cortas
```bash
python manage.py simulate_collars --escape-interval 20 --return-interval 10
```

### Tip 2: Ver Solo Fugas en Logs
```bash
python manage.py simulate_collars | grep -E "FUGA|REGRESADO|FUGADO"
```

### Tip 3: Sin Fugas durante Development
```bash
python manage.py simulate_collars --escape-interval 999999
```

### Tip 4: Fugas Muy Ocasionales
```bash
python manage.py simulate_collars --escape-interval 300  # Cada 5 minutos
```

---

## 📞 Comandos de Referencia Rápida

```bash
# Default (fugas cada 60 seg)
python manage.py simulate_collars

# Demo rápida
python manage.py simulate_collars --escape-interval 30 --return-interval 15

# Sin fugas
python manage.py simulate_collars --escape-interval 999999

# Ver ayuda
python manage.py help simulate_collars

# Detener
Ctrl + C
```

---

## 🔗 Documentación Relacionada

- **CAMBIOS-V5.md** - Documentación técnica completa
- **CAMBIOS-V4.md** - Contexto de rebaño completo
- **CAMBIOS-V3.md** - Contexto de pastoreo virtual
- **HISTORIAL-VERSIONES.md** - Evolución completa V1→V5

---

**Versión:** CAMPORT V5.0  
**Última Actualización:** 11 de Noviembre, 2025  
**Estado:** ✅ Producción

---

¡Disfruta de las demos dinámicas con V5.0! 🐄🚨🏠🚀
