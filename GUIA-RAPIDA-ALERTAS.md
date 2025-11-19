# 🚀 GUÍA RÁPIDA - SISTEMA DE ALERTAS Y REPORTES

## 📝 CÓMO USAR EL NUEVO SISTEMA

### 1️⃣ INICIAR EL SISTEMA

#### Terminal 1: Backend
```powershell
cd "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO"
.\start-backend.ps1
```

#### Terminal 2: Frontend  
```powershell
cd "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO"
.\start-frontend.ps1
```

#### Terminal 3: Simulador V8 (Recomendado)
```powershell
cd "C:\Users\bale_\Videos\Proyecto Integrado Camport_NUEVO"
.\start-simulator.ps1 v8
```

**NOTA:** El simulador V8 tiene intervalos de alerta configurados para demostración:
- Alertas de signos vitales (Temp/BPM): cada 90 segundos (1:30 min)
- Alertas de perímetro: cada 30 segundos
- Los tres tipos tienen un desfase de 30 segundos entre sí para distribuir temporalmente

### 2️⃣ ACCEDER AL SISTEMA

1. Abrir navegador en `http://localhost:3000`
2. Iniciar sesión:
   - **Usuario:** admin
   - **Contraseña:** admin123

### 3️⃣ NAVEGAR A ALERTAS/REPORTES

**Opción A:** Desde el Dashboard Principal
1. Login exitoso → Dashboard
2. En el header, ver selector de vista: `🗺️ Mapa | 📋 Alertas/Reportes`
3. Click en `📋 Alertas/Reportes`

**Opción B:** Icono de Notificaciones
1. Click en el icono 🔔 en el header
2. Ver alertas recientes
3. Click en "Ver Todas" → Va a Alertas/Reportes

### 4️⃣ GESTIONAR ALERTAS ACTIVAS

#### Ver Alertas
- Pestaña "Alertas Activas" muestra todas las alertas sin resolver
- Cada tarjeta muestra:
  - Icono según tipo (🌡️ Temp, ❤️ BPM, 🚨 Perímetro)
  - Animal afectado
  - Mensaje de alerta
  - Valor que disparó la alerta
  - Fecha y hora
  - Badge "NUEVA" si no está leída

#### Marcar como Leída
1. Encontrar la alerta
2. Click en botón `✓ Marcar Leída`
3. La alerta se marca como leída (quita badge "NUEVA")

#### Eliminar Alerta (Falso Positivo)
1. Click en botón `🗑️ Eliminar`
2. Confirmar en el diálogo
3. La alerta desaparece de la vista (soft delete, no se pierde el registro)

#### Resolver y Mover a Reportes
1. Click en botón `📊 Resolver`
2. Se abre modal con:
   - Resumen de la alerta
   - Campo para observaciones (opcional)
   - Información sobre la acción
3. Escribir observaciones (ej: "Administrado medicamento X, animal recuperado")
4. Click en `✓ Resolver y Reportar`
5. La alerta se mueve al historial de reportes

### 5️⃣ VER HISTORIAL DE REPORTES

1. Click en pestaña `📊 Historial de Reportes`
2. Ver tabla con todas las alertas resueltas
3. Información mostrada:
   - ID del reporte
   - Tipo de alerta
   - Animal
   - Mensaje
   - Valor registrado
   - Fecha de la alerta
   - Fecha de resolución
   - Usuario que resolvió
   - Estado de exportación

### 6️⃣ EXPORTAR REPORTES EN XML

#### Exportar Todos los Reportes
1. En pestaña "Historial de Reportes"
2. Click en botón `📥 Exportar Todos (XML)`
3. El archivo se descarga automáticamente
4. Nombre del archivo: `reportes_camport_YYYYMMDD_HHMMSS.xml`

#### Exportar Reportes Filtrados
1. En sección "Filtros para Exportación"
2. Configurar filtros:
   - **Desde:** Fecha inicial (opcional)
   - **Hasta:** Fecha final (opcional)
   - **Tipo:** TEMPERATURA / FRECUENCIA / PERIMETRO (opcional)
   - **Animal ID:** (futuro)
3. Click en `📥 Exportar Filtrado (XML)`
4. Solo los reportes que cumplan los filtros se exportan

### 7️⃣ ESTRUCTURA DEL ARCHIVO XML

```xml
<?xml version="1.0" ?>
<reportes sistema="CAMPORT" fecha_exportacion="2025-01-18T15:30:00" total="5">
  <reporte id="1">
    <animal>
      <collar_id>OVINO-001</collar_id>
      <display_id>OVINO-1</display_id>
      <tipo>OVINO</tipo>
    </animal>
    <alerta>
      <tipo>TEMPERATURA</tipo>
      <mensaje>Fiebre detectada: 40.5°C (Animal: OVINO-1)</mensaje>
      <timestamp>2025-01-18T14:25:30</timestamp>
      <valor_registrado>40.5</valor_registrado>
      <fecha_resolucion>2025-01-18T15:10:00</fecha_resolucion>
    </alerta>
    <fecha_generacion>2025-01-18T15:10:00</fecha_generacion>
    <generado_por>admin</generado_por>
    <observaciones>Administrado antiinflamatorio, temperatura normalizada</observaciones>
    <exportado>true</exportado>
  </reporte>
  <!-- Más reportes... -->
</reportes>
```

---

## 🎯 FLUJO DE TRABAJO COMPLETO (EJEMPLO)

### Escenario: Alerta de Fiebre en OVINO-1

#### 1. **Simulador genera alerta**
```
🌡️🔥 ALERTA: OVINO-1 - FIEBRE: 40.5°C
```

#### 2. **Usuario recibe notificación**
- Aparece en icono 🔔 (muestra badge con número)
- Sonido de notificación (opcional, depende del navegador)

#### 3. **Usuario revisa la alerta**
- Dashboard → Click en "Alertas/Reportes"
- Ve tarjeta:
  ```
  ┌──────────────────┐
  │ 🌡️ TEMPERATURA  │
  │ OVINO-1 [NUEVA]  │
  │ Fiebre: 40.5°C   │
  │ 18/01/25 14:25   │
  │                  │
  │ [✓ Leída]        │
  │ [📊 Resolver]    │
  │ [🗑️ Eliminar]   │
  └──────────────────┘
  ```

#### 4. **Usuario marca como leída**
- Click en `✓ Marcar Leída`
- Badge "NUEVA" desaparece
- Contador de notificaciones 🔔 disminuye

#### 5. **Usuario atiende al animal**
- Revisa físicamente al animal
- Administra tratamiento
- Confirma que temperatura baja

#### 6. **Usuario resuelve la alerta**
- Click en `📊 Resolver`
- Modal se abre
- Escribe observaciones:
  ```
  "Animal OVINO-1 presentaba fiebre de 40.5°C.
   Se administró antiinflamatorio (Meloxicam 5mg).
   Después de 2 horas, temperatura normalizada a 38.5°C.
   Animal muestra comportamiento normal."
  ```
- Click en `✓ Resolver y Reportar`

#### 7. **Sistema mueve a reportes**
- Alerta desaparece de "Alertas Activas"
- Aparece en "Historial de Reportes"

#### 8. **Al final del día, exportar reportes**
- Pestaña "Historial de Reportes"
- Configurar filtros:
  - Desde: 18/01/2025
  - Hasta: 18/01/2025
  - Tipo: (todos)
- Click en `📥 Exportar Filtrado (XML)`
- Descargar archivo: `reportes_camport_filtrado_20250118_180000.xml`

#### 9. **Usar el XML para análisis**
- Importar en sistema de gestión
- Generar reportes para el veterinario
- Análisis estadístico
- Documentación regulatoria

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### No aparecen alertas
**Causas posibles:**
1. Simulador no está corriendo
2. Ningún animal tiene geocerca asignada
3. Valores están dentro de rangos normales

**Solución:**
```powershell
# Verificar que el simulador esté corriendo
# Ver consola del simulador, debe mostrar estadísticas cada 10s

# Verificar asignación de geocercas
cd backend
python diagnostico_completo.py
```

### Botón de exportar deshabilitado
**Causa:** No hay reportes para exportar

**Solución:** Resolver al menos una alerta primero

### Archivo XML no se descarga
**Causas posibles:**
1. Bloqueador de pop-ups activo
2. Configuración del navegador

**Solución:**
- Permitir descargas automáticas en el navegador
- Verificar consola del navegador (F12) por errores

### Alerta no se resuelve
**Causa:** Error de conectividad con backend

**Solución:**
- Verificar que backend esté corriendo
- Ver consola del navegador (F12)
- Verificar consola del backend por errores

---

## 📊 MONITOREO DEL SISTEMA

### Verificar Estado General
```powershell
cd backend
python diagnostico_completo.py
```

Esto muestra:
- ✅ Usuarios en el sistema
- ✅ Geocercas y animales asignados
- ✅ Última telemetría de cada animal
- ✅ Si están dentro/fuera de geocerca
- ✅ Alertas activas y resueltas
- ✅ Distribución de alertas por tipo

### Ver Logs del Simulador
La consola del simulador muestra:
```
━━━ ESTADÍSTICAS CICLO #15 ━━━
  ✅ BOVINO-001: Temp=38.3°C | BPM=68 | Pos=(-38.84451, -72.29408)
  ✅ BOVINO-002🐑: Temp=38.7°C | BPM=72 | Pos=(-38.84382, -72.30627)
  🌡️🔥 ALERTA: EQUINO-001 - FIEBRE: 40.2°C
  ✅ EQUINO-001: Temp=40.2°C | BPM=35 | Pos=(-38.84380, -72.30661)
```

### Ver Logs del Backend
La consola del backend muestra cuando se crean alertas:
```
🌡️🔥 ALERTA CREADA EN BD: Fiebre detectada: 40.2°C (Animal: EQUINO-001) - Temp: 40.2°C
❤️⚡ ALERTA CREADA EN BD: Agitación: 105 BPM (Animal: OVINO-2) - BPM: 105
🚨 ALERTA CREADA EN BD: Animal BOVINO-1 fuera de geocerca "Perímetro Principal"
```

---

## 🎓 MEJORES PRÁCTICAS

### 1. **Revisión Regular de Alertas**
- Revisar al menos cada hora durante el día
- Configurar notificaciones sonoras
- Priorizar alertas de TEMPERATURA (salud crítica)

### 2. **Documentación en Observaciones**
- Ser específico en las acciones tomadas
- Incluir medicamentos/dosis si aplica
- Registrar hora de seguimiento
- Incluir resultado del tratamiento

### 3. **Exportación Periódica**
- Exportar reportes diariamente
- Mantener respaldo de archivos XML
- Usar filtros para reportes específicos
- Archivar por mes/año

### 4. **Gestión de Falsos Positivos**
- Usar botón "Eliminar" solo para falsos positivos confirmados
- No eliminar alertas sin verificar
- Si hay duda, marcar como leída y resolver después

### 5. **Análisis de Tendencias**
- Revisar reportes exportados semanalmente
- Identificar animales con alertas frecuentes
- Ajustar umbrales si es necesario
- Coordinar con veterinario

---

## 📞 SOPORTE

### Documentación Completa
- `SISTEMA-ALERTAS-REPORTES.md` - Documentación técnica completa
- `INICIO-RAPIDO-SIMULADORES.md` - Guía de simuladores
- `DOCUMENTACION.md` - Documentación general

### Scripts Útiles
- `diagnostico_completo.py` - Diagnóstico del sistema
- `start-backend.ps1` - Iniciar backend
- `start-frontend.ps1` - Iniciar frontend
- `start-simulator.ps1` - Iniciar simulador unificado

---

**Desarrollado con ❤️ por CAMPORT Team**  
**Versión:** 9.0.0  
**Fecha:** Enero 2025

🐑 Simplificando la gestión ganadera 🐑
