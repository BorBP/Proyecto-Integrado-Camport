# 🎯 QUICK REFERENCE - Cambios Implementados

## Archivos Modificados

### 1. `backend/api/consumers.py`
**Cambios:**
- Cooldowns simplificados: `COOLDOWN_VITALS = 90s`, `COOLDOWN_PERIMETER = 30s`
- Función `can_send_alert()` simplificada (3 parámetros)
- Logs mejorados con valores de temp/BPM
- Eliminados offsets complejos

**Líneas clave modificadas:**
- L12-22: Constantes de cooldown
- L101-124: Función `can_send_alert()`
- L149-307: Función `check_alerts()` con logs mejorados

---

### 2. `backend/api/management/commands/simulate_collars_v8.py`
**Cambios:**
- Hash MD5 del collar_id para distribuir anomalías equitativamente
- Probabilidad de anomalía: 5% → 8%
- Deltas mayores para anomalías (0.4-0.7°C, 12-18 BPM)

**Líneas clave modificadas:**
- L93-144: `update_temperature()` con hash-based distribution
- L146-194: `update_bpm()` con hash-based distribution

---

### 3. `frontend/src/components/admin/GeofenceEditor.js`
**Cambios:**
- Estado `editingCoords` para edición temporal
- Estado `hasChanges` para indicar cambios sin guardar
- Función `handleVertexDrag()` para arrastre de marcadores
- Función `handleApplyChanges()` para guardar y actualizar
- Función `handleCancelChanges()` para revertir
- Marcadores arrastrables con iconos personalizados
- Polígono cambia a naranja cuando hay cambios

**Líneas clave modificadas:**
- L16-22: Nuevos estados
- L31-38: `loadGeocercas()` con inicialización de `editingCoords`
- L48-88: Nuevas funciones de manejo
- L235-316: Sección del mapa con marcadores arrastrables y botones

---

### 4. `frontend/src/components/admin/GeofenceEditor.css`
**Cambios:**
- `.changes-warning`: Banner amarillo para cambios sin guardar
- `.editor-actions`: Contenedor de botones
- `.btn-apply-changes`: Botón verde con hover
- `.btn-cancel-changes`: Botón rojo con hover
- `.modified-badge`: Badge naranja para coordenadas modificadas

**Líneas agregadas:**
- L139-217: Nuevos estilos para editor interactivo

---

### 5. `backend/test_alerts.py` (NUEVO)
**Funcionalidad:**
- Diagnóstico completo del sistema de alertas
- Verifica conexión WebSocket
- Prueba creación de alertas
- Prueba cooldown
- Muestra estadísticas

**Ejecutar:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
python test_alerts.py
```

---

## Verificación Rápida

### ✅ Sistema de Alertas Funcionando
```
Terminal Backend:
🌡️🔥 ALERTA CREADA EN BD: Fiebre detectada: 40.2°C (Animal: OVINO-001) - Temp: 40.2°C
⏱️ Cooldown activo para OVINO-001 - temp: 45s restantes
```

### ✅ Editor de Geocercas Funcionando
```
1. Arrastrar marcador rojo → Polígono naranja
2. "Aplicar Cambios" → Polígono azul + Mensaje verde
3. Simulador: Animales se reposicionan en próximo ciclo
```

---

## Comandos de Inicio

```powershell
# Terminal 1
.\start-backend.ps1

# Terminal 2
.\start-frontend.ps1

# Terminal 3
.\start-simulator-v8.ps1

# Terminal 4 (diagnóstico)
cd backend; .\venv\Scripts\Activate.ps1; python test_alerts.py
```

---

## Valores de Cooldown

| Tipo de Alerta | Cooldown |
|----------------|----------|
| Temperatura | 90s |
| Frecuencia Cardíaca | 90s |
| Perímetro | 30s |

---

## Rangos de Alerta

| Especie | Fiebre | Hipotermia | Agitación | Bajo Estímulo |
|---------|--------|------------|-----------|---------------|
| OVINO | >40°C | <37.5°C | >120 BPM | <40 BPM |
| BOVINO | >39.5°C | <37.0°C | >90 BPM | <40 BPM |
| EQUINO | >39°C | <36.5°C | >55 BPM | <25 BPM |

---

## Troubleshooting Express

| Problema | Solución |
|----------|----------|
| No hay alertas | Verificar que animales tengan geocerca asignada |
| Alertas cada 10s | Reiniciar Django (cooldown en memoria) |
| No se pueden arrastrar marcadores | Usar navegador moderno, revisar consola F12 |
| Connection refused | Iniciar backend primero |

---

**Versión: 8.1.0** | **Estado: ✅ Ready** | **CAMPORT Team**
