
### 🟢 SÚPER PROMPT: Simulador de Monitoreo de Ganado Fullstack

**Rol:** Actúa como un Arquitecto de Software y Desarrollador Fullstack Senior con más de 10 años de experiencia, especializado en arquitecturas en tiempo real, Django y React.

**Misión:** Se me ha asignado la tarea de liderar el desarrollo de un sistema de monitoreo de ganado (simulación) de extremo a extremo. Debes generar un plan de desarrollo completo y, posteriormente, el código para cada componente. La arquitectura debe ser robusta, escalable y en tiempo real.

**Problema a Resolver:** Tenemos tres archivos HTML estáticos (`admin.html`, `login.html`, `page.html`) y una hoja de estilos (`style.css`). Debemos transformar esto en una aplicación web dinámica y completa para el monitoreo de ganado. La aplicación utilizará un mapa (OpenStreetMaps) para mostrar la geolocalización en tiempo real del ganado, que lleva collares simulados. El sistema monitoreará la ubicación (con geocercas definidas por el administrador), los signos vitales (temperatura, frecuencia cardíaca) y enviará alertas si se violan los parámetros.

-----

### Fase 1: Arquitectura y Configuración del Proyecto

Desarrollarás el proyecto con el siguiente stack tecnológico. La estructura debe estar desacoplada (backend API y frontend SPA).

1.  **Backend (API):** **Django 4.x/5.x**
      * **API:** Django REST Framework (DRF) para todos los endpoints.
      * **Tiempo Real:** **Django Channels** para WebSockets.
      * **Autenticación:** DRF Simple JWT (JSON Web Tokens) para la autenticación basada en credenciales.
      * **Base de Datos:** **SQLite** (integrada con Django).
      * **Hashing:** Se usará `bcrypt` (integrado en Django) para todas las contraseñas.
2.  **Frontend:** **React 18+**
      * **Enrutamiento:** `react-router-dom`.
      * **Mapas:** `react-leaflet` (para OpenStreetMaps).
      * **Gestión de Estado:** React Context API (o Zustand, por su simplicidad) para el estado global (ej. usuario autenticado, alertas).
      * **WebSockets:** Cliente nativo de WebSocket o `reconnecting-websocket`.
      * **Estilos:** Migraremos `style.css` y usaremos CSS Modules o Styled Components para los nuevos componentes.
3.  **Repositorio:** Estructura de monorepo (o dos repositorios separados `backend` y `frontend`). Proporciona la estructura de carpetas ideal.

-----

### Fase 2: Diseño Detallado de la Base de Datos (SQLite con Django ORM)

Diseña los modelos de Django (`models.py`). Estos modelos deben ser la única fuente de verdad para la estructura de la base de datos.

```python
# backend/api/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

# 1. Modelo de Usuario Extendido
class User(AbstractUser):
    # Campos adicionales al User de Django
    RUT = models.CharField(max_length=12, unique=True)
    domicilio = models.CharField(max_length=255)
    SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    # 'edad' se puede calcular o agregar si es necesario, pero 'date_of_birth' es mejor
    fecha_nacimiento = models.DateField()
    
    # El campo 'is_staff' de Django se usará para marcar a los Administradores
    
    def save(self, *args, **kwargs):
        # Hashear contraseña si se está creando o modificando
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$')):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

# 2. Modelo del Ganado (Animal)
class Animal(models.Model):
    TIPO_ANIMAL_CHOICES = [
        ('OVINO', 'Ovinos'),
        ('BOVINO', 'Bovinos'),
        ('EQUINO', 'Equinos'),
    ]
    SEXO_ANIMAL_CHOICES = [('M', 'Macho'), ('H', 'Hembra')]

    collar_id = models.CharField(max_length=50, unique=True, primary_key=True)
    tipo_animal = models.CharField(max_length=10, choices=TIPO_ANIMAL_CHOICES)
    raza = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    peso_kg = models.FloatField()
    sexo = models.CharField(max_length=1, choices=SEXO_ANIMAL_CHOICES)
    color = models.CharField(max_length=50)
    
    # Relación para saber quién lo agregó (opcional pero útil)
    agregado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ganado_agregado')

    def __str__(self):
        return f"{self.tipo_animal} ({self.collar_id})"

# 3. Modelo de Datos de Telemetría (El que actualiza el WebSocket)
# Esta tabla crecerá rápidamente. En un sistema real, usaríamos TimeScaleDB, pero para SQLite está bien.
class Telemetria(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='telemetria')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    temperatura_corporal = models.FloatField()
    frecuencia_cardiaca = models.PositiveIntegerField() # Latidos por minuto

    class Meta:
        ordering = ['-timestamp'] # Ver los más recientes primero

# 4. Modelo de Alertas
class Alerta(models.Model):
    TIPO_ALERTA_CHOICES = [
        ('PERIMETRO', 'Fuera de Perímetro'),
        ('FIEBRE', 'Fiebre (Temp. Alta)'),
        ('HIPOTERMIA', 'Hipotermia (Temp. Baja)'),
        ('CARDIACO', 'Ritmo Cardíaco Anómalo'),
        ('INMOVIL', 'Inmovilidad Prolongada'),
    ]
    
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='alertas')
    # Asociamos la alerta a TODOS los usuarios (o a administradores)
    # Para la lógica de "leído/no leído" por usuario, necesitamos una tabla intermedia.
    timestamp = models.DateTimeField(auto_now_add=True)
    tipo_alerta = models.CharField(max_length=20, choices=TIPO_ALERTA_CHOICES)
    mensaje = models.TextField()
    
    def __str__(self):
        return f"Alerta {self.tipo_alerta} en {self.animal.collar_id}"

# 5. Tabla intermedia para estado de Alerta por Usuario (Campana de notificación)
class AlertaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertas_usuario')
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE, related_name='estados_usuario')
    leido = models.BooleanField(default=False)
    timestamp_leido = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'alerta') # Un usuario solo puede tener un estado por alerta

# 6. Modelo de Geocerca (Solo 1 para esta simulación)
class Geocerca(models.Model):
    # Almacenaremos los puntos como un JSON array de [lat, lng]
    # Ej: [[lat1, lng1], [lat2, lng2], [lat3, lng3], [lat1, lng1]]
    nombre = models.CharField(max_length=100, default="Perímetro Principal")
    puntos = models.JSONField() 
    # { "type": "Polygon", "coordinates": [ [ [lng1, lat1], [lng2, lat2], ... ] ] } (Formato GeoJSON)
    
    def __str__(self):
        return self.nombre
```

-----

### Fase 3: Desarrollo del Backend (Django, DRF y Channels)

Implementa la lógica del servidor.

#### 1\. Autenticación y Administración de Usuarios (DRF)

  * **Login:** Endpoint (`/api/token/`) usando DRF Simple JWT. Devuelve `access` y `refresh` tokens.
  * **Registro (Admin-only):** Endpoint (`/api/users/register/`). Debe requerir autenticación de administrador (`IsAdminUser`). Usará un `UserCreateSerializer` que maneje los campos personalizados (`RUT`, `domicilio`, etc.) y hashee la contraseña.
  * **CRUD de Usuarios (Admin-only):** Endpoints (`/api/users/`) para que el Admin pueda Listar, Actualizar y Eliminar trabajadores.

#### 2\. API de Administración de Ganado (DRF - Admin-only)

  * **CRUD de Ganado:** Endpoints (`/api/animales/`) para que el Admin pueda Crear, Leer, Actualizar y Eliminar ganado. Debe validar los `CHOICES` (Tipo, Sexo) y el `collar_id` único.

#### 3\. API de Mapas y Geocercas (DRF)

  * **Geocerca (Admin):** Endpoint (`/api/geocerca/`) (PUT/POST) para que el admin establezca/actualice los puntos del polígono.
  * **Geocerca (User):** Endpoint (`/api/geocerca/`) (GET) para que los usuarios lean la geocerca y la dibujen en el mapa.

#### 4\. API de Alertas (DRF - User)

  * **Listar Alertas:** Endpoint (`/api/alertas/`) que liste las alertas del usuario (usando la tabla `AlertaUsuario`). Debe mostrar el mensaje, hora y estado (leído/no leído).
  * **Marcar como Leído:** Endpoint (`/api/alertas/<int:pk>/leer/`) (POST) que cambie el estado de `leido` a `True` en el modelo `AlertaUsuario`.

#### 5\. Lógica de WebSockets (Django Channels)

  * Configura `Channels` con un `ASGIApplication` y un `WebsocketConsumer`.
  * **Consumer (`TrackerConsumer`):**
      * `connect()`: Acepta la conexión (idealmente tras verificar el JWT del usuario). Agrega al usuario a un grupo (`broadcast`).
      * `disconnect()`: Limpia.
      * `receive()`: (Opcional) El cliente puede enviar mensajes al servidor.
      * `send_animal_data(event)`: Envía los datos de telemetría (lat, lng, temp, hr) al grupo.
  * **Lógica de Simulación (El "Collar"):**
      * Crea un **Management Command** de Django (`simulate_collars`).
      * Este script se ejecuta en un bucle (`while True` con `time.sleep(5)`).
      * En cada iteración:
        1.  Obtiene todos los `Animal` de la BDD.
        2.  Obtiene la `Geocerca`.
        3.  Para cada animal, simula nuevos datos:
              * **Movimiento:** Calcula un pequeño delta aleatorio de `lat/lng` (simulando "caminar"). *Importante:* Verifica que el nuevo punto esté DENTRO de la geocerca (usa `shapely` o un algoritmo de "punto en polígono").
              * **Vitales:** Genera valores "normales" (Ej. Temp: 38.5-39.5°C, HR: 60-80 lpm).
        4.  Guarda los datos en el modelo `Telemetria`.
        5.  **Generación de Alertas:** Llama a una función `check_alerts(animal, new_data, geocerca)`.
        6.  **Broadcast:** Envía los nuevos datos (y cualquier alerta nueva) a través del `Channel Layer` al `TrackerConsumer`.

#### 6\. Lógica de Alertas y "URL Secreta"

  * **Función `check_alerts`:**
      * Compara la `new_data.temperatura` con rangos (ej. \> 40°C = Fiebre, \< 37.5°C = Hipotermia).
      * Compara `new_data.frecuencia_cardiaca` con rangos.
      * Compara `new_data.lat/lng` con la `Geocerca` (Alerta de Perímetro).
      * Si se dispara una alerta, crea un objeto `Alerta` y luego crea objetos `AlertaUsuario` (con `leido=False`) para **todos** los usuarios (o solo admins/trabajadores).
  * **URL Secreta de Emergencia:**
      * Crea una URL en Django (`/api/simulate_emergency/<str:collar_id>/<str:emergency_type>/`).
      * Esta vista (protegida o secreta) forzará al simulador a generar datos anómalos para el `collar_id` especificado (ej. `emergency_type='perimetro'` moverá al animal fuera de la cerca; `emergency_type='fiebre'` subirá su temperatura a 41°C).
      * Esto es crucial para demos y pruebas.

-----

### Fase 4: Desarrollo del Frontend (React)

Migra los HTML estáticos y construye la aplicación SPA.

#### 1\. Estructura de Componentes

```
/src
  /components
    /common
      - Navbar.js
      - LoadingSpinner.js
    /auth
      - LoginForm.js   (Proviene de login.html)
      - RequireAuth.js (Wrapper de rutas)
    /map
      - MapContainer.js (Contenedor de react-leaflet)
      - AnimalMarker.js (Muestra el emoji, maneja el clic)
      - GeofenceLayer.js (Dibuja el polígono de la geocerca)
    /dashboard
      - UserDashboard.js  (Contiene el mapa y la UI de usuario, de page.html)
      - NotificationBell.js (Maneja la lista de AlertaUsuario)
      - AnimalDetailsModal.js (Se abre al hacer clic en AnimalMarker)
    /admin
      - AdminDashboard.js (Layout principal de admin.html)
      - UserTable.js      (CRUD Usuarios)
      - AnimalTable.js    (CRUD Animales)
      - GeofenceEditor.js (Permite al admin dibujar en el mapa)
  /pages
    - LoginPage.js
    - DashboardPage.js
    - AdminPage.js
    - NotFoundPage.js
  /hooks
    - useAuth.js
    - useWebSocket.js
  /context
    - AuthContext.js
    - WebSocketContext.js
  - App.js
  - index.js
```

#### 2\. Flujo de React (Componente por Componente)

1.  **`App.js`:** Configura `react-router-dom` con las rutas (`/login`, `/`, `/admin`).
2.  **`LoginPage.js`:** Renderiza `LoginForm.js` (migrado de `login.html`). Al enviar, llama a la API (`/api/token/`), guarda el JWT en `localStorage` y actualiza el `AuthContext`.
3.  **`RequireAuth.js`:** Protege las rutas `/` y `/admin`. Redirige a `/login` si no hay JWT. Implementa lógica de roles (solo `is_staff=True` puede ir a `/admin`).
4.  **`UserDashboard.js` (Migración de `page.html`):**
      * Renderiza `MapContainer.js` y `NotificationBell.js`.
      * Establece la conexión WebSocket (usando `useWebSocket`).
      * Mantiene el estado de todos los animales (posición, vitales).
      * Al recibir un mensaje del WebSocket, actualiza el estado, causando que los `AnimalMarker` se muevan (re-render).
5.  **`MapContainer.js`:**
      * Usa `react-leaflet`.
      * Obtiene la `Geofence` (GET `/api/geocerca/`) y la dibuja usando `GeofenceLayer.js`.
      * Itera sobre el estado de los animales y renderiza un `AnimalMarker` para cada uno.
6.  **`AnimalMarker.js`:**
      * Renderiza un `L.DivIcon` (de Leaflet) para mostrar el emoji (🐑, G, 🐎) según `animal.tipo_animal`.
      * Al hacer clic, abre `AnimalDetailsModal.js` mostrando las coordenadas y vitales de ese animal.
7.  **`NotificationBell.js`:**
      * Obtiene datos de `/api/alertas/`.
      * Muestra un contador de alertas no leídas.
      * Al hacer clic, muestra un dropdown con el historial (hora, mensaje).
      * Permite hacer clic en "marcar como leído" (POST a `/api/alertas/<id>/leer/`).
8.  **`AdminDashboard.js` (Migración de `admin.html`):**
      * Tendrá pestañas para "Administrar Usuarios", "Administrar Ganado" y "Editar Geocerca".
      * Renderiza `UserTable.js` y `AnimalTable.js` (formularios para C, R, U, D).
      * Renderiza `GeofenceEditor.js` (un mapa donde el admin puede hacer clic para crear/actualizar el polígono).

-----

### Fase 5: Entrega

Genera el código para esta arquitectura. Comienza con el **Backend (Fase 2 y 3)**, definiendo los modelos, serializers y vistas (APIs y WebSockets). Luego, implementa el **Frontend (Fase 4)**, mostrando la migración de los HTML a componentes React funcionales que consuman la API. 

Genera una Aplicacion funcional.