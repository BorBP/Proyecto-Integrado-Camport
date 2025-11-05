# 📁 Estructura del Proyecto

```
Sistema-Monitoreo-Ganado/
│
├── README.md                      # Documentación completa
├── INICIO-RAPIDO.md              # Guía de inicio rápido
├── start-backend.ps1             # Script para iniciar backend
├── start-frontend.ps1            # Script para iniciar frontend
├── start-simulator.ps1           # Script para iniciar simulador
│
├── backend/                      # 🐍 Backend Django
│   ├── venv/                     # Entorno virtual de Python
│   ├── ganadoproject/            # Configuración principal Django
│   │   ├── __init__.py
│   │   ├── settings.py          # ⚙️ Configuración (CORS, JWT, Channels)
│   │   ├── urls.py              # URLs principales + JWT
│   │   ├── asgi.py              # 📡 Configuración ASGI + WebSocket
│   │   └── wsgi.py
│   │
│   ├── api/                      # 📦 App principal
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py            # 🗄️ Modelos (User, Animal, Telemetría, etc.)
│   │   ├── serializers.py       # 🔄 Serializers DRF
│   │   ├── views.py             # 👁️ ViewSets + API de emergencias
│   │   ├── urls.py              # 🛣️ URLs de la API
│   │   ├── admin.py             # 👨‍💼 Panel de administración Django
│   │   ├── consumers.py         # 📡 WebSocket Consumer (telemetría)
│   │   └── routing.py           # 🔀 Routing de WebSocket
│   │
│   ├── manage.py                # Django management
│   ├── requirements.txt         # 📋 Dependencias Python
│   ├── populate_db.py          # 🌱 Script para poblar BD
│   ├── simulator.py            # 🎯 Simulador de telemetría
│   └── db.sqlite3              # 💾 Base de datos SQLite
│
└── frontend/                    # ⚛️ Frontend React
    ├── node_modules/
    ├── public/
    │   ├── index.html
    │   └── favicon.ico
    │
    ├── src/
    │   ├── components/          # 🧩 Componentes React
    │   │   ├── auth/
    │   │   │   ├── LoginForm.js        # 🔐 Formulario de login
    │   │   │   ├── LoginForm.css
    │   │   │   └── RequireAuth.js      # 🛡️ HOC de autenticación
    │   │   │
    │   │   ├── map/
    │   │   │   ├── MapContainer.js     # 🗺️ Contenedor del mapa
    │   │   │   ├── MapComponent.css
    │   │   │   ├── AnimalMarker.js     # 📍 Marcador de animal
    │   │   │   └── GeofenceLayer.js    # 🔷 Capa de geocerca
    │   │   │
    │   │   ├── dashboard/
    │   │   │   ├── UserDashboard.js    # 📊 Dashboard principal
    │   │   │   ├── UserDashboard.css
    │   │   │   ├── NotificationBell.js # 🔔 Campana de alertas
    │   │   │   └── NotificationBell.css
    │   │   │
    │   │   └── admin/
    │   │       ├── AdminDashboard.js   # ⚙️ Panel admin
    │   │       ├── AdminDashboard.css
    │   │       ├── UserTable.js        # 👥 CRUD usuarios
    │   │       ├── AnimalTable.js      # 🐄 CRUD animales
    │   │       ├── GeofenceEditor.js   # 🗺️ Editor geocerca
    │   │       ├── GeofenceEditor.css
    │   │       └── Tables.css
    │   │
    │   ├── context/              # 🔄 Context API
    │   │   └── AuthContext.js   # Contexto de autenticación
    │   │
    │   ├── hooks/               # 🪝 Custom Hooks
    │   │   └── useWebSocket.js  # Hook para WebSocket
    │   │
    │   ├── services/            # 🌐 Servicios API
    │   │   └── api.js           # Cliente Axios + servicios
    │   │
    │   ├── App.js               # 🎯 Componente principal
    │   ├── App.css
    │   ├── index.js             # 📍 Punto de entrada
    │   └── index.css
    │
    ├── package.json             # 📋 Dependencias npm
    └── package-lock.json
```

## 🔑 Archivos Clave

### Backend

**models.py** (279 líneas)
- Modelo User extendido con campos personalizados
- Modelo Animal con collar_id único
- Modelo Telemetría con timestamp y datos vitales
- Modelo Geocerca con coordenadas JSON
- Modelos Alerta y AlertaUsuario

**views.py** (173 líneas)
- ViewSets REST para todos los modelos
- Endpoint de emergencia para simulaciones
- Permisos configurados (Admin/User)
- Acciones personalizadas

**consumers.py** (163 líneas)
- Consumer de WebSocket para telemetría
- Lógica de verificación de alertas
- Chequeo de temperatura, FC y perímetro
- Broadcasting a clientes conectados

**serializers.py** (78 líneas)
- Serializers para todos los modelos
- Campos anidados para relaciones
- Validación de datos

### Frontend

**UserDashboard.js** (143 líneas)
- Dashboard principal con mapa
- Lista de animales en sidebar
- Panel de detalles
- Integración WebSocket
- Estado de conexión

**MapContainer.js**
- Mapa Leaflet con OpenStreetMap
- Renderizado de animales
- Capa de geocerca
- Marcadores personalizados

**NotificationBell.js** (103 líneas)
- Sistema de notificaciones
- Contador de no leídas
- Dropdown con historial
- Marcar como leídas

**AdminDashboard.js**
- Panel de administración con pestañas
- Gestión de usuarios
- Gestión de animales
- Editor de geocerca

**AuthContext.js**
- Context API para autenticación
- Manejo de JWT
- Estado del usuario
- Login/Logout

## 📊 Estadísticas del Proyecto

### Backend
- **Líneas de código Python:** ~1,500+
- **Modelos de datos:** 6
- **Endpoints API:** 25+
- **WebSocket Consumers:** 1
- **Scripts auxiliares:** 2

### Frontend
- **Componentes React:** 15+
- **Hooks personalizados:** 2
- **Context Providers:** 1
- **Servicios API:** 1
- **Líneas de código JS/JSX:** ~2,000+
- **Archivos CSS:** 8

### Total
- **Archivos creados:** 50+
- **Líneas de código:** ~3,500+
- **Tecnologías integradas:** 12+

## 🎨 Tecnologías por Capa

### Backend Stack
```
Django 5.0.3
├── djangorestframework 3.14.0
├── djangorestframework-simplejwt 5.3.1
├── channels 4.0.0
├── daphne 4.1.0
├── django-cors-headers 4.3.1
└── shapely 2.0.2
```

### Frontend Stack
```
React 18
├── react-router-dom 6
├── leaflet + react-leaflet
├── axios
└── reconnecting-websocket
```

## 🏗️ Arquitectura

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Browser   │◄───────►│    React     │◄───────►│   Django    │
│  (Cliente)  │  HTTP   │   Frontend   │  REST   │   Backend   │
└─────────────┘         └──────────────┘         └─────────────┘
       │                        │                        │
       │                        │                        │
       │         WebSocket      │                        │
       └────────────────────────┴────────────────────────┘
                            Real-Time
                          Telemetry Data
```

## 📝 Flujo de Datos

1. **Simulador** → Envía telemetría via WebSocket
2. **Backend Consumer** → Recibe, valida y guarda en BD
3. **Backend Consumer** → Verifica alertas (temp, FC, perímetro)
4. **Backend Consumer** → Broadcast a todos los clientes
5. **Frontend** → Actualiza mapa y UI en tiempo real
6. **Frontend** → Muestra alertas en campana de notificaciones

## ✨ Características Implementadas

✅ Autenticación JWT
✅ CRUD completo de usuarios y animales
✅ WebSocket para tiempo real
✅ Mapa interactivo con Leaflet
✅ Sistema de alertas automáticas
✅ Geocercas con verificación geométrica
✅ Panel de administración
✅ Dashboard de monitoreo
✅ Simulador de telemetría
✅ API REST completa
✅ Responsive design
✅ Manejo de errores
✅ Validación de datos
✅ Permisos por roles

## 🎯 Próximas Mejoras Sugeridas

- [ ] Editor visual de geocercas
- [ ] Gráficos históricos de telemetría
- [ ] Exportación de reportes
- [ ] Notificaciones push
- [ ] Modo oscuro
- [ ] Multi-idioma
- [ ] Tests unitarios
- [ ] Docker deployment
- [ ] Redis para Channels
- [ ] PostgreSQL para producción
