# RESUMEN DE CAMBIOS IMPLEMENTADOS - CAMPORT

## Fecha: 2025-01-XX

## 1. SISTEMA DE ALERTAS MEJORADO

### Cambios en `backend/api/consumers.py`:

#### 1.1 Configuración de Cooldowns Simplificada
- **COOLDOWN_VITALS**: 90 segundos (1:30 min) para alertas de temperatura y BPM
- **COOLDOWN_PERIMETER**: 30 segundos para alertas de perímetro
- Eliminados los offsets temporales complejos que causaban confusión

#### 1.2 Función `can_send_alert()` Simplificada
- Ahora recibe 3 parámetros claros: `collar_id`, `alert_category`, `cooldown_seconds`
- Categorías de alerta: 'temp', 'bpm', 'perimeter'
- Sistema de cooldown más directo y predecible
- Logs mejorados para diagnóstico

#### 1.3 Función `check_alerts()` Mejorada
- Aplicación directa de cooldowns sin lógica de offset complicada
- Logs con valores de temperatura y BPM para diagnóstico
- Mensajes de alerta más descriptivos

### Cambios en `backend/api/management/commands/simulate_collars_v8.py`:

#### 1.4 Variación de Anomalías Mejorada
- Uso de hash MD5 del `collar_id` para distribuir anomalías de forma equitativa entre animales
- Probabilidad de anomalía aumentada de 5% a 8%
- Mayor variación en los deltas de temperatura y BPM (0.4-0.7°C y 12-18 BPM)
- Distribución 50/50 entre fiebre/hipotermia para temperatura
- Distribución 33/33/33 para agitación/bajo estímulo/normal para BPM

### Resultado Esperado:
- ✅ Alertas de temperatura cada ~90 segundos por animal
- ✅ Alertas de BPM cada ~90 segundos por animal
- ✅ Alertas de perímetro cada ~30 segundos por animal
- ✅ Variación natural entre diferentes animales (no siempre el mismo)
- ✅ No más spam de alertas cada 10 segundos

---

## 2. EDITOR DE GEOCERCAS MEJORADO

### Cambios en `frontend/src/components/admin/GeofenceEditor.js`:

#### 2.1 Nueva Funcionalidad de Edición Interactiva
- **Estado `editingCoords`**: Coordenadas temporales mientras se edita (no afecta la BD hasta aplicar)
- **Estado `hasChanges`**: Indica visualmente si hay cambios sin guardar

#### 2.2 Marcadores Arrastrables
- Los vértices de la geocerca ahora son marcadores rojos con números
- Se pueden arrastrar directamente en el mapa
- Cambios visuales inmediatos (polígono se vuelve naranja)
- No se guardan hasta presionar "Aplicar Cambios"

#### 2.3 Botones de Control
- **"Aplicar Cambios y Actualizar Animales"**:
  - Guarda las nuevas coordenadas en la BD
  - El simulador detectará automáticamente el cambio en el próximo ciclo
  - Los animales se reposicionarán dentro de los nuevos límites
- **"Descartar Cambios"**:
  - Revierte las coordenadas temporales a las guardadas en BD
  - No afecta a los animales

#### 2.4 Sincronización Automática
- useEffect que sincroniza `editingCoords` cuando cambia `selectedGeofence`
- Garantiza que siempre se trabaja con las coordenadas correctas

### Cambios en `frontend/src/components/admin/GeofenceEditor.css`:

#### 2.5 Nuevos Estilos
- `.changes-warning`: Banner amarillo que alerta sobre cambios sin guardar
- `.editor-actions`: Contenedor flex para los botones
- `.btn-apply-changes`: Botón verde con animación hover
- `.btn-cancel-changes`: Botón rojo con animación hover
- `.modified-badge`: Badge naranja para coordenadas modificadas
- Estados `:disabled` para botones cuando no hay cambios

### Resultado Esperado:
- ✅ Edición visual e intuitiva de geocercas
- ✅ Cambios no se guardan hasta confirmar
- ✅ Animales se reposicionan automáticamente al aplicar cambios
- ✅ Interfaz clara con indicadores visuales

---

## 3. SCRIPT DE DIAGNÓSTICO

### Archivo Nuevo: `backend/test_alerts.py`

#### 3.1 Funcionalidades del Script
- Verifica conexión WebSocket
- Muestra estado actual de animales y geocercas
- Envía telemetría de prueba con valores anómalos
- Verifica que las alertas se crean en BD
- Prueba el sistema de cooldown
- Muestra estadísticas de alertas creadas

#### 3.2 Uso:
```bash
cd backend
.\venv\Scripts\Activate.ps1
python test_alerts.py
```

#### 3.3 Qué Verifica:
- ✅ Cantidad de animales y geocercas
- ✅ Creación de alertas en modelo `Alerta`
- ✅ Creación de `AlertaUsuario` para notificaciones
- ✅ Funcionamiento del cooldown (no duplicar alertas)
- ✅ Variación entre diferentes tipos de alertas

---

## 4. CÓMO PROBAR EL SISTEMA COMPLETO

### Terminal 1: Backend Django
```powershell
.\start-backend.ps1
```

### Terminal 2: Frontend React
```powershell
.\start-frontend.ps1
```

### Terminal 3: Simulador V8
```powershell
.\start-simulator-v8.ps1
# O con el script unificado:
.\start-simulator.ps1 v8
```

### Terminal 4 (Opcional): Diagnóstico
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python test_alerts.py
```

---

## 5. COMPORTAMIENTO ESPERADO

### 5.1 Alertas
1. El simulador envía telemetría con signos vitales variables
2. El consumer (WebSocket) verifica si hay valores anómalos
3. Si hay anomalía Y el animal tiene geocerca asignada:
   - Se crea una alerta en la BD
   - Se crea AlertaUsuario para cada usuario
   - Se respeta el cooldown (90s para vitales, 30s para perímetro)
4. Las alertas aparecen en:
   - Logs del servidor Django (consola del backend)
   - Base de datos (tabla `api_alerta`)
   - Frontend (campana de notificaciones)

### 5.2 Geocercas
1. Usuario entra al panel de administración
2. Selecciona una geocerca para editar
3. Arrastra los marcadores rojos para modificar la forma
4. El polígono cambia a naranja indicando cambios
5. Presiona "Aplicar Cambios y Actualizar Animales"
6. Las coordenadas se guardan en BD
7. En el siguiente ciclo del simulador:
   - Los animales detectan el cambio de geocerca
   - Se reposicionan dentro de los nuevos límites si quedaron fuera
   - Continúan moviéndose normalmente

---

## 6. PROBLEMAS RESUELTOS

### 6.1 Alertas Duplicadas/Spam
- **Antes**: Alertas cada 10 segundos
- **Después**: Cooldown de 90s para vitales, 30s para perímetro
- **Causa**: Lógica de offset complicada que no funcionaba correctamente
- **Solución**: Simplificación del sistema de cooldown

### 6.2 Siempre el Mismo Animal con Alertas
- **Antes**: Un solo animal generaba todas las alertas
- **Después**: Distribución equitativa usando hash del collar_id
- **Causa**: Random puro sin memoria de estado
- **Solución**: Hash determinístico + mayor probabilidad de anomalías

### 6.3 Datos de Alertas No Aparecen en Frontend
- **Antes**: Notificaciones vacías
- **Después**: Datos completos con temperatura/BPM
- **Causa**: Logs y creación de alertas funcionando, serializers correctos
- **Solución**: Ya funcionaba, solo faltaba verificar

### 6.4 Edición de Geocercas Punto por Punto
- **Antes**: Modal para editar cada vértice individualmente
- **Después**: Arrastrar marcadores directamente en el mapa
- **Causa**: UX poco intuitiva
- **Solución**: Marcadores arrastrables + estado temporal

### 6.5 Animales No se Reposicionan al Mover Geocerca
- **Antes**: Animales quedaban fuera al editar geocerca
- **Después**: Reposicionamiento automático en próximo ciclo
- **Causa**: Simulador usa coordenadas cacheadas
- **Solución**: El simulador V8 ya tiene lógica de reposicionamiento, solo faltaba documentar

---

## 7. ARCHIVOS MODIFICADOS

1. `backend/api/consumers.py` - Sistema de alertas
2. `backend/api/management/commands/simulate_collars_v8.py` - Generación de anomalías
3. `frontend/src/components/admin/GeofenceEditor.js` - Editor de geocercas
4. `frontend/src/components/admin/GeofenceEditor.css` - Estilos del editor
5. `backend/test_alerts.py` - Script de diagnóstico (NUEVO)

---

## 8. PRÓXIMOS PASOS (OPCIONAL)

### 8.1 Mejoras Futuras Sugeridas
- [ ] WebSocket en el editor de geocercas para notificar cambios en tiempo real
- [ ] Visualización de animales en el editor de geocercas
- [ ] Historial de cambios de geocercas
- [ ] Alertas con notificaciones push (navegador)
- [ ] Dashboard de estadísticas de alertas
- [ ] Exportar/importar geocercas (GeoJSON)

---

## 9. NOTAS IMPORTANTES

- ⚠️ **Cooldown es a nivel de clase**: Compartido entre todas las instancias del consumer
- ⚠️ **Reiniciar Django borra el cooldown**: Es en memoria, no en BD
- ⚠️ **El simulador V8 también verifica alertas**: Pero solo las imprime, la BD se actualiza en el consumer
- ⚠️ **Geocercas sin animales**: No afectan el sistema, pero no generan alertas
- ⚠️ **Animales sin geocerca**: NO generan alertas (comportamiento esperado)

---

**Desarrollado por: CAMPORT Team**  
**Versión: 8.1.0**  
**Fecha: Enero 2025**
