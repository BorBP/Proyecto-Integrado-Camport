Rol: Actúa como un Arquitecto de Software y Desarrollador Fullstack Senior con más de 10 años de experiencia, especializado en arquitecturas en tiempo real, Django y sistemas de simulación geoespacial.

Contexto Anterior: Ya hemos definido y actualizado nuestro sistema "CAMPORT" (Versión 2.0). Contamos con un backend en Django que soporta múltiples geocercas y un frontend en React. La simulación de movimiento actual (simulate_collars) utiliza un Management Command que asigna animales a geocercas, pero el movimiento es un simple "random walk" (delta aleatorio), lo que provoca que los animales se escapen con demasiada frecuencia.

Misión: Se me ha asignado la tarea de evolucionar la simulación de movimiento para hacerla más realista y robusta. Debemos implementar dos cambios clave en el Management Command del backend:

Inicialización en el Centro: Los animales deben comenzar su simulación desde el centro de la geocerca a la que están asignados.

Lógica de "Pastoreo Virtual": Los animales deben "intentar" permanecer dentro de su geocerca. Las alertas por fugas de perímetro deben ser raras y deliberadas, no un subproducto de un movimiento aleatorio.

IMPORTANTE: Esta actualización se centra exclusivamente en el backend, específicamente en el archivo backend/api/management/commands/simulate_collars.py. Se asumirá el uso de la librería shapely (ya introducida en V2) para los cálculos geoespaciales.

🎯 Requerimientos Clave de la Actualización (V3.0)
Debes modificar el script simulate_collars para implementar la siguiente lógica:

1. Inicialización en el Centroide de la Geocerca
Al ejecutarse el comando, antes de iniciar el bucle de movimiento, debe verificar la posición inicial de cada animal.

Lógica:

Para cada animal en la base de datos:

Verificar si el animal tiene registros de telemetría previos (animal.telemetria.exists()).

Si NO tiene telemetría (y tiene una geocerca asignada):

Obtener los puntos de animal.geocerca.puntos.

Usar shapely.geometry.Polygon para crear un objeto de polígono.

Calcular el centroide del polígono (polygon.centroid).

Crear el primer registro de Telemetria para ese animal usando las coordenadas del centroide (lat=centroid.y, lng=centroid.x), con signos vitales base.

Si SÍ tiene telemetría, se utiliza la última posición conocida para el siguiente paso.

2. Algoritmo de Movimiento de "Pastoreo Virtual" (Evitar Fugas)
La lógica principal dentro del bucle while True debe ser reemplazada. El simple "delta aleatorio" ya no es suficiente.

Lógica de "Propuesta y Corrección":

Para cada animal:

Obtener la última telemetría (lat_actual, lng_actual).

Obtener la geocerca asignada y crear su objeto shapely.geometry.Polygon.

Proponer un Movimiento: Calcular una posición propuesta (lat_propuesta, lng_propuesta) sumando un pequeño delta aleatorio a la posición actual (como se hacía antes).

Verificar Límite: Crear un shapely.geometry.Point(lng_propuesta, lat_propuesta).

Usar geocerca_polygon.contains(punto_propuesto) para verificar si el animal sigue dentro de la geocerca.

Si SÍ (Movimiento Válido):

El movimiento es seguro. Guardar la Telemetria con la lat_propuesta y lng_propuesta.

Si NO (Intento de Fuga):

El animal "chocó" con el límite virtual.

Descartar el movimiento propuesto.

Calcular un Movimiento Corregido: Calcular un nuevo movimiento que "rebote" o "se aleje" del borde. La estrategia más simple es calcular un vector desde la posición actual hacia el centroide de la geocerca y dar un pequeño paso en esa dirección.

Guardar la Telemetria con esta nueva posición corregida (que lo empuja de vuelta al centro).

Resultado Esperado: Con esta lógica, los animales deambularán aleatoriamente dentro de la geocerca, y al acercarse a los bordes, serán "empujados" sutilmente hacia el centro. Esto hará que las alertas de perímetro solo se activen si la URL de emergencia (/api/simulate_emergency/) fuerza una coordenada fuera de los límites, que es exactamente el comportamiento deseado para una demo.

Fase 1: Actualización del Backend (Management Command)
Genera el código completo y actualizado para backend/api/management/commands/simulate_collars.py.

Asegúrate de incluir las importaciones necesarias (time, random, shapely.geometry).

Implementa la lógica de Inicialización en el Centroide (el chequeo if not animal.telemetria.exists()).

Implementa la nueva lógica de bucle while True con el algoritmo de "Pastoreo Virtual" (Propuesta y Corrección).

Asegúrate de que la función check_alerts (que ya existe) se siga llamando con los datos de telemetría finales (ya sean los propuestos o los corregidos).

Fase 2: Dependencias
Confirma que shapely esté en backend/requirements.txt, ya que ahora es fundamental para la simulación.