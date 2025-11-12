# 🚀 CAMPORT V2.0 - Guía Rápida de Cambios

## 📋 Cambios Principales en 30 Segundos

| Característica | V1.0 | V2.0 |
|----------------|------|------|
| **Nombre del Sistema** | Monitor de Ganado | **CAMPORT** |
| **ID de Animales** | collar_id (HW-12345) | **display_id** (OVINO-001) |
| **Geocercas** | 1 geocerca global | **Múltiples geocercas** |
| **Asignación** | Todos en misma zona | **Individual por animal** |
| **Editor** | Vista básica | **Editor interactivo con mapa** |
| **Acceso Admin** | URL manual | **Botón en navbar** |
| **Alertas** | Genéricas | **Con display_id y nombre de geocerca** |
| **Visualización** | 1 polígono azul | **Múltiples polígonos con colores** |

---

## 🆕 Funcionalidades Nuevas

### 1. IDs Automáticos (display_id)
```
Antes: HW-12345, HW-67890, HW-11111
Ahora: OVINO-001, OVINO-002, BOVINO-001
```
✅ Generación automática
✅ Formato legible: TIPO-XXX
✅ Numeración por tipo de animal

---

### 2. Múltiples Geocercas

**Crear:**
```
Panel Admin → Editor de Geocercas → + Nueva Geocerca
```

**Editar Vértices:**
```
Seleccionar geocerca → Click en vértice → Modal con minimapa → Seleccionar nueva ubicación → Guardar
```

**Gestionar:**
- ✅ Activar/Desactivar
- ✅ Eliminar (con confirmación)
- ✅ Ver cantidad de animales

---

### 3. Asignar Animal a Geocerca

**En Formulario:**
```
Gestión de Ganado → Editar Animal → Dropdown "Geocerca Asignada" → Seleccionar → Guardar
```

**Resultado:**
- Muestra nombre en tabla
- Muestra en dashboard
- Alertas específicas a esa geocerca

---

### 4. Botón de Administración

**Ubicación:** Navbar superior (solo para staff)

**Texto:** `⚙️ Panel de Administración`

**Acción:** Navega a `/admin`

---

### 5. Alertas Mejoradas

**Formato Anterior:**
```
"Animal fuera del perímetro permitido"
```

**Formato Nuevo:**
```
"Animal OVINO-003 fuera de geocerca 'Zona Norte'"
```

Incluye:
- ✅ Display ID del animal
- ✅ Nombre de la geocerca
- ✅ Solo alerta si sale de SU geocerca

---

## 🎨 Cambios en la Interfaz

### Dashboard Principal
- Título: **"CAMPORT - Monitor de Ganado en Tiempo Real"**
- Botón admin visible para staff
- Muestra display_id en lugar de collar_id
- Info de geocerca en cada animal

### Tabla de Animales
```
| ID Display | Collar ID | Tipo | Raza | Edad | Peso | Sexo | Geocerca | Acciones |
|------------|-----------|------|------|------|------|------|----------|----------|
| OVINO-001  | HW-12345  | ...  | ...  | ...  | ...  | ...  | Zona A   | ✏️ 🗑️   |
```

### Editor de Geocercas
```
┌─────────────────┬───────────────────────────────┐
│ Lista           │ Mapa y Detalles               │
│                 │                               │
│ + Nueva         │ [Mapa con polígono]           │
│                 │                               │
│ ┌─────────────┐ │ Coordenadas:                  │
│ │ Zona Norte  │ │ Punto 1: -38.8440, -72.2946  │
│ │ 3 animales  │ │ Punto 2: -38.8450, -72.2946  │
│ │ ● Activa    │ │ ...                           │
│ │ 🔴 🗑️       │ │                               │
│ └─────────────┘ │                               │
└─────────────────┴───────────────────────────────┘
```

---

## 🔧 API Endpoints Nuevos/Modificados

### Geocercas
```
GET    /api/geocercas/              # Lista TODAS (antes: solo activa)
POST   /api/geocercas/              # Crear nueva
GET    /api/geocercas/:id/          # Ver una
PUT    /api/geocercas/:id/          # Actualizar (incluso vértices)
DELETE /api/geocercas/:id/          # Eliminar
GET    /api/geocercas/activa/       # Solo activas (compatible)
```

### Animales
```
GET    /api/animales/               # Incluye display_id, geocerca
POST   /api/animales/               # Puede incluir geocerca_id
PUT    /api/animales/:id/           # Puede actualizar geocerca
```

**Ejemplo Response:**
```json
{
  "collar_id": "HW-12345",
  "display_id": "OVINO-001",
  "tipo_animal": "OVINO",
  "geocerca": 1,
  "geocerca_nombre": "Zona Norte",
  ...
}
```

---

## 📱 Flujos de Usuario Comunes

### Administrador: Configurar Nueva Zona

1. Login como staff
2. Click en "⚙️ Panel de Administración"
3. Click en "Editor de Geocercas"
4. Click en "+ Nueva Geocerca"
5. Ingresar nombre (ej: "Zona de Verano")
6. Click en "Crear"
7. Ajustar vértices si es necesario:
   - Click en un marcador del polígono
   - Click en nueva ubicación en minimapa
   - Click en "Guardar"
8. Ir a "Gestión de Ganado"
9. Asignar animales a la nueva geocerca

**Tiempo estimado:** 2-3 minutos

---

### Administrador: Migrar Animales entre Zonas

1. Ir a "Gestión de Ganado"
2. Click en editar (✏️) del animal
3. Cambiar "Geocerca Asignada"
4. Click en "Actualizar"
5. Verificar en tabla que muestra nueva geocerca

**Tiempo estimado:** 30 segundos por animal

---

### Usuario Regular: Monitorear Animales

1. Login
2. Ver mapa con todas las geocercas (colores diferentes)
3. Click en animal en lista izquierda
4. Ver panel de detalles con:
   - Display ID (ej: OVINO-003)
   - Geocerca asignada
   - Telemetría actual
5. Revisar notificaciones (🔔)

**Visualización continua en tiempo real**

---

## 🐛 Solución Rápida de Problemas

### Display ID no se genera

**Síntoma:** Animal creado sin display_id

**Solución:**
```python
# En Django shell
python manage.py shell
>>> from api.models import Animal
>>> for animal in Animal.objects.filter(display_id=''):
...     animal.save()  # Fuerza regeneración
```

---

### Geocerca no aparece en mapa

**Checklist:**
- ✅ ¿Geocerca está activa? (verificar badge)
- ✅ ¿Tiene coordenadas válidas? (min 3 puntos)
- ✅ ¿Coordenadas están en formato correcto? `{lat: X, lng: Y}`
- ✅ Refrescar página (Ctrl+R)

---

### Alertas no se generan

**Checklist:**
- ✅ ¿Animal tiene geocerca asignada?
- ✅ ¿Geocerca está activa?
- ✅ ¿WebSocket conectado? (ver indicador en header)
- ✅ ¿Simulador enviando datos?

---

### Botón Admin no aparece

**Checklist:**
- ✅ Usuario tiene `is_staff=True`?
- ✅ Sesión activa?
- ✅ Refrescar página
- ✅ Verificar consola de navegador (F12)

**Solución:**
```python
# Django shell
from api.models import User
user = User.objects.get(username='tu_usuario')
user.is_staff = True
user.save()
```

---

## 💡 Tips y Trucos

### Tip 1: Colores de Geocercas
Los colores se asignan automáticamente basados en el nombre. Geocercas con nombres similares tendrán colores similares.

### Tip 2: Contadores en Tiempo Real
Los contadores de "X animales" se actualizan automáticamente al asignar/desasignar.

### Tip 3: Atajos de Teclado
- `Ctrl+R`: Refrescar datos
- `Esc`: Cerrar modales
- `Click fuera del modal`: También cierra modal

### Tip 4: Búsqueda Rápida
En tabla de animales, usa `Ctrl+F` del navegador para buscar por display_id, tipo, o geocerca.

### Tip 5: Exportar Coordenadas
Para backup de geocercas:
```python
python manage.py shell
>>> from api.models import Geocerca
>>> import json
>>> for g in Geocerca.objects.all():
...     print(f"{g.nombre}: {json.dumps(g.coordenadas)}")
```

---

## 📊 Comandos Útiles

### Ver Animales y sus Geocercas
```python
python manage.py shell
>>> from api.models import Animal
>>> for a in Animal.objects.all():
...     print(f"{a.display_id} → {a.geocerca.nombre if a.geocerca else 'Sin asignar'}")
```

### Contar Animales por Geocerca
```python
>>> from api.models import Geocerca
>>> for g in Geocerca.objects.all():
...     print(f"{g.nombre}: {g.animales.count()} animales")
```

### Listar Geocercas
```python
>>> for g in Geocerca.objects.all():
...     print(f"ID: {g.id}, Nombre: {g.nombre}, Activa: {g.activa}")
```

---

## 🎯 Checklist Post-Instalación

Después de actualizar a V2.0, verificar:

- [ ] Backend inicia sin errores
- [ ] Frontend compila exitosamente
- [ ] Migración aplicada (`0002_animal_display_id_animal_geocerca`)
- [ ] Animales existentes tienen display_id
- [ ] Botón admin visible para usuarios staff
- [ ] Se pueden crear nuevas geocercas
- [ ] Se pueden editar vértices
- [ ] Se pueden asignar animales a geocercas
- [ ] Mapa muestra múltiples geocercas
- [ ] Alertas incluyen display_id y nombre de geocerca
- [ ] Contador de animales funciona

---

## 🔗 Enlaces Rápidos

- **Documentación Completa:** `CAMBIOS-V2.md`
- **Guía de Pruebas:** `GUIA-PRUEBAS-V2.md`
- **Resumen Ejecutivo:** `RESUMEN-V2.md`
- **Especificaciones:** `Actualizacion_sistema.md`

---

## 📞 ¿Necesitas Ayuda?

1. Revisa esta guía rápida
2. Consulta `GUIA-PRUEBAS-V2.md` para casos específicos
3. Revisa `CAMBIOS-V2.md` para detalles técnicos
4. Contacta al equipo de desarrollo

---

**Versión:** CAMPORT V2.0
**Última Actualización:** 11 de Noviembre, 2025
**Estado:** ✅ Producción

---

¡Disfruta de CAMPORT V2.0! 🎉
