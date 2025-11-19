# 🚀 CAMPORT V7.0 - GUÍA DE INICIO RÁPIDO

## ⚡ Diferencias Clave: V6.0 vs V7.0

### V6.0 (ANTERIOR - Gravedad de Centroide)
```bash
python manage.py simulate_collars --gravity-factor 0.2
```
- ❌ Animales tienden al centro
- ❌ Movimiento predecible
- ❌ Fugas temporales aleatorias
- ❌ Hardcoded a ubicación específica

### V7.0 (NUEVO - Random Walk Natural)
```bash
python manage.py simulate_collars_v7
```
- ✅ Movimiento 100% errático
- ✅ Sin tendencia al centro
- ✅ Oveja negra específica persistente
- ✅ Funciona en cualquier parte del mundo

---

## 🎯 INICIO RÁPIDO

### 1. Usando el Script Automático

```powershell
# Ejecutar simulador V7.0
.\start-simulator-v7.ps1
```

### 2. Manual (Control Total)

```powershell
# Activar entorno
cd backend
.\venv\Scripts\Activate.ps1

# Simulador básico
python manage.py simulate_collars_v7

# Con parámetros personalizados
python manage.py simulate_collars_v7 --interval 15 --black-sheep OVINO-001 --escape-probability 0.2
```

---

## 🎮 PARÁMETROS DISPONIBLES

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `--interval` | 20 | Segundos entre ciclos |
| `--movement-range` | 0.0003 | Grados de movimiento (~30m) |
| `--black-sheep` | Auto | ID del animal "oveja negra" |
| `--escape-probability` | 0.15 | Probabilidad de escape (0.0-1.0) |

### Ejemplos de Uso

```bash
# Ciclos rápidos para testing
python manage.py simulate_collars_v7 --interval 10

# Movimiento amplio
python manage.py simulate_collars_v7 --movement-range 0.0005

# Oveja negra específica
python manage.py simulate_collars_v7 --black-sheep BOVINO-002

# Escapes frecuentes (demo)
python manage.py simulate_collars_v7 --escape-probability 0.3

# Combinación completa
python manage.py simulate_collars_v7 \
  --interval 15 \
  --movement-range 0.0004 \
  --black-sheep OVINO-001 \
  --escape-probability 0.2
```

---

## 🐑 LA OVEJA NEGRA

### ¿Qué es?

**Un animal específico** que tiene comportamiento diferente:
- Probabilidad de intentar escapar
- Movimiento dirigido hacia afuera
- Continúa alejándose al escapar
- Pequeña probabilidad de retornar (5%)

### Selección

```bash
# Automática (aleatorio)
python manage.py simulate_collars_v7

# Manual (específico)
python manage.py simulate_collars_v7 --black-sheep OVINO-001
```

### Comportamiento Observable

```
Ciclo #5: 📍 OVINO-001 🐑: OK            # Normal
Ciclo #6: 🏃 OVINO-001 (OVEJA NEGRA) está intentando ESCAPAR!
Ciclo #7: ⚠️  OVINO-001 🐑⚫: FUERA       # Escapada
Ciclo #8: ⚠️  OVINO-001 🐑⚫: FUERA       # Continúa fuera
Ciclo #12: 🔙 OVINO-001 (OVEJA NEGRA) ha REGRESADO
```

---

## 🗺️ GEOCERCAS Y ADAPTABILIDAD

### Sin Geocerca Asignada

El animal aparece en la **primera geocerca disponible** como placeholder:

```
📌 EQUINO-001: PLACEHOLDER | Geocerca: Potrero Norte (Placeholder)
```

### Con Geocerca Asignada

El animal se mueve naturalmente dentro de sus límites:

```
📍 OVINO-001: OK | Geocerca: Potrero Sur
```

### Cambio de Geocerca

Si cambias la asignación durante la simulación:

```
# Antes
📍 OVINO-001: OK | Geocerca: Potrero Norte

# Cambias en Admin Panel: Norte → Sur

# Siguiente ciclo
🔄 OVINO-001: Geocerca cambiada - Reposicionando...
📍 OVINO-001: OK | Geocerca: Potrero Sur
```

**¡Adaptación automática!** No necesitas reiniciar el simulador.

---

## 📊 ENTENDIENDO LOS LOGS

### Símbolos

- 📍 = Dentro de geocerca (OK)
- ⚠️  = Fuera de límites
- 📌 = Placeholder (sin geocerca)
- 🐑 = Oveja negra (comportamiento normal)
- 🐑⚫ = Oveja negra escapada
- 🔄 = Cambio de geocerca detectado
- 🏃 = Intento de escape
- 🔙 = Retorno a geocerca

### Ejemplo de Ciclo Completo

```
━━━ CICLO #10 ━━━
  📍 OVINO-001: OK | Temp: 38.7°C | FC: 75 lpm | Geocerca: Potrero Norte
  📍 OVINO-002: OK | Temp: 39.1°C | FC: 80 lpm | Geocerca: Potrero Norte
  ⚠️  BOVINO-001 🐑⚫: FUERA | Temp: 38.4°C | FC: 70 lpm | Geocerca: Potrero Sur
  📍 BOVINO-002: OK | Temp: 38.6°C | FC: 72 lpm | Geocerca: Potrero Sur
  📌 EQUINO-001: PLACEHOLDER | Temp: 37.9°C | FC: 35 lpm | Geocerca: Potrero Norte (Placeholder)
    ⚠️  ALERTAS: 1 generadas

📊 RESUMEN:
   ✓ Exitosos: 4
   ⚠️  Fuera de límites: 1
   📌 Sin geocerca: 1

⏳ Esperando 18.2 segundos...
```

---

## 🔄 MIGRACIÓN DESDE V6.0

### Cambios Necesarios

**¡NINGUNO!** El simulador V7.0 es **completamente compatible** con:
- Base de datos existente
- Modelos de Django
- WebSocket consumer
- Frontend React

### Ejecutar Ambas Versiones

```bash
# Terminal 1: V6.0 (viejo)
python manage.py simulate_collars --gravity-factor 0.2

# Terminal 2: V7.0 (nuevo)
python manage.py simulate_collars_v7
```

**Recomendación:** Usa V7.0 para comportamiento natural.

---

## 🧪 TESTING Y VALIDACIÓN

### Verificar Instalación

```powershell
# 1. Verificar archivo existe
Get-Item backend\api\management\commands\simulate_collars_v7.py

# 2. Ver ayuda del comando
cd backend
.\venv\Scripts\Activate.ps1
python manage.py help simulate_collars_v7
```

### Test de Conectividad

```bash
# 1. Iniciar Django en otra terminal
python manage.py runserver

# 2. Iniciar simulador
python manage.py simulate_collars_v7

# Debe mostrar: "✓ Conectado a WebSocket"
```

### Test de Oveja Negra

```bash
# Alta probabilidad para testing
python manage.py simulate_collars_v7 --escape-probability 0.8

# Deberías ver escapes en ~80% de ciclos
```

---

## 🌍 USO CON DIFERENTES GEOCERCAS

### Chile (Default)
```json
{
  "nombre": "Potrero Araucanía",
  "coordenadas": [
    {"lat": -38.8440, "lng": -72.2946},
    ...
  ]
}
```

### España
```json
{
  "nombre": "Dehesa Extremadura",
  "coordenadas": [
    {"lat": 39.4699, "lng": -6.3724},
    ...
  ]
}
```

### Nueva Zelanda
```json
{
  "nombre": "Canterbury Paddock",
  "coordenadas": [
    {"lat": -43.5321, "lng": 172.6362},
    ...
  ]
}
```

**El simulador funciona idénticamente** en cualquier ubicación.

---

## ⚙️ CONFIGURACIONES RECOMENDADAS

### Desarrollo
```bash
python manage.py simulate_collars_v7 \
  --interval 10 \
  --movement-range 0.0005 \
  --escape-probability 0.3
```
- Ciclos rápidos (visualización rápida)
- Movimiento amplio (fácil de ver)
- Escapes frecuentes (testing de alertas)

### Producción
```bash
python manage.py simulate_collars_v7 \
  --interval 20 \
  --movement-range 0.0003 \
  --escape-probability 0.15
```
- Ciclos realistas (20s)
- Movimiento natural (~30m)
- Escapes ocasionales (realista)

### Demostración
```bash
python manage.py simulate_collars_v7 \
  --interval 15 \
  --black-sheep OVINO-001 \
  --escape-probability 0.25
```
- Oveja negra específica (predecible)
- Escapes moderadamente frecuentes (impacto visual)

---

## 🆘 TROUBLESHOOTING

### Error: "No module named 'websockets'"
```bash
pip install websockets
```

### Error: "Connection refused"
**Solución:** Iniciar Django primero
```bash
# Terminal 1
python manage.py runserver

# Terminal 2
python manage.py simulate_collars_v7
```

### Error: "Animal matching query does not exist"
**Solución:** Poblar base de datos
```bash
python populate_db.py
```

### No veo movimiento en el mapa
**Verificar:**
1. ✅ Backend ejecutándose (puerto 8000)
2. ✅ Frontend ejecutándose (puerto 3000)
3. ✅ Simulador ejecutándose (logs activos)
4. ✅ WebSocket conectado (ver logs)

---

## 📚 DOCUMENTACIÓN ADICIONAL

- **Documentación Completa:** `SIMULADOR-V7-DOCUMENTACION.md`
- **Arquitectura General:** `DOCUMENTACION.md`
- **Guía de Inicio:** `INICIO-RAPIDO.md`

---

## 🎓 CONCEPTOS CLAVE

### Random Walk
Algoritmo de movimiento donde cada paso es completamente aleatorio:
- No hay "memoria" de pasos anteriores
- No hay objetivo o atracción
- Distribución uniforme en el espacio

### Bouncing Physics
Al tocar un borde, el animal "rebota":
- Invierte dirección del movimiento
- Reduce velocidad (50%)
- Previene quedarse pegado al borde

### Oveja Negra
Animal con comportamiento anómalo:
- Tendencia a escapar (no accidental)
- Útil para testing de alertas
- Representa animal problemático real

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de reportar un problema:

- [ ] Django ejecutándose (puerto 8000)
- [ ] Frontend ejecutándose (puerto 3000)
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Base de datos migrada (`python manage.py migrate`)
- [ ] Datos poblados (`python populate_db.py`)
- [ ] WebSocket funcional (logs muestran conexión)

---

## 🚀 PRÓXIMOS PASOS

1. **Iniciar Sistema:**
   ```powershell
   # Terminal 1
   .\start-backend.ps1
   
   # Terminal 2
   .\start-frontend.ps1
   
   # Terminal 3
   .\start-simulator-v7.ps1
   ```

2. **Abrir en navegador:**
   ```
   http://localhost:3000
   ```

3. **Observar comportamiento:**
   - Animales moviéndose errácticamente
   - Oveja negra con marcador especial
   - Alertas al escapar

4. **Experimentar:**
   - Cambiar geocerca de un animal
   - Observar adaptación automática
   - Probar diferentes parámetros

---

**¡Listo para usar CAMPORT V7.0!** 🎉

**¿Preguntas?** Consulta `SIMULADOR-V7-DOCUMENTACION.md` para detalles técnicos.

---

**CAMPORT Team - Noviembre 2025**  
**Versión:** 7.0.0  
**Estado:** ✅ Production Ready
