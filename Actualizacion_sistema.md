🟢 SÚPER PROMPT V2: Evolución del Sistema "CAMPORT"
Rol: Actúa como un Arquitecto de Software y Desarrollador Fullstack Senior con más de 10 años de experiencia, especializado en arquitecturas en tiempo real, Django y React.

Contexto Anterior: Ya hemos definido y (conceptualmente) construido una aplicación de monitoreo de ganado (descrita en el "Contexto.md" original). Esta V1 incluye un backend (Django, DRF, Channels, SQLite), un frontend (React, Leaflet) y una simulación de telemetría por WebSockets. La V1 tiene una limitación de una sola geocerca y una administración de animales básica.

Misión: Se me ha asignado la tarea de tomar el sistema V1 existente y liderar su actualización a la Versión 2.0, que se llamará oficialmente "CAMPORT". Debes integrar una serie de mejoras críticas, enfocadas en la administración avanzada de geocercas, la asignación de animales, la generación de IDs, y la mejora de la UI/UX del panel de administración.

IMPORTANTE: Todos los cambios deben realizarse sobre la arquitectura ya definida en el contexto original (Django 4.x/5.x, React 18, DRF, Channels, SQLite, Simple JWT). No estás creando un stack nuevo, estás actualizándolo.

🎯 Requerimientos Clave de la Actualización (V2.0)
Debes modificar el sistema V1 para implementar lo siguiente:

Nomenclatura y Acceso:

El nombre oficial del sistema ahora es "CAMPORT".

En la Navbar de la página principal (la que contiene el mapa de gestión, UserDashboard.js), se debe agregar un botón que lleve al "Panel de Administración" (/admin).

Este botón solo debe ser visible si el usuario autenticado tiene el flag is_staff=True (obtenido del AuthContext de React).

Lógica de Animales y Alertas:

ID de Animal Personalizado: El modelo Animal debe generar un ID legible y diferido por tipo. Por ejemplo: 'OVINO-001', 'BOVINO-001', 'OVINO-002'.

Recomendación de Arquitectura: El collar_id (PK original) debe mantenerse como el identificador de hardware (un UUID o CharField único). Debes agregar un nuevo campo llamado display_id (CharField, editable=False, unique=True) que se genere automáticamente en el método save() del modelo Animal calculando el siguiente número para su tipo_animal.

Alertas de Vitales (Énfasis): Asegurar que la función de simulación check_alerts genere y envíe alertas fiables a través de WebSockets para todos los signos vitales anómalos (Fiebre: Temp Alta, Hipotermia: Temp Baja, Cardíaco: Ritmo Anómalo), además de la alerta de perímetro. La NotificationBell.js debe recibirlas.

Administración Avanzada de Geocercas (El Mayor Cambio):

Múltiples Geocercas (Backend):

Eliminar la limitación de "Solo 1 geocerca". El modelo Geocerca debe ser un ModelViewSet completo de DRF (/api/geocerca/) que permita Crear, Leer (Lista), Actualizar y Eliminar múltiples geocercas.

Cada geocerca debe tener su propio ID (el ID de Django) y su JSONField de puntos.

Asignación de Animales (Backend):

Modificar el modelo Animal para incluir una ForeignKey al modelo Geocerca. Cada animal debe estar asignado a una (y solo una) geocerca.

El CRUD de Animales (/api/animales/) debe permitir asignar una geocerca_id al crear o actualizar un animal.

Lógica de Simulación (Backend):

Actualizar el Management Command (simulate_collars). Al iterar, el script debe obtener la geocerca específica asignada a ese animal (ej. animal.geocerca).

La alerta de perímetro se debe disparar solo si el animal sale de su geocerca asignada.

Visualización (Frontend):

El mapa principal (MapContainer.js) debe obtener y renderizar todas las geocercas creadas (GET a /api/geocerca/), no solo una.

Editor de Geocercas (Frontend - Admin):

El GeofenceEditor.js debe ser más sofisticado:

Debe mostrar una lista de las geocercas existentes y permitir seleccionar una para editar o crear una nueva.

Al editar una geocerca, el admin debe poder hacer clic en un punto (vértice) existente del polígono en el mapa.

Al seleccionar un vértice, debe aparecer un "minimapa" (en un modal) que permita al admin hacer clic para seleccionar las nuevas coordenadas solo para ese punto.

Al guardar, se actualiza el JSONField de puntos para esa geocerca específica (PUT/PATCH a /api/geocerca/<id>/).

Fase 1: Actualización de Modelos de BDD (models.py)
Genera el código actualizado para backend/api/models.py. Enfócate en los cambios en Animal y Geocerca.

Geocerca: Asegúrate de que el modelo Geocerca (que ya existe) esté listo para múltiples instancias (básicamente, no necesita cambios, pero su uso cambia).

Animal: Agrega los nuevos campos:

display_id = models.CharField(...)

geocerca = models.ForeignKey(Geocerca, on_delete=models.SET_NULL, null=True, blank=True, related_name='animales')

Animal.save(): Sobrescribe este método para implementar la lógica de generación del display_id (ej. OVINO-001, OVINO-002).

Fase 2: Actualización del Backend (API y Simulación)
Genera el código actualizado para las Vistas, Serializers y el Management Command.

api/serializers.py:

Actualiza AnimalSerializer para incluir geocerca (como PrimaryKeyRelatedField) y display_id (como read_only).

Crea un GeocercaSerializer (ModelSerializer).

api/views.py:

Asegúrate de que GeocercaViewSet sea un ModelViewSet completo (no solo GET/POST único).

Asegúrate de que AnimalViewSet maneje la asignación de geocerca.

api/management/commands/simulate_collars.py:

Actualiza la lógica del bucle while True.

El bucle debe:

Obtener el animal y su animal.geocerca asociada.

Simular movimiento y vitales.

Llamar a check_alerts(animal, new_data, animal.geocerca).

La función check_alerts debe generar alertas para vitales (fiebre, hipotermia, cardíaco) y perímetro (solo si está fuera de su geocerca).

Fase 3: Actualización del Frontend (React)
Genera el código actualizado para los componentes de React que sufren modificaciones.

components/common/Navbar.js (o UserDashboard.js):

Muestra la lógica para renderizar el botón "Panel de Administración" condicionalmente, usando un AuthContext para verificar user.is_staff.

components/map/MapContainer.js:

Muestra cómo hacer fetch a la lista de /api/geocerca/.

Muestra cómo iterar (.map()) sobre esa lista para renderizar múltiples componentes GeofenceLayer.

components/admin/AnimalTable.js (o AnimalForm.js):

Muestra cómo el formulario de "Crear/Editar Animal" ahora incluye un <select> para asignar una geocerca (cargando las opciones desde /api/geocerca/).

components/admin/GeofenceEditor.js (Componente Crítico):

Este es el componente más complejo. Muestra su estructura:

Estado para la lista de geocercas (geofences).

Estado para la geocerca seleccionada (selectedGeofence).

Un mapa de react-leaflet que dibuja los polígonos.

Lógica para hacer clic en un vértice (Marker de Leaflet) del polígono seleccionado.

Un Modal que contiene el "Minimapa" para seleccionar el nuevo punto.

Función handleSave que envía los puntos actualizados vía API (PUT/PATCH).

Fase 4: Entrega
Genera los cambios correspondientes dentro del codigo y verifica su funcionamiento final 