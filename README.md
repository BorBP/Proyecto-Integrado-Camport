# 🐄 Sistema de Monitoreo de Ganado en Tiempo Real

Sistema fullstack para monitoreo de ganado con geolocalización en tiempo real, telemetría de signos vitales y alertas automáticas.

## 🏗️ Arquitectura

### Backend
- **Framework:** Django 5.0 + Django REST Framework
- **Base de Datos:** SQLite
- **Tiempo Real:** Django Channels (WebSockets)
- **Autenticación:** JWT (Simple JWT)

### Frontend
- **Framework:** React 18
- **Enrutamiento:** React Router DOM
- **Mapas:** React Leaflet + OpenStreetMap
- **WebSockets:** ReconnectingWebSocket
- **Estado:** React Context API

## 📦 Instalación

### Backend

1. Navegar al directorio backend:
```bash
cd backend
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# o
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Poblar base de datos con datos iniciales:
```bash
python populate_db.py
```

### Frontend

1. Navegar al directorio frontend:
```bash
cd frontend
```

2. Instalar dependencias:
```bash
npm install
```

## 🚀 Ejecución

### 1. Iniciar el Backend (Django)

En el directorio `backend`:

```bash
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

El backend estará disponible en: `http://localhost:8000`

### 2. Iniciar el Simulador de Telemetría (Opcional)

En otra terminal, en el directorio `backend`:

```bash
.\venv\Scripts\Activate.ps1
pip install websockets
python simulator.py
```

El simulador enviará datos de telemetría cada 5 segundos para los 5 animales.

### 3. Iniciar el Frontend (React)

En el directorio `frontend`:

```bash
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## 👤 Credenciales de Acceso

### Administrador
- **Usuario:** admin
- **Contraseña:** admin123

### Trabajador
- **Usuario:** trabajador
- **Contraseña:** trabajador123

## 🎯 Funcionalidades

### Para Todos los Usuarios

1. **Dashboard en Tiempo Real**
   - Mapa interactivo con OpenStreetMap
   - Visualización de animales con emojis (🐑 🐄 🐎)
   - Actualización en tiempo real vía WebSocket
   - Panel lateral con lista de animales y telemetría
   - Detalles completos al seleccionar un animal

2. **Sistema de Alertas**
   - Notificaciones en tiempo real
   - Campana con contador de alertas no leídas
   - Tipos de alertas:
     - 🌡️ Temperatura anormal (fiebre/hipotermia)
     - ❤️ Frecuencia cardíaca anormal
     - 🗺️ Fuera de perímetro (geocerca)
   - Marcar alertas como leídas

3. **Visualización de Geocerca**
   - Polígono azul en el mapa
   - Define el perímetro permitido
   - Alertas automáticas si un animal sale

### Para Administradores

1. **Gestión de Usuarios**
   - Crear, editar y eliminar usuarios
   - Asignar roles (Admin/Trabajador)
   - Gestión completa de datos personales

2. **Gestión de Ganado**
   - Registrar nuevos animales con collar
   - Editar información del ganado
   - Eliminar animales del sistema
   - Datos: tipo, raza, edad, peso, sexo, color

3. **Editor de Geocerca**
   - Visualizar geocerca activa
   - Ver coordenadas del perímetro
   - Información de creación

## 🧪 Probar el Sistema

### 1. Simular Emergencias

Puedes forzar emergencias para pruebas usando la URL secreta:

```bash
# Simular fiebre en un animal
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-001/fiebre/

# Simular salida de perímetro
curl -X POST http://localhost:8000/api/simulate_emergency/BOVINO-001/perimetro/

# Simular taquicardia
curl -X POST http://localhost:8000/api/simulate_emergency/EQUINO-001/taquicardia/

# Simular hipotermia
curl -X POST http://localhost:8000/api/simulate_emergency/OVINO-002/hipotermia/
```

### 2. API Endpoints

Todos los endpoints requieren autenticación JWT excepto `/api/token/`.

#### Autenticación
- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Refrescar token

#### Usuarios
- `GET /api/users/` - Listar usuarios
- `POST /api/users/` - Crear usuario (admin)
- `GET /api/users/me/` - Obtener usuario actual
- `PUT /api/users/{id}/` - Actualizar usuario (admin)
- `DELETE /api/users/{id}/` - Eliminar usuario (admin)

#### Animales
- `GET /api/animales/` - Listar animales
- `POST /api/animales/` - Crear animal (admin)
- `GET /api/animales/{id}/` - Obtener animal
- `PUT /api/animales/{id}/` - Actualizar animal (admin)
- `DELETE /api/animales/{id}/` - Eliminar animal (admin)

#### Telemetría
- `GET /api/telemetria/` - Listar telemetría
- `GET /api/telemetria/?animal={collar_id}` - Telemetría de un animal

#### Geocercas
- `GET /api/geocercas/` - Listar geocercas
- `GET /api/geocercas/activa/` - Obtener geocerca activa
- `POST /api/geocercas/` - Crear geocerca (admin)
- `PUT /api/geocercas/{id}/` - Actualizar geocerca (admin)

#### Alertas
- `GET /api/alertas/` - Listar todas las alertas
- `GET /api/alertas-usuario/` - Alertas del usuario actual
- `GET /api/alertas-usuario/no_leidas/` - Alertas no leídas
- `POST /api/alertas-usuario/{id}/marcar_leido/` - Marcar como leída

#### WebSocket
- `ws://localhost:8000/ws/telemetria/` - Canal de telemetría en tiempo real

## 📊 Datos Iniciales

El sistema viene con 5 animales de prueba:

1. **OVINO-001** - Suffolk (Oveja)
2. **OVINO-002** - Merino (Oveja)
3. **BOVINO-001** - Angus (Vaca)
4. **BOVINO-002** - Hereford (Vaca)
5. **EQUINO-001** - Criollo (Caballo)

Cada animal tiene telemetría inicial con:
- Temperatura corporal: 38-39.5°C
- Frecuencia cardíaca: 60-100 lpm
- Ubicación: Dentro de la geocerca predefinida en **La Araucanía, Chile** (región sur)

### Geocerca Configurada
- **Ubicación:** La Araucanía, Chile
- **Coordenadas:** -38.84°S, -72.29°W (aproximadamente)
- **Área:** Polígono de 4 puntos que define el perímetro permitido

## 🔧 Configuración

### Variables de Backend

En `backend/ganadoproject/settings.py`:

- `SECRET_KEY` - Clave secreta de Django
- `DEBUG` - Modo debug
- `ALLOWED_HOSTS` - Hosts permitidos
- `CORS_ALLOWED_ORIGINS` - Orígenes permitidos para CORS

### Variables de Frontend

En `frontend/src/services/api.js`:

- `API_URL` - URL de la API backend (default: `http://localhost:8000/api`)

En componentes WebSocket:

- WebSocket URL (default: `ws://localhost:8000/ws/telemetria/`)

## 📝 Notas Técnicas

### Rangos de Alerta

**Temperatura Corporal:**
- Normal: 37.5°C - 40°C
- Hipotermia: < 37.5°C
- Fiebre: > 40°C

**Frecuencia Cardíaca:**
- Normal: 40 - 120 lpm
- Bradicardia: < 40 lpm
- Taquicardia: > 120 lpm

**Geocerca:**
- Se verifica si el punto (lng, lat) está dentro del polígono
- Usa la librería Shapely para cálculos geométricos

### Flujo de Telemetría

1. Simulador envía datos via WebSocket
2. Backend (Consumer) recibe y guarda en BD
3. Backend verifica alertas automáticamente
4. Si hay alerta, crea registro y notifica usuarios
5. Backend transmite datos a todos los clientes conectados
6. Frontend actualiza mapa y UI en tiempo real

## 🐛 Solución de Problemas

### El WebSocket no conecta

1. Verificar que el backend esté corriendo
2. Verificar la URL del WebSocket en el código
3. Comprobar que Channels esté instalado correctamente

### Las alertas no aparecen

1. Verificar que el simulador esté enviando datos
2. Comprobar la consola del backend para errores
3. Verificar que la geocerca esté creada

### Error de CORS

1. Verificar `CORS_ALLOWED_ORIGINS` en settings.py
2. Asegurarse de que incluya `http://localhost:3000`

## 📚 Tecnologías Utilizadas

### Backend
- Django 5.0.3
- Django REST Framework 3.14.0
- Django Channels 4.0.0
- djangorestframework-simplejwt 5.3.1
- django-cors-headers 4.3.1
- Shapely 2.0.2
- Daphne 4.1.0

### Frontend
- React 18
- React Router DOM 6
- Leaflet + React Leaflet
- Axios
- ReconnectingWebSocket

## 📄 Licencia

Este es un proyecto de demostración educativa.

## 👨‍💻 Autor

Sistema desarrollado como demostración de arquitectura fullstack con Django y React.
