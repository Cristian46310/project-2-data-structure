# Proyecto: Simulación de Viajes Intergalácticos con Burro Científico

Este proyecto implementa una simulación de viajes intergalácticos en un entorno de constelaciones, donde un burro científico realiza misiones, gestiona su energía, consume pasto y enfrenta eventos como enfermedades y saltos hipergigantes. El sistema permite la gestión dinámica de caminos entre estrellas, así como la actualización de estados y recursos del burro.

## Estructura de Archivos

### Back\utils\DonkeySimulation.py

Contiene la clase principal `DonkeySimulation` que gestiona la lógica de simulación del burro:
- **Gestión de energía y pasto:** Métodos para calcular energía consumida, regeneración al comer pasto y validación de límites.
- **Simulación de rutas:** Ejecuta el recorrido entre estrellas, considerando distancias, consumo de recursos y eventos especiales.
- **Enfermedades:** Simula la probabilidad y efectos de enfermedades durante las misiones.
- **Saltos hipergigantes:** Permite al burro saltar entre galaxias, recargando energía y duplicando pasto.
- **Gestión de caminos:** Permite bloquear o habilitar conexiones entre estrellas (requiere soporte en el controlador).
- **Actualización de configuración:** Modifica el estado del burro en el archivo de configuración tras cada simulación.

### Back\Repository\ReadConstellations.py

Clase `ReadConstellations` para la lectura y manipulación del archivo JSON de constelaciones:
- **Lectura de datos:** Obtiene todas las constelaciones, estrellas, enlaces y propiedades específicas.
- **Gestión de conexiones:** Permite bloquear/habilitar caminos entre estrellas modificando el campo `enabled` en los enlaces.
- **Utilidades:** Métodos para obtener distancias, tiempos de estancia, energía disponible y búsqueda por ID o nombre.

### Back\Controller\ControllerConstellations.py

Controlador que abstrae el acceso a los servicios de constelaciones:
- **Interfaz de acceso:** Métodos para obtener constelaciones, estrellas, enlaces y propiedades específicas.
- **Gestión de caminos:** Expone el método `setConnectionStatus` para bloquear/habilitar caminos entre estrellas, delegando la lógica al servicio correspondiente.

### Back\Services\ServiceConfig.py

Servicio que gestiona la configuración persistente del burro:
- **Lectura y escritura:** Permite obtener, crear y modificar la configuración del burro mediante métodos simples.
- **Persistencia:** Utiliza un repositorio de configuración para todas las operaciones de entrada/salida.

### Back\Services\SerivceReadConstellations.py

Servicio que expone operaciones de lectura y gestión ligera sobre constelaciones y estrellas:
- **Interfaz estable:** Proporciona métodos para obtener constelaciones, estrellas, enlaces, distancias y propiedades específicas.
- **Gestión de conexiones:** Permite habilitar o bloquear caminos entre estrellas mediante el método `manageConnection`.
- **Encapsulamiento:** Actúa como capa intermedia entre el controlador y el repositorio de constelaciones.

### Back\utils\FlujoOptimo.py

Implementa el algoritmo de Dijkstra para encontrar rutas óptimas entre estrellas:
- **Construcción de grafo:** Genera un grafo dirigido y ponderado a partir de los datos de constelaciones, ignorando enlaces bloqueados.
- **Búsqueda de ruta óptima:** Calcula el camino más corto entre dos estrellas usando Dijkstra, retornando la distancia total y la secuencia de estrellas.
- **Integración:** Utiliza el controlador de constelaciones para obtener datos y resolver nombres de estrellas.

## Dependencias

- Python 3.13.9
- Estructura de carpetas y archivos JSON según el modelo del proyecto.


## Uso

1. Configura el archivo de constelaciones en `back/Data/Constellations.json` con la estructura esperada.
2. Utiliza las clases y métodos para simular rutas, gestionar recursos y modificar conexiones entre estrellas.
3. Los métodos de gestión de caminos permiten a los científicos bloquear o habilitar rutas en tiempo real.



