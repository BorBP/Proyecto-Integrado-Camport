# 🚀 CAMPORT - GUÍA DE INICIO RÁPIDO DE SIMULADORES

## 📋 Versiones Disponibles

### V6.0 - Gravedad de Centroide
**Estado:** Estable  
**Características:**
- Movimiento con atracción al centro (20%)
- Sistema de fugas aleatorias
- Retorno automático

### V7.0 - Random Walk Natural + Oveja Negra
**Estado:** Estable  
**Características:**
- Random Walk puro (sin gravedad)
- Oveja negra con tendencia a escapar
- Adaptabilidad dinámica a geocercas
- Reposicionamiento automático

### V8.0 - Signos Vitales Realistas ⭐ RECOMENDADO
**Estado:** Producción  
**Características:**
- ✅ Signos vitales con variación gradual (Temperatura + BPM)
- ✅ Intervalos independientes por tipo de dato
- ✅ Alertas inteligentes (solo si animal tiene geocerca)
- ✅ Sistema de cooldown anti-spam
- ✅ Múltiples loops asíncronos

---

## ⚡ INICIO RÁPIDO

### Opción 1: Script Unificado (Recomendado)

```powershell
# Usar V8 (por defecto)
.\start-simulator.ps1

# Usar V7
.\start-simulator.ps1 v7

# Usar V6
.\start-simulator.ps1 v6

# Ver ayuda completa
.\start-simulator.ps1 -Help
```

### Opción 2: Scripts Individuales

```powershell
# V6
.\start-simulator-v6.ps1    # (antiguo start-simulator.ps1)

# V7
.\start-simulator-v7.ps1

# V8
.\start-simulator-v8.ps1
```

---

## 🎮 PARÁMETROS Y OPCIONES

### V6.0 - Gravedad de Centroide

```powershell
.\start-simulator.ps1 v6 -Interval 20

# O manual:
python manage.py simulate_collars --interval 20 --gravity-factor 0.2
```

**Parámetros:**
- `--interval` - Segundos entre ciclos (default: 20)
- `--gravity-factor` - Factor de atracción 0.0-1.0 (default: 0.2)

---

### V7.0 - Random Walk Natural

```powershell
.\start-simulator.ps1 v7 -Interval 20 -BlackSheep "OVINO-001"

# O manual:
python manage.py simulate_collars_v7 --interval 20 --black-sheep OVINO-001
```

**Parámetros:**
- `--interval` - Segundos entre ciclos (default: 20)
- `--movement-range` - Rango de movimiento (default: 0.0003)
- `--black-sheep` - ID de la oveja negra (default: aleatorio)
- `--escape-probability` - Probabilidad de escape 0.0-1.0 (default: 0.15)

---

### V8.0 - Signos Vitales Realistas ⭐

```powershell
# Con script unificado
.\start-simulator.ps1 v8 -IntervalMovement 3 -IntervalTemperature 5 -IntervalBpm 2

# O manual:
python manage.py simulate_collars_v8 \
    --interval-movement 3 \
    --interval-temperature 5 \
    --interval-bpm 2 \
    --alert-cooldown 60
```

**Parámetros:**
- `--interval-movement` - Segundos entre actualizaciones de posición (default: 3)
- `--interval-temperature` - Segundos entre actualizaciones de temperatura (default: 5)
- `--interval-bpm` - Segundos entre actualizaciones de BPM (default: 2)
- `--movement-range` - Rango de movimiento (default: 0.0003)
- `--black-sheep` - ID de la oveja negra (default: aleatorio)
- `--escape-probability` - Probabilidad de escape (default: 0.15)
- `--alert-cooldown-vitals` - Segundos entre alertas de signos vitales (default: 180)
- `--alert-cooldown-perimeter` - Segundos entre alertas de perímetro (default: 60)

---

## 📊 COMPARATIVA DE VERSIONES

| Característica | V6 | V7 | V8 |
|----------------|----|----|-----|
| **Movimiento** | Gravedad centroide | Random walk | Random walk |
| **Oveja negra** | Temporal | Específica | Específica |
| **Signos vitales** | Básicos | Básicos | Graduales realistas |
| **Intervalos** | Unificado | Unificado | Independientes ⭐ |
| **Alertas** | Siempre | Siempre | Solo con geocerca ⭐ |
| **Cooldown** | No | No | Sí (180s/60s) ⭐ |
| **Adaptabilidad** | Manual | Automática | Automática |

---

## 🎯 CASOS DE USO

### Para Desarrollo/Testing
```powershell
# V8 con ciclos rápidos
.\start-simulator.ps1 v8 -IntervalMovement 2 -IntervalTemperature 3 -IntervalBpm 1
```

### Para Producción
```powershell
# V8 con valores por defecto (recomendado)
.\start-simulator.ps1 v8
```

### Para Demos
```powershell
# V7 con oveja negra específica
.\start-simulator.ps1 v7 -BlackSheep "OVINO-001" -Interval 15
```

---

## 📋 SISTEMA COMPLETO DE 3 TERMINALES

### Terminal 1: Backend
```powershell
.\start-backend.ps1
```

### Terminal 2: Frontend
```powershell
.\start-frontend.ps1
```

### Terminal 3: Simulador
```powershell
# Opción A: V8 (Recomendado para producción)
.\start-simulator.ps1 v8

# Opción B: V7 (Para testing de movimiento)
.\start-simulator.ps1 v7

# Opción C: V6 (Para comparar comportamientos)
.\start-simulator.ps1 v6
```

---

## 🔍 SALIDA ESPERADA

### V8.0 - Signos Vitales

```
━━━ ESTADÍSTICAS CICLO #5 ━━━
  ✅ BOVINO-001: Temp=38.3°C | BPM=68 | Pos=(-38.84451, -72.29408)
  ✅ BOVINO-002🐑: Temp=38.7°C | BPM=72 | Pos=(-38.84382, -72.30627)
  🌡️🔥 ALERTA: EQUINO-001 - FIEBRE: 40.2°C
  ✅ EQUINO-001: Temp=40.2°C | BPM=35 | Pos=(-38.84380, -72.30661)
  ✅ OVINO-001: Temp=39.1°C | BPM=78 | Pos=(-38.84394, -72.30673)
  ❤️⚡ ALERTA: OVINO-002 - AGITACIÓN: 105 BPM
  ✅ OVINO-002: Temp=38.9°C | BPM=105 | Pos=(-38.84470, -72.29379)
```

### V7.0 - Random Walk

```
━━━ CICLO #10 ━━━
  📍 BOVINO-001: OK | Temp: 38.3°C | FC: 68 lpm | Geocerca: Perimetro secundario
  🔄 BOVINO-002: Geocerca reasignada - Reposicionando...
  📍 BOVINO-002 🔄: OK | Temp: 38.7°C | FC: 72 lpm | Geocerca: Perímetro Principal
  🏃 OVINO-001 (OVEJA NEGRA) está intentando ESCAPAR!
  ⚠️ OVINO-001 🐑⚫: FUERA | Temp: 39.1°C | FC: 78 lpm

📊 RESUMEN:
   ✓ Exitosos: 4
   🔄 Reposicionados: 1
   ⚠️ Fuera de límites: 1
```

---

## 🆘 TROUBLESHOOTING

### Error: "Connection refused"
**Solución:** Inicia el backend primero
```powershell
.\start-backend.ps1
```

### Error: "No module named 'websockets'"
**Solución:** Instala dependencias
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### No veo animales moviéndose
**Verificar:**
1. ✅ Backend corriendo (puerto 8000)
2. ✅ Frontend corriendo (puerto 3000)
3. ✅ Simulador corriendo (logs en terminal)
4. ✅ Animales tienen geocerca asignada

### Alertas no aparecen (V8)
**Verificar:**
- ✅ Los animales tienen geocerca asignada
- ✅ Cooldown de 60s entre alertas del mismo tipo
- ✅ Los valores están fuera de rangos normales

---

## 📝 NOTAS IMPORTANTES

### V8.0 - Alertas Inteligentes
- **Solo se generan alertas si el animal tiene geocerca asignada**
- Cooldown diferenciado:
  - Signos vitales (Temp/BPM): 180 segundos (3 minutos)
  - Perímetro: 60 segundos (1 minuto)
- Rangos de alerta ajustados por especie

### Rangos de Alerta por Especie (V8)

**🐑 OVINO:**
- Temperatura: Fiebre >40°C, Hipotermia <37.5°C
- BPM: Agitación >100, Bajo estímulo <50

**🐄 BOVINO:**
- Temperatura: Fiebre >39.5°C, Hipotermia <37.0°C
- BPM: Agitación >90, Bajo estímulo <45

**🐴 EQUINO:**
- Temperatura: Fiebre >39.0°C, Hipotermia <36.5°C
- BPM: Agitación >55, Bajo estímulo <25

---

## 🎓 RECOMENDACIONES

### Para Producción
✅ **Usar V8.0** - Más realista, alertas inteligentes, intervalos independientes

### Para Testing
✅ **Usar V7.0** - Control preciso del movimiento, oveja negra específica

### Para Comparar
✅ **Usar V6.0** - Ver diferencia entre gravedad y random walk

---

## 📚 DOCUMENTACIÓN ADICIONAL

- **Arquitectura completa:** `DOCUMENTACION.md`
- **Detalles V7:** `SIMULADOR-V7-DOCUMENTACION.md`
- **Comparativa:** `COMPARATIVA-V6-V7.md`

---

## ✨ QUICK TIPS

```powershell
# Ver ayuda del script unificado
.\start-simulator.ps1 -Help

# Ver parámetros de V8
python manage.py simulate_collars_v8 --help

# Cambiar intervalos en tiempo real
# (Detener con Ctrl+C y reiniciar con nuevos parámetros)
```

---

**Desarrollado con ❤️ por CAMPORT Team**  
**Versión:** 8.0.0  
**Estado:** ✅ Production Ready

🐑 El futuro digital de la ganadería 🐑
