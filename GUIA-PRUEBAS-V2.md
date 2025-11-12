# 🧪 Guía de Pruebas - CAMPORT V2.0

## 📋 Preparativos

### 1. Iniciar el Sistema

**Terminal 1 - Backend:**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm start
```

**Terminal 3 - Simulador (Opcional):**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python simulator.py
```

### 2. Credenciales de Prueba

Asegúrate de tener un usuario administrador creado. Si no, créalo:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py createsuperuser
```

---

## ✅ Pruebas de Funcionalidad

### PRUEBA 1: Botón de Administración

**Objetivo:** Verificar que el botón "Panel de Administración" aparece solo para usuarios staff.

**Pasos:**
1. Iniciar sesión con usuario regular (non-staff)
2. ✅ Verificar que NO aparece el botón "⚙️ Panel de Administración"
3. Cerrar sesión
4. Iniciar sesión con usuario administrador (staff)
5. ✅ Verificar que SÍ aparece el botón "⚙️ Panel de Administración"
6. Click en el botón
7. ✅ Verificar que navega a `/admin`

**Resultado esperado:** El botón solo es visible para usuarios staff y navega correctamente.

---

### PRUEBA 2: Generación Automática de Display ID

**Objetivo:** Verificar que los IDs de display se generan automáticamente con el formato correcto.

**Pasos:**
1. Ir al Panel de Administración
2. Click en "Gestión de Ganado"
3. Click en "+ Nuevo Animal"
4. Llenar formulario:
   - Collar ID: `TEST-OVINO-001`
   - Tipo: Ovino
   - Raza: Suffolk
   - Edad: 2
   - Peso: 60
   - Sexo: Macho
   - Color: Blanco
5. Guardar
6. ✅ Verificar en la tabla que aparece un "ID Display" con formato `OVINO-XXX`
7. Crear otro animal del mismo tipo
8. ✅ Verificar que el número se incrementa (ej: `OVINO-002`)
9. Crear un animal de tipo diferente (Bovino)
10. ✅ Verificar que inicia con `BOVINO-001`

**Resultado esperado:** 
- `display_id` se genera automáticamente
- Formato: `TIPO-XXX` (3 dígitos con ceros a la izquierda)
- Numeración independiente por tipo de animal

---

### PRUEBA 3: Crear Múltiples Geocercas

**Objetivo:** Verificar que se pueden crear múltiples geocercas.

**Pasos:**
1. Ir al Panel de Administración
2. Click en "Editor de Geocercas"
3. ✅ Verificar que muestra lista de geocercas existentes
4. Click en "+ Nueva Geocerca"
5. Ingresar nombre: "Zona Norte"
6. Click en "Crear"
7. ✅ Verificar que aparece en la lista
8. ✅ Verificar que tiene coordenadas por defecto
9. Repetir para crear "Zona Sur"
10. ✅ Verificar que ambas aparecen en la lista

**Resultado esperado:** 
- Se pueden crear múltiples geocercas
- Cada una tiene su propio nombre e ID
- Aparecen en la lista de geocercas disponibles

---

### PRUEBA 4: Editar Vértices de Geocerca

**Objetivo:** Verificar que se pueden editar los vértices de una geocerca.

**Pasos:**
1. En el Editor de Geocercas, seleccionar una geocerca
2. ✅ Verificar que se muestra el mapa con el polígono
3. ✅ Verificar que aparecen marcadores en cada vértice
4. Click en uno de los marcadores (vértices)
5. ✅ Verificar que se abre un modal con un minimapa
6. Click en una nueva ubicación en el minimapa
7. ✅ Verificar que aparece un marcador en la nueva ubicación
8. ✅ Verificar que muestra las coordenadas seleccionadas
9. Click en "Guardar"
10. ✅ Verificar que el modal se cierra
11. ✅ Verificar que el polígono se actualiza en el mapa principal
12. ✅ Verificar mensaje de éxito

**Resultado esperado:**
- Modal se abre al hacer click en vértice
- Se puede seleccionar nueva ubicación en minimapa
- Cambios se guardan y se reflejan en el mapa
- Mensaje de confirmación aparece

---

### PRUEBA 5: Asignar Animal a Geocerca

**Objetivo:** Verificar que se pueden asignar animales a geocercas específicas.

**Pasos:**
1. Ir a "Gestión de Ganado"
2. Click en editar (✏️) de un animal
3. ✅ Verificar que aparece dropdown "Geocerca Asignada"
4. ✅ Verificar que lista todas las geocercas creadas
5. Seleccionar una geocerca
6. Guardar
7. ✅ Verificar que en la tabla aparece el nombre de la geocerca
8. Ir al Dashboard principal
9. ✅ Verificar que el animal muestra la geocerca en su información
10. Click en el animal en la lista
11. ✅ Verificar que en el panel de detalles muestra "Geocerca Asignada"

**Resultado esperado:**
- Dropdown muestra todas las geocercas
- Asignación se guarda correctamente
- Se muestra en tabla y dashboard

---

### PRUEBA 6: Visualización de Múltiples Geocercas

**Objetivo:** Verificar que el mapa muestra todas las geocercas simultáneamente.

**Pasos:**
1. Ir al Dashboard principal
2. ✅ Verificar que el mapa muestra todas las geocercas creadas
3. ✅ Verificar que cada geocerca tiene un color diferente
4. ✅ Verificar que cada geocerca muestra su nombre en tooltip
5. Hacer zoom in/out
6. ✅ Verificar que los polígonos se mantienen visibles

**Resultado esperado:**
- Todas las geocercas se muestran simultáneamente
- Diferentes colores para distinguirlas
- Tooltips con nombres

---

### PRUEBA 7: Alertas por Geocerca Asignada

**Objetivo:** Verificar que las alertas de perímetro usan la geocerca asignada al animal.

**Prerequisito:** Tener simulador corriendo o datos de telemetría en tiempo real.

**Pasos:**
1. Asignar un animal a una geocerca específica
2. Iniciar simulador o enviar telemetría
3. Simular movimiento fuera de la geocerca asignada
4. ✅ Verificar que se genera alerta de perímetro
5. ✅ Verificar que el mensaje menciona:
   - El display_id del animal
   - El nombre de la geocerca
6. Click en la campana de notificaciones
7. ✅ Verificar que la alerta aparece

**Resultado esperado:**
- Alerta se genera solo cuando sale de SU geocerca
- Mensaje incluye display_id y nombre de geocerca
- Aparece en notificaciones

---

### PRUEBA 8: Activar/Desactivar Geocerca

**Objetivo:** Verificar que se puede cambiar el estado de las geocercas.

**Pasos:**
1. Ir al Editor de Geocercas
2. Seleccionar una geocerca activa
3. ✅ Verificar que el badge muestra "Activa" en verde
4. Click en botón "🔴 Desactivar"
5. ✅ Verificar mensaje de confirmación
6. ✅ Verificar que el badge cambia a "Inactiva" en gris
7. Click en botón "🟢 Activar"
8. ✅ Verificar que vuelve a estado activo

**Resultado esperado:**
- Estado cambia correctamente
- Badge se actualiza
- Mensaje de confirmación

---

### PRUEBA 9: Eliminar Geocerca

**Objetivo:** Verificar que se pueden eliminar geocercas con confirmación.

**Pasos:**
1. Crear una geocerca de prueba ("Zona Temporal")
2. Click en botón "🗑️ Eliminar"
3. ✅ Verificar que aparece diálogo de confirmación
4. Click en "Cancelar"
5. ✅ Verificar que la geocerca NO se elimina
6. Click en "🗑️ Eliminar" nuevamente
7. Click en "Aceptar/OK"
8. ✅ Verificar que la geocerca desaparece de la lista
9. ✅ Verificar mensaje de éxito

**Resultado esperado:**
- Confirmación antes de eliminar
- Eliminación exitosa tras confirmación
- Geocerca desaparece de lista

---

### PRUEBA 10: Información de Animales en Geocerca

**Objetivo:** Verificar que se muestra cuántos animales tiene cada geocerca.

**Pasos:**
1. Asignar 3 animales a "Zona Norte"
2. Asignar 2 animales a "Zona Sur"
3. Ir al Editor de Geocercas
4. ✅ Verificar que "Zona Norte" muestra "Animales: 3"
5. ✅ Verificar que "Zona Sur" muestra "Animales: 2"
6. En Gestión de Ganado, verificar dropdown
7. ✅ Verificar que muestra: "Zona Norte (3 animales)"

**Resultado esperado:**
- Contador de animales correcto
- Se actualiza al asignar/desasignar
- Visible en editor y formularios

---

## 🔍 Pruebas de Integración

### INT-1: Flujo Completo de Gestión

**Escenario:** Un administrador configura una nueva zona de pastoreo.

**Pasos:**
1. Crear geocerca "Zona de Primavera"
2. Editar vértices para ajustar área
3. Crear 5 animales nuevos
4. Asignar los 5 animales a la nueva geocerca
5. Verificar en mapa que:
   - Aparece la geocerca
   - Animales tienen indicador de geocerca
6. Iniciar simulador
7. Verificar que alertas funcionan con la nueva geocerca

**Resultado esperado:** Sistema completo funcional end-to-end.

---

### INT-2: Migración de Animales entre Geocercas

**Escenario:** Mover animales de una geocerca a otra.

**Pasos:**
1. Tener 3 animales en "Zona A"
2. Verificar contador: "Zona A (3 animales)"
3. Editar un animal y cambiar a "Zona B"
4. Guardar
5. ✅ Verificar: "Zona A (2 animales)"
6. ✅ Verificar: "Zona B (1 animal)"
7. Verificar en mapa que el animal muestra nueva geocerca

**Resultado esperado:** Contadores se actualizan, visualización correcta.

---

## 🐛 Pruebas de Casos Edge

### EDGE-1: Animal sin Geocerca

**Pasos:**
1. Crear animal sin asignar geocerca
2. ✅ Verificar que se guarda correctamente
3. ✅ Verificar que en tabla muestra "Sin asignar"
4. Iniciar simulador
5. ✅ Verificar que NO genera alertas de perímetro

**Resultado esperado:** Funciona sin errores, no genera alertas de perímetro.

---

### EDGE-2: Geocerca sin Animales

**Pasos:**
1. Crear geocerca sin asignar animales
2. ✅ Verificar que muestra "Animales: 0"
3. ✅ Verificar que se puede editar normalmente
4. ✅ Verificar que aparece en mapa

**Resultado esperado:** Funciona normalmente sin animales.

---

### EDGE-3: Eliminar Geocerca con Animales

**Pasos:**
1. Crear geocerca con 2 animales asignados
2. Intentar eliminar
3. ✅ Verificar confirmación
4. Confirmar eliminación
5. ✅ Verificar que animales quedan como "Sin asignar"
6. ✅ Verificar que animales NO se eliminan

**Resultado esperado:** Animales se mantienen, geocerca se establece a null (CASCADE SET_NULL).

---

## 📊 Checklist de Validación Final

### Backend
- [ ] Modelo Animal tiene campo `display_id`
- [ ] Modelo Animal tiene FK a Geocerca
- [ ] Display IDs se generan automáticamente
- [ ] API `/api/geocercas/` retorna todas las geocercas
- [ ] API permite CRUD completo de geocercas
- [ ] Alertas usan geocerca asignada al animal
- [ ] Mensajes de alerta incluyen display_id

### Frontend
- [ ] Botón "Panel de Administración" visible para staff
- [ ] Botón navega a `/admin`
- [ ] Título muestra "CAMPORT"
- [ ] Mapa muestra múltiples geocercas
- [ ] Geocercas tienen colores diferentes
- [ ] Geocercas muestran tooltips con nombre
- [ ] Editor de geocercas lista todas las geocercas
- [ ] Se puede crear nueva geocerca
- [ ] Se puede editar vértices con modal
- [ ] Se puede activar/desactivar geocerca
- [ ] Se puede eliminar geocerca
- [ ] Formulario de animal tiene dropdown de geocerca
- [ ] Tabla de animales muestra display_id
- [ ] Tabla de animales muestra geocerca asignada
- [ ] Dashboard muestra geocerca en info de animal
- [ ] Contadores de animales por geocerca funcionan

### Integración
- [ ] Simulador funciona con nuevos campos
- [ ] WebSocket envía/recibe datos correctamente
- [ ] Alertas aparecen en NotificationBell
- [ ] Mapas se renderizan correctamente
- [ ] No hay errores en consola del navegador
- [ ] No hay errores en logs del backend

---

## 🎯 Criterios de Éxito

El sistema se considera completamente funcional si:

1. ✅ Todos los tests básicos (1-10) pasan
2. ✅ Pruebas de integración funcionan
3. ✅ Casos edge no generan errores
4. ✅ Checklist de validación está 100% completo
5. ✅ No hay errores en consolas (navegador/backend)
6. ✅ Performance es aceptable (<2s carga inicial)

---

## 📞 Reporte de Problemas

Si encuentras algún problema durante las pruebas:

1. Anota el número de prueba
2. Describe el comportamiento esperado vs. observado
3. Incluye screenshots si es posible
4. Revisa logs de consola (F12 en navegador)
5. Revisa logs del backend (terminal)

---

**Fecha:** 11 de Noviembre, 2025
**Versión del Sistema:** CAMPORT V2.0
**Estado:** ✅ Listo para Pruebas
