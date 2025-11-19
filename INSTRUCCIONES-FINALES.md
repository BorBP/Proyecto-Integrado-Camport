# ✅ INSTRUCCIONES FINALES - SISTEMA DE ALERTAS Y GEOCERCAS

## 🎯 RESUMEN DE LO IMPLEMENTADO

### 1. Sistema de Alertas Mejorado
- ✅ Cooldown de 90 segundos para alertas de temperatura y BPM
- ✅ Cooldown de 30 segundos para alertas de perímetro
- ✅ Variación automática entre diferentes animales (usa hash del collar_id)
- ✅ Mayor probabilidad de anomalías (8% vs 5% anterior)
- ✅ Sistema simplificado sin offsets complejos

### 2. Editor de Geocercas Renovado
- ✅ Marcadores arrastrables para editar vértices
- ✅ Vista previa en tiempo real (polígono naranja)
- ✅ Botón "Aplicar Cambios" que actualiza animales automáticamente
- ✅ Botón "Descartar Cambios" para revertir
- ✅ Indicadores visuales de cambios sin guardar

### 3. Script de Diagnóstico
- ✅ `backend/test_alerts.py` para verificar el sistema completo
- ✅ Prueba conexión WebSocket, alertas, cooldown, etc.

---

## 🚀 CÓMO PROBAR TODO

### PASO 1: Iniciar Backend (Terminal 1)
```powershell
cd "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO"
.\start-backend.ps1
```

**Esperar a ver:** `Starting development server at http://127.0.0.1:8000/`

---

### PASO 2: Iniciar Frontend (Terminal 2)
```powershell
cd "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO"
.\start-frontend.ps1
```

**Esperar a ver:** `webpack compiled successfully`

---

### PASO 3: Iniciar Simulador V8 (Terminal 3)
```powershell
cd "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO"
.\start-simulator-v8.ps1

# O con el script unificado:
.\start-simulator.ps1 v8
```

**Deberías ver:**
- Conexión al WebSocket establecida
- Estadísticas cada 10 segundos con Temp/BPM/Posición
- Alertas ocasionales (cada ~90s para cada tipo)

---

### PASO 4: Ejecutar Diagnóstico (Terminal 4 - OPCIONAL)
```powershell
cd "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO\backend"
.\venv\Scripts\Activate.ps1
python test_alerts.py
```

**Esto verificará:**
1. Estado inicial de animales y geocercas
2. Creación de alertas en BD
3. Funcionamiento del cooldown
4. Alertas de diferentes tipos

---

## 🔍 QUÉ OBSERVAR

### En la Terminal del Backend (Terminal 1):
```
🌡️🔥 ALERTA CREADA EN BD: Fiebre detectada: 40.2°C (Animal: OVINO-001) - Temp: 40.2°C
❤️⬆️ ALERTA CREADA EN BD: Frecuencia cardíaca alta: 125 lpm (Animal: BOVINO-002) - BPM: 125
🚨 ALERTA CREADA EN BD: Animal EQUINO-001 fuera de geocerca "Perímetro Principal"
⏱️ Cooldown activo para OVINO-001 - temp: 45s restantes
```

### En la Terminal del Simulador (Terminal 3):
```
━━━ ESTADÍSTICAS CICLO #15 ━━━
  ✅ BOVINO-001: Temp=38.3°C | BPM=68 | Pos=(-38.84451, -72.29408)
  ✅ BOVINO-002: Temp=38.7°C | BPM=72 | Pos=(-38.84382, -72.30627)
  🌡️🔥 ALERTA: EQUINO-001 - FIEBRE: 40.2°C
  ✅ EQUINO-001🐑: Temp=40.2°C | BPM=35 | Pos=(-38.84380, -72.30661)
```

### En el Frontend (Navegador):
1. Ir a `http://localhost:3000`
2. Login como admin
3. Ver la campana de notificaciones 🔔 con el número de alertas
4. Click en la campana para ver detalles:
   - Tipo de alerta (TEMPERATURA, FRECUENCIA, PERIMETRO)
   - Mensaje descriptivo con valores
   - Timestamp
   - Animal afectado

---

## 🛠️ PROBAR EL EDITOR DE GEOCERCAS

### En el Frontend:
1. Login como administrador
2. Ir a "Gestión de Geocercas" (menú de administración)
3. Seleccionar una geocerca de la lista izquierda
4. **Arrastrar los marcadores rojos** en el mapa:
   - El polígono cambia a color naranja
   - Aparece un banner amarillo "Hay cambios sin guardar"
   - Los botones se habilitan
5. Click en **"Aplicar Cambios y Actualizar Animales"**
6. **Resultado esperado:**
   - Las coordenadas se guardan en BD
   - El polígono vuelve a azul
   - Mensaje de confirmación verde
   - En el siguiente ciclo del simulador:
     * Los animales detectan el cambio
     * Si quedaron fuera, se reposicionan dentro
     * Continúan moviéndose normalmente

---

## 🐛 TROUBLESHOOTING

### ❌ "No module named 'django'"
**Solución:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ "Connection refused" en simulador
**Solución:**
- Asegúrate de que el backend esté corriendo en puerto 8000
- Verifica con: `Test-NetConnection localhost -Port 8000`

### ❌ No aparecen alertas
**Verificar:**
1. ✅ ¿Los animales tienen geocerca asignada?
   ```python
   python manage.py shell -c "from api.models import Animal; [print(f'{a.display_id}: {a.geocerca.nombre if a.geocerca else None}') for a in Animal.objects.all()]"
   ```
2. ✅ ¿El simulador está enviando datos?
   - Ver logs en Terminal 3
3. ✅ ¿El cooldown está activo?
   - Esperar 90 segundos después de una alerta del mismo tipo
4. ✅ ¿Los valores están fuera de rango?
   - Fiebre: >40°C
   - Hipotermia: <37.5°C
   - Agitación: >120 BPM
   - Bajo estímulo: <40 BPM

### ❌ Alertas muy frecuentes (cada 10s)
**Esto NO debería pasar más. Si pasa:**
- Reinicia el backend Django (el cooldown está en memoria)
- Verifica que estés usando el `consumers.py` actualizado

### ❌ Marcadores no se pueden arrastrar
**Verificar:**
- Que el navegador es Chrome/Firefox/Edge (moderno)
- Que no hay errores en la consola del navegador (F12)
- Que estás en la versión correcta del `GeofenceEditor.js`

---

## 📊 VALORES DE REFERENCIA

### Rangos Normales por Especie:
| Especie | Temp Normal | Temp Alerta | BPM Normal | BPM Alerta |
|---------|-------------|-------------|------------|------------|
| **OVINO** | 38.5-39.5°C | <37.5 o >40 | 70-90 | <40 o >120 |
| **BOVINO** | 38.0-39.0°C | <37.0 o >39.5 | 60-80 | <40 o >90 |
| **EQUINO** | 37.5-38.5°C | <36.5 o >39.0 | 28-40 | <25 o >55 |

### Cooldowns:
- **Temperatura**: 90 segundos
- **Frecuencia Cardíaca**: 90 segundos
- **Perímetro**: 30 segundos

---

## ✨ CARACTERÍSTICAS IMPLEMENTADAS

### Alertas Inteligentes:
- [x] Solo para animales CON geocerca asignada
- [x] Cooldown para evitar spam
- [x] Variación entre diferentes animales
- [x] Logs descriptivos con valores
- [x] Creación de AlertaUsuario automática
- [x] Notificaciones en frontend

### Editor de Geocercas:
- [x] Visualización de todas las geocercas
- [x] Edición de vértices mediante arrastre
- [x] Vista previa de cambios
- [x] Aplicar/Descartar cambios
- [x] Reposicionamiento automático de animales
- [x] Indicadores visuales claros
- [x] Diseño responsive

---

## 📝 NOTAS FINALES

1. **El sistema de cooldown está en memoria**: Si reinicias Django, se resetea
2. **Animales sin geocerca NO generan alertas**: Es comportamiento esperado
3. **El simulador V8 tiene su propio cooldown local**: Solo para los logs, la BD usa el del consumer
4. **Las coordenadas de geocerca se guardan en formato JSON**: {lat, lng} para cada vértice
5. **El reposicionamiento de animales es automático**: No requiere acción manual

---

## 🎓 PRÓXIMOS PASOS SUGERIDOS

1. **Probar con usuarios reales**: Ver cómo diferentes usuarios reciben alertas
2. **Ajustar cooldowns si es necesario**: Los valores actuales son conservadores
3. **Monitorear rendimiento**: Con muchos animales, revisar carga del sistema
4. **Implementar notificaciones push**: Para alertas críticas
5. **Dashboard de estadísticas**: Gráficos de alertas por tiempo/tipo/animal

---

**¡Todo listo para producción!** 🚀

Si encuentras algún problema, revisa:
1. Los logs del backend (Terminal 1)
2. Los logs del simulador (Terminal 3)
3. La consola del navegador (F12 → Console)
4. Ejecuta `test_alerts.py` para diagnóstico completo

---

**Desarrollado por: CAMPORT Team**  
**Versión: 8.1.0**  
**Estado: ✅ Production Ready**
