# 🖼️ Guía Visual de la Aplicación

## 📱 Pantallas Principales

### 1. Pantalla de Login
**Ruta:** `/login`

**Elementos:**
- 🐄 Logo y título del sistema
- 📝 Formulario de login (usuario/contraseña)
- 🔒 Validación de credenciales
- 💡 Credenciales de prueba visibles
- 🎨 Diseño con gradiente morado

**Funcionalidad:**
- Autenticación con JWT
- Redirección automática al dashboard
- Mensajes de error claros

---

### 2. Dashboard de Monitoreo (Usuario/Admin)
**Ruta:** `/`

**Layout Principal:**
```
┌──────────────────────────────────────────────────────────┐
│  🐄 Monitor de Ganado    🟢 Conectado 🔔 👤 admin [Salir]│
├────────────┬──────────────────────────────┬──────────────┤
│            │                              │              │
│  Animales  │         🗺️ MAPA            │   Detalles   │
│  (5)       │       OpenStreetMap          │   Animal     │
│            │                              │  Seleccionado│
│  🐑 OVINO  │     🐑  🐑  🐄               │              │
│  - 001     │         🐎                   │  Collar ID   │
│  🌡️ 38.5°C │           🐄                │  Raza        │
│  ❤️ 75 lpm │                              │  Telemetría  │
│            │      🔷 Geocerca             │  Ubicación   │
│  🐑 OVINO  │                              │              │
│  - 002     │                              │              │
│  ...       │                              │              │
│            │                              │              │
└────────────┴──────────────────────────────┴──────────────┘
```

**Sidebar Izquierdo (300px):**
- Lista de todos los animales monitoreados
- Emoji según tipo (🐑 Ovino, 🐄 Bovino, 🐎 Equino)
- Collar ID y raza
- Temperatura y frecuencia cardíaca en tiempo real
- Card seleccionada con borde azul

**Mapa Central:**
- OpenStreetMap como base
- Marcadores con emojis grandes para cada animal
- Polígono azul semitransparente (geocerca)
- Zoom y pan interactivo
- Popup al hacer clic con detalles

**Panel Derecho (300px - opcional):**
- Aparece al seleccionar un animal
- Información completa del animal
- Datos de telemetría actuales
- Botón X para cerrar

**Header:**
- Título del sistema
- Indicador de conexión WebSocket (🟢/🔴)
- Campana de notificaciones con contador
- Nombre de usuario y badge de admin
- Botón de cerrar sesión

---

### 3. Campana de Notificaciones
**Componente:** Dropdown desde header

**Estructura:**
```
┌─────────────────────────────────────┐
│  Notificaciones              [×]    │
├─────────────────────────────────────┤
│ │ BOVINO-001                    [✓] │
│ │ Temperatura alta: 41.2°C          │
│ │ 05/11/2025 13:45                  │
├─────────────────────────────────────┤
│ │ OVINO-002                     [✓] │
│ │ Animal fuera del perímetro        │
│ │ 05/11/2025 13:40                  │
├─────────────────────────────────────┤
│ │ EQUINO-001                        │
│ │ Frecuencia cardíaca alta: 135 lpm │
│ │ 05/11/2025 13:38                  │
└─────────────────────────────────────┘
```

**Características:**
- Contador en rojo sobre la campana
- Alertas no leídas con fondo azul claro
- Barra de color según tipo de alerta
- Timestamp de cada alerta
- Botón ✓ para marcar como leída
- Scroll para ver más

---

### 4. Panel de Administración
**Ruta:** `/admin` (Solo administradores)

**Pestañas:**
```
┌────────────────────────────────────────────────────┐
│  ⚙️ Panel de Administración    [Dashboard] [Salir]│
├────────────────────────────────────────────────────┤
│  👥 Usuarios  │  🐄 Ganado  │  🗺️ Geocerca         │
└────────────────────────────────────────────────────┘
```

#### 4.1 Pestaña Usuarios
```
┌──────────────────────────────────────────────────┐
│  Gestión de Usuarios          [+ Nuevo Usuario]  │
├──────────────────────────────────────────────────┤
│                                                  │
│  [Formulario de Usuario - cuando se crea/edita] │
│  ┌────────────────────────────────────────────┐ │
│  │ Usuario:     [________________]            │ │
│  │ Email:       [________________]            │ │
│  │ Nombre:      [________________]            │ │
│  │ RUT:         [________________]            │ │
│  │ ...                                        │ │
│  │ ☐ Es Administrador                        │ │
│  │ [Crear]  [Cancelar]                       │ │
│  └────────────────────────────────────────────┘ │
│                                                  │
│  Tabla de Usuarios                               │
│  ┌────────┬────────────┬──────────┬─────┬────┐ │
│  │Usuario │   Email    │  Nombre  │ Rol │ ⚙️ │ │
│  ├────────┼────────────┼──────────┼─────┼────┤ │
│  │admin   │admin@...   │ Admin U. │Admin│✏️🗑️│ │
│  │trabaj..│trabajad... │ Juan P.  │User │✏️🗑️│ │
│  └────────┴────────────┴──────────┴─────┴────┘ │
└──────────────────────────────────────────────────┘
```

#### 4.2 Pestaña Ganado
```
┌──────────────────────────────────────────────────┐
│  Gestión de Ganado            [+ Nuevo Animal]   │
├──────────────────────────────────────────────────┤
│                                                  │
│  Tabla de Animales                               │
│  ┌────────┬────────┬────────┬────┬──────┬────┐ │
│  │Collar  │ Tipo   │  Raza  │Edad│ Peso │ ⚙️ │ │
│  ├────────┼────────┼────────┼────┼──────┼────┤ │
│  │OVINO-1 │ OVINO  │Suffolk │ 2  │65.5kg│✏️🗑️│ │
│  │BOVINO-1│ BOVINO │ Angus  │ 4  │450kg │✏️🗑️│ │
│  │EQUINO-1│ EQUINO │Criollo │ 5  │380kg │✏️🗑️│ │
│  └────────┴────────┴────────┴────┴──────┴────┘ │
└──────────────────────────────────────────────────┘
```

#### 4.3 Pestaña Geocerca
```
┌──────────────────────────────────────────────────┐
│  Editor de Geocerca                              │
├──────────────────────────────────────────────────┤
│  La geocerca define el perímetro permitido...   │
│                                                  │
│  Geocerca Activa                                 │
│  ┌────────────────────────────────────────────┐ │
│  │ Nombre: Perímetro Principal                │ │
│  │ Creado por: admin                          │ │
│  │ Fecha: 01/11/2025                          │ │
│  │                                            │ │
│  │ Coordenadas del Perímetro:                 │ │
│  │ ┌────────────────────────────────────────┐ │ │
│  │ │ Punto 1: Lat: -33.4372, Lng: -70.6506 │ │ │
│  │ │ Punto 2: Lat: -33.4372, Lng: -70.6406 │ │ │
│  │ │ Punto 3: Lat: -33.4272, Lng: -70.6406 │ │ │
│  │ │ Punto 4: Lat: -33.4272, Lng: -70.6506 │ │ │
│  │ └────────────────────────────────────────┘ │ │
│  │                                            │ │
│  │ [Editar Coordenadas]                       │ │
│  └────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

---

## 🎨 Paleta de Colores

### Colores Principales
- **Primario:** `#667eea` (Azul/Morado)
- **Secundario:** `#764ba2` (Morado Oscuro)
- **Éxito:** `#4caf50` (Verde)
- **Error:** `#f44336` (Rojo)
- **Advertencia:** `#ff9800` (Naranja)
- **Info:** `#2196f3` (Azul)

### Backgrounds
- **Dashboard:** `#f5f5f5` (Gris Claro)
- **Cards:** `#ffffff` (Blanco)
- **Hover:** `#f9f9f9` (Gris Muy Claro)
- **Seleccionado:** `#f0f4ff` (Azul Muy Claro)

### Tipos de Alertas
- 🌡️ **Temperatura:** `#ff9800` (Naranja)
- ❤️ **Frecuencia:** `#f44336` (Rojo)
- 🗺️ **Perímetro:** `#2196f3` (Azul)

### Badges
- **Admin:** `#667eea` (Azul)
- **User:** `#4caf50` (Verde)
- **OVINO:** `#e3f2fd` / `#1976d2`
- **BOVINO:** `#fff3e0` / `#f57c00`
- **EQUINO:** `#fce4ec` / `#c2185b`

---

## 🔄 Flujo de Usuario

### Flujo Normal de Usuario
```
Login → Dashboard → Ver Animales en Mapa
                 ↓
          Recibir Alertas
                 ↓
        Ver Notificaciones
                 ↓
       Marcar como Leídas
                 ↓
     Seleccionar Animal → Ver Detalles
                 ↓
              Cerrar Sesión
```

### Flujo de Administrador
```
Login → Dashboard o Admin Panel
        ↓              ↓
     Monitoreo    Gestión
                     ↓
            Usuarios / Ganado / Geocerca
                     ↓
               Crear/Editar/Eliminar
                     ↓
                Volver a Dashboard
```

---

## 📊 Estados de la Aplicación

### Estados de Conexión
- **🟢 Conectado:** WebSocket activo, datos en tiempo real
- **🔴 Desconectado:** Sin conexión, datos estáticos

### Estados de Alerta
- **Sin leer:** Fondo azul claro, contador visible
- **Leída:** Fondo blanco, sin contador

### Estados de Animal
- **Normal:** Datos en rangos correctos
- **Alerta Temperatura:** Fondo rojo/naranja en el indicador
- **Alerta FC:** Fondo rojo en el indicador
- **Fuera de Perímetro:** Marcador con efecto especial

---

## 💡 Interacciones Clave

### En el Mapa
1. **Click en animal** → Abre popup con info básica
2. **Click en card lateral** → Abre panel de detalles
3. **Zoom/Pan** → Navegación libre del mapa

### En Notificaciones
1. **Click en campana** → Abre/cierra dropdown
2. **Click en ✓** → Marca alerta como leída
3. **Actualización automática** → Cada 10 segundos

### En Admin
1. **Click en pestaña** → Cambia vista
2. **Click en + Nuevo** → Muestra formulario
3. **Click en ✏️** → Edita registro
4. **Click en 🗑️** → Elimina (con confirmación)
5. **Submit formulario** → Crea/Actualiza y recarga tabla

---

## 🎭 Animaciones

- **Indicador conectado:** Pulso suave cada 2s
- **Card hover:** Desplazamiento 5px a la derecha
- **Botones:** Transición de color 0.3s
- **Alertas nuevas:** (Futuro) Shake o bounce

---

## 📱 Responsive Design

**Desktop (>1200px):**
- Layout completo con sidebar y panel de detalles
- Mapa grande en el centro

**Tablet (768px - 1200px):**
- Panel de detalles se superpone al mapa
- Sidebar colapsable

**Mobile (<768px):**
- Vista de lista en lugar de mapa
- Pestañas para cambiar entre vista
- Menú hamburguesa

---

## 🎯 Próximas Mejoras Visuales

- [ ] Modo oscuro
- [ ] Animaciones de transición
- [ ] Gráficos de telemetría (Chart.js)
- [ ] Mapa de calor
- [ ] Timeline de eventos
- [ ] Filtros avanzados
- [ ] Exportar a PDF
- [ ] Vista de comparación
