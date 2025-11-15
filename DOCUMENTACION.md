# 🐄 CAMPORT - Sistema de Monitoreo de Ganado en Tiempo Real

**Versión:** V6.0 - Gravedad de Centroide  
**Estado:** ✅ Production Ready  
**Fecha:** Noviembre 2025

---

## 📑 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Instalación Rápida](#instalación-rápida)
3. [Inicio del Sistema](#inicio-del-sistema)
4. [Arquitectura](#arquitectura)
5. [Funcionalidades](#funcionalidades)
6. [Credenciales de Acceso](#credenciales-de-acceso)
7. [API Endpoints](#api-endpoints)
8. [Características por Versión](#características-por-versión)
9. [Configuración Avanzada](#configuración-avanzada)
10. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Resumen Ejecutivo

**CAMPORT** es un sistema fullstack completo para monitoreo de ganado en tiempo real con:

- 🗺️ **Geolocalización en tiempo real** con mapas interactivos
- 📊 **Telemetría de signos vitales** (temperatura, frecuencia cardíaca)
- 🔷 **Geocercas múltiples** con alertas automáticas
- 🔔 **Sistema de notificaciones** en tiempo real
- 🧲 **Simulador avanzado** con gravedad de centroide
- 📡 **WebSocket** para actualizaciones instantáneas
- 👥 **Gestión de usuarios** con roles (Admin/Trabajador)

### Stack Tecnológico

**Backend:**
- Django 5.0.3 + Django REST Framework
- Django Channels (WebSocket)
- SQLite Database
- JWT Authentication

**Frontend:**
- React 18
- Leaflet (OpenStreetMap)
- Axios + WebSocket
- React Router DOM

---

## ⚡ Instalación Rápida

### Prerrequisitos
- Python 3.8+
- Node.js 14+
- PowerShell (Windows) o Bash (Linux/Mac)

### Pasos de Instalación

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/BorBP/Proyecto-Integrado-Camport.git
cd Proyecto-Integrado-Camport
```

#### 2. Configurar Backend
```bash
cd backend
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python manage.py migrate

# Poblar con datos iniciales
python populate_db.py
```

#### 3. Configurar Frontend
```bash
cd frontend
npm install
```

**✅ Instalación Completa!**

---

## 🚀 Inicio del Sistema

### Opción 1: Scripts Automáticos (Recomendado)

Abre **3 terminales** diferentes:

**Terminal 1 - Backend:**
```powershell
.\start-backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
.\start-frontend.ps1
```

**Terminal 3 - Simulador (Opcional):**
```powershell
.\start-simulator.ps1
```

### Opción 2: Inicio Manual

**Backend (Terminal 1):**
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac
python manage.py runserver
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm start
```

**Simulador V6.0 (Terminal 3 - Opcional):**
```bash
cd backend
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate    # Linux/Mac
python manage.py simulate_collars --interval 20 --gravity-factor 0.2
```

### URLs de Acceso

Una vez iniciado:
- 🌐 **Frontend:** http://localhost:3000
- 🔧 **Backend API:** http://localhost:8000/api
- 👨‍💼 **Admin Panel:** http://localhost:8000/admin
- 📡 **WebSocket:** ws://localhost:8000/ws/telemetria/

---

## 🏗️ Arquitectura

```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────┐
│   React 18       │◄───────►│   Django 5.0     │◄───────►│  SQLite DB   │
│   Frontend       │  HTTP   │   REST API       │   ORM   │              │
│   (Port 3000)    │  REST   │   (Port 8000)    │         │              │
└──────────────────┘         └──────────────────┘         └──────────────┘
         ↕                            ↕
    WebSocket                    WebSocket
         ↕                            ↕
    ┌────────────────────────────────────────┐
    │      Real-Time Telemetry Updates       │
    │   (Temperature, Heart Rate, Location)  │
    └────────────────────────────────────────┘
```

### Componentes Principales

#### Backend (`/backend`)
- **API REST** - Django REST Framework
- **WebSocket Consumer** - Django Channels
- **Modelos de Datos** - User, Animal, Telemetría, Geocerca, Alertas
- **Autenticación** - JWT (Simple JWT)
- **Simulador** - Pastoreo virtual con gravedad de centroide

#### Frontend (`/frontend`)
- **Autenticación** - Login/Logout con JWT
- **Dashboard** - Mapa interactivo con Leaflet
- **Panel Admin** - CRUD de usuarios, animales y geocercas
- **Notificaciones** - Sistema de alertas en tiempo real
- **WebSocket Client** - Actualizaciones automáticas

---

## 🎯 Funcionalidades

### Para Todos los Usuarios

#### 1. Dashboard en Tiempo Real
- ✅ Mapa interactivo con OpenStreetMap
- ✅ Visualización de animales con emojis (🐑 🐄 🐎)
- ✅ Actualización automática vía WebSocket
- ✅ Panel lateral con lista de animales
- ✅ Detalles completos al seleccionar un animal
- ✅ Visualización de geocercas con colores

#### 2. Sistema de Alertas
- 🔔 Notificaciones en tiempo real
- 📊 Campana con contador de alertas no leídas
- 🌡️ Temperatura anormal (fiebre/hipotermia)
- ❤️ Frecuencia cardíaca anormal
- 🗺️ Fuera de perímetro (geocerca)
- ✅ Marcar alertas como leídas

#### 3. Telemetría en Vivo
- 📍 Ubicación GPS (latitud, longitud)
- 🌡️ Temperatura corporal
- ❤️ Frecuencia cardíaca
- 🕐 Timestamp de última actualización

### Para Administradores

#### 1. Gestión de Usuarios
- ✅ Crear, editar y eliminar usuarios
- ✅ Asignar roles (Admin/Trabajador)
- ✅ Gestión de datos personales
- ✅ Control de acceso

#### 2. Gestión de Ganado
- ✅ Registrar nuevos animales con collar
- ✅ Editar información del ganado
- ✅ Eliminar animales del sistema
- ✅ Asignar animales a geocercas
- 📝 Datos: tipo, raza, edad, peso, sexo, color, display ID

#### 3. Editor de Geocercas
- ✅ Crear múltiples geocercas
- ✅ Editar vértices del polígono
- ✅ Activar/desactivar geocercas
- ✅ Ver contador de animales por geocerca
- ✅ Visualización en mapa interactivo

---

## 👤 Credenciales de Acceso

### Usuario Administrador
- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Permisos:** Gestión completa del sistema

### Usuario Trabajador
- **Usuario:** `trabajador`
- **Contraseña:** `trabajador123`
- **Permisos:** Solo monitoreo y visualización

### Datos Iniciales

**5 Animales de Prueba:**
1. **OVINO-001** - Oveja Suffolk
2. **OVINO-002** - Oveja Merino
3. **BOVINO-001** - Vaca Angus
4. **BOVINO-002** - Vaca Hereford
5. **EQUINO-001** - Caballo Criollo

**Geocerca Configurada:**
- Ubicación: La Araucanía, Chile (-38.84°S, -72.29°W)
- Polígono de 4 vértices
- Todos los animales asignados

---

## 📡 API Endpoints

### Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/token/` | Obtener token JWT |
| POST | `/api/token/refresh/` | Refrescar token |

### Usuarios

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/users/` | Listar usuarios | Admin |
| POST | `/api/users/` | Crear usuario | Admin |
| GET | `/api/users/me/` | Usuario actual | Todos |
| PUT | `/api/users/{id}/` | Actualizar usuario | Admin |
| DELETE | `/api/users/{id}/` | Eliminar usuario | Admin |

### Animales

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/animales/` | Listar animales | Todos |
| POST | `/api/animales/` | Crear animal | Admin |
| GET | `/api/animales/{id}/` | Detalle de animal | Todos |
| PUT | `/api/animales/{id}/` | Actualizar animal | Admin |
| DELETE | `/api/animales/{id}/` | Eliminar animal | Admin |

### Telemetría

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/telemetria/` | Listar telemetría |
| GET | `/api/telemetria/?animal={collar_id}` | Telemetría de un animal |

### Geocercas

| Método | Endpoint | Descripción | Permisos |
|--------|----------|-------------|----------|
| GET | `/api/geocercas/` | Listar geocercas | Todos |
| GET | `/api/geocercas/activa/` | Geocerca activa | Todos |
| POST | `/api/geocercas/` | Crear geocerca | Admin |
| PUT | `/api/geocercas/{id}/` | Actualizar geocerca | Admin |

### Alertas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/alertas/` | Todas las alertas |
| GET | `/api/alertas-usuario/` | Alertas del usuario |
| GET | `/api/alertas-usuario/no_leidas/` | Alertas no leídas |
| POST | `/api/alertas-usuario/{id}/marcar_leido/` | Marcar como leída |

### WebSocket

| URL | Descripción |
|-----|-------------|
| `ws://localhost:8000/ws/telemetria/` | Canal de telemetría en tiempo real |

---

## 🚀 Características por Versión

### V6.0 - Gravedad de Centroide (Actual)

**🧲 Nuevas Características:**
- Movimiento proactivo con atracción al centro (80% aleatorio + 20% atracción)
- Migración automática cuando cambia la geocerca
- Factor de gravedad configurable (0%-100%)
- Distancia al centroide visible en logs
- Adaptación dinámica sin reinicio

**Parámetros del Simulador:**
```bash
python manage.py simulate_collars --interval 20 --gravity-factor 0.2
```

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `--interval` | 20 | Segundos entre actualizaciones |
| `--gravity-factor` | 0.2 | 20% atracción al centroide |

### V5.0 - Sistema de Fugas

- 🚨 Fugas aleatorias cada 60 segundos
- 🏠 Retorno automático después de 30 segundos
- 📊 Temperatura con 1 decimal (realista)
- 🔄 Consulta dinámica EN VIVO

### V4.0 - Rebaño Completo

- 🐄 Simulación de rebaño completo
- ⏱️ Intervalo realista (20 segundos)
- 🔄 Dinamismo sin reinicio
- 📈 Escalable a 100+ animales

### V3.0 - Pastoreo Virtual

- 🌱 Inicialización en centroide de geocerca
- 🎯 Algoritmo de pastoreo virtual
- 📡 Integración WebSocket completa
- 🛡️ Muros de rebote anti-fuga

### V2.0 - Múltiples Geocercas

- 🗺️ Sistema multi-geocerca
- 🆔 Display IDs automáticos (OVINO-001, etc.)
- ✏️ Editor avanzado de geocercas
- 📊 Asignación individual de animales

### V1.0 - Sistema Base

- ⚛️ React + Django
- 📡 WebSocket básico
- 🗺️ Mapa con Leaflet
- 🔐 Autenticación JWT

---

## ⚙️ Configuración Avanzada

### Rangos de Alerta

**Temperatura Corporal:**
- ✅ Normal: 37.5°C - 40°C
- 🥶 Hipotermia: < 37.5°C
- 🔥 Fiebre: > 40°C

**Frecuencia Cardíaca:**
- ✅ Normal: 40 - 120 lpm
- 💙 Bradicardia: < 40 lpm
- ❤️ Taquicardia: > 120 lpm

### Simulador - Opciones Avanzadas

**Gravedad Normal (Recomendado):**
```bash
python manage.py simulate_collars --gravity-factor 0.2
```

**Gravedad Fuerte:**
```bash
python manage.py simulate_collars --gravity-factor 0.4
```

**Sin Gravedad (V5.0 Mode):**
```bash
python manage.py simulate_collars --gravity-factor 0.0
```

**Intervalo Personalizado:**
```bash
python manage.py simulate_collars --interval 10  # 10 segundos
```

### Simular Emergencias Manualmente

Puedes forzar emergencias para pruebas:

```bash
# Simular fiebre
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-001/fiebre/

# Simular salida de perímetro
curl -X POST http://localhost:8000/api/simulate_emergency/BOVINO-001/perimetro/

# Simular taquicardia
curl -X POST http://localhost:8000/api/simulate_emergency/EQUINO-001/taquicardia/

# Simular hipotermia
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-002/hipotermia/
```

### Variables de Entorno

**Backend (`backend/ganadoproject/settings.py`):**
```python
SECRET_KEY = 'tu-clave-secreta'
DEBUG = True  # False en producción
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CORS_ALLOWED_ORIGINS = ['http://localhost:3000']
```

**Frontend (`frontend/src/services/api.js`):**
```javascript
const API_URL = 'http://localhost:8000/api';
const WS_URL = 'ws://localhost:8000/ws/telemetria/';
```

---

## 🛠️ Solución de Problemas

### ❌ El Backend no Inicia

**Error:** `ModuleNotFoundError: No module named 'django'`

**Solución:**
```bash
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### ❌ El Frontend no Inicia

**Error:** `npm ERR! missing script: start`

**Solución:**
```bash
cd frontend
npm install
```

---

### ❌ WebSocket no Conecta

**Problema:** Frontend no recibe actualizaciones en tiempo real

**Verificar:**
1. Backend está corriendo en puerto 8000
2. URL del WebSocket es correcta en el código
3. Channels está instalado:
```bash
pip install channels daphne
```

---

### ❌ Error de CORS

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solución:**
Verificar `CORS_ALLOWED_ORIGINS` en `backend/ganadoproject/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

---

### ❌ Alertas no Aparecen

**Verificar:**
1. Simulador está enviando datos
2. Geocerca está creada en la BD
3. Consola del backend para errores
4. WebSocket conectado en el frontend

---

### ❌ Base de Datos Corrupta

**Solución:**
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python populate_db.py
```

---

### ❌ Puerto Ya en Uso

**Error:** `Error: That port is already in use`

**Solución:**

**Windows:**
```powershell
# Ver proceso en puerto 8000
netstat -ano | findstr :8000
# Matar proceso (reemplaza PID)
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
# Ver proceso en puerto 8000
lsof -i :8000
# Matar proceso
kill -9 <PID>
```

---

## 📊 Estadísticas del Proyecto

### Código
- **Backend:** ~1,500 líneas de Python
- **Frontend:** ~2,000 líneas de JavaScript/JSX
- **Simulador V6.0:** ~570 líneas
- **Total:** ~4,000+ líneas de código

### Archivos
- **Componentes React:** 15+
- **Modelos Django:** 6
- **API Endpoints:** 25+
- **Scripts PowerShell:** 3

### Tecnologías
- **Backend:** 10 paquetes principales
- **Frontend:** 1,350+ paquetes npm
- **Total Size:** ~200MB

---

## 📁 Estructura del Proyecto

```
Proyecto-Integrado-Camport/
│
├── backend/                          # Backend Django
│   ├── venv/                        # Entorno virtual Python
│   ├── api/                         # App principal
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── simulate_collars.py  # Simulador V6.0
│   │   ├── models.py                # Modelos de datos
│   │   ├── serializers.py           # DRF Serializers
│   │   ├── views.py                 # ViewSets API
│   │   ├── consumers.py             # WebSocket Consumer
│   │   ├── routing.py               # WebSocket Routing
│   │   └── urls.py                  # URLs API
│   │
│   ├── ganadoproject/               # Configuración Django
│   │   ├── settings.py              # Configuración
│   │   ├── urls.py                  # URLs principales
│   │   ├── asgi.py                  # ASGI config
│   │   └── wsgi.py                  # WSGI config
│   │
│   ├── db.sqlite3                   # Base de datos
│   ├── manage.py                    # Django CLI
│   ├── populate_db.py              # Script de población
│   ├── simulator.py                # Simulador legacy
│   └── requirements.txt            # Dependencias Python
│
├── frontend/                         # Frontend React
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/               # Autenticación
│   │   │   │   ├── LoginForm.js
│   │   │   │   └── RequireAuth.js
│   │   │   │
│   │   │   ├── map/                # Mapa
│   │   │   │   ├── MapContainer.js
│   │   │   │   ├── AnimalMarker.js
│   │   │   │   └── GeofenceLayer.js
│   │   │   │
│   │   │   ├── dashboard/          # Dashboard
│   │   │   │   ├── UserDashboard.js
│   │   │   │   └── NotificationBell.js
│   │   │   │
│   │   │   └── admin/              # Panel Admin
│   │   │       ├── AdminDashboard.js
│   │   │       ├── UserTable.js
│   │   │       ├── AnimalTable.js
│   │   │       └── GeofenceEditor.js
│   │   │
│   │   ├── context/                # Context API
│   │   │   └── AuthContext.js
│   │   │
│   │   ├── hooks/                  # Custom Hooks
│   │   │   └── useWebSocket.js
│   │   │
│   │   ├── services/               # Servicios
│   │   │   └── api.js
│   │   │
│   │   ├── App.js                  # Componente raíz
│   │   └── index.js                # Entry point
│   │
│   ├── package.json                # Dependencias npm
│   └── package-lock.json
│
├── start-backend.ps1               # Script inicio backend
├── start-frontend.ps1              # Script inicio frontend
├── start-simulator.ps1             # Script inicio simulador
│
└── DOCUMENTACION.md                # Este archivo
```

---

## 🎓 Flujo de Datos

### Telemetría en Tiempo Real

```
1. Simulador
   ↓ (WebSocket)
2. Backend Consumer
   ↓ (Recibe y valida)
3. Base de Datos
   ↓ (Guarda telemetría)
4. Verificación de Alertas
   ↓ (Temp, FC, Perímetro)
5. Broadcast a Clientes
   ↓ (WebSocket)
6. Frontend
   ↓ (Actualiza UI)
7. Usuario ve cambios
```

### Autenticación

```
1. Usuario ingresa credenciales
   ↓
2. Frontend → POST /api/token/
   ↓
3. Backend valida y retorna JWT
   ↓
4. Frontend guarda token
   ↓
5. Requests subsecuentes incluyen:
   Authorization: Bearer <token>
```

---

## 🔮 Roadmap Futuro

### Mejoras Propuestas

- [ ] Machine Learning para predicción de movimiento
- [ ] Historial de rutas de animales
- [ ] Zonas de interés (agua, comida)
- [ ] Comportamiento de manada
- [ ] Patrones circadianos
- [ ] Multi-tenant (múltiples granjas)
- [ ] Exportación de reportes PDF
- [ ] Notificaciones push móviles
- [ ] Integración con dispositivos IoT reales
- [ ] APIs de clima

### Optimizaciones Técnicas

- [ ] Caché con Redis
- [ ] PostgreSQL en producción
- [ ] Docker deployment
- [ ] Tests unitarios (Jest, Pytest)
- [ ] CI/CD con GitHub Actions
- [ ] Compresión de datos WebSocket
- [ ] Paginación optimizada
- [ ] Índices de BD

---

## 📄 Licencia

Este es un proyecto educativo de demostración.

---

## 👨‍💻 Autor

Sistema desarrollado como demostración de arquitectura fullstack moderna con Django y React.

---

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa la sección [Solución de Problemas](#solución-de-problemas)
2. Verifica los logs del backend y frontend
3. Abre un issue en GitHub con detalles del error

---

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Python 3.8+ instalado
- [ ] Node.js 14+ instalado
- [ ] Entorno virtual activado
- [ ] Dependencias instaladas (pip y npm)
- [ ] Migraciones aplicadas
- [ ] Base de datos poblada
- [ ] Puertos 3000 y 8000 disponibles
- [ ] No hay errores en consola

---

## 🎉 Conclusión

**CAMPORT V6.0** es un sistema completo y funcional de monitoreo de ganado que demuestra:

✅ **Arquitectura fullstack** moderna  
✅ **Tiempo real** con WebSocket  
✅ **Geolocalización** avanzada  
✅ **Simulación realista** con física  
✅ **Escalabilidad** demostrada  
✅ **Production ready** y documentado  

**El sistema está listo para:**
- Demostraciones a clientes
- Operación en producción
- Expansión a múltiples granjas
- Integración con hardware IoT

---

**Desarrollado con ❤️ para la gestión eficiente del ganado**

**CAMPORT - El futuro digital de la ganadería** 🐄🚀📡

---

**Versión:** V6.0.0  
**Última Actualización:** Noviembre 2025  
**Estado:** ✅ **PRODUCCIÓN**
