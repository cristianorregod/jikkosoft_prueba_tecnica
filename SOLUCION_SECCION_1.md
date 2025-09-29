# Soluciones de la Prueba Técnica

## Pregunta 1: Análisis de Transacciones de Clientes

### Descripción del Problema
Desarrollar un sistema para analizar las transacciones de clientes de una plataforma de comercio electrónico, incluyendo:
1. Generación de grandes conjuntos de datos de transacciones
2. Identificación eficiente de los 10 clientes más frecuentes en un período específico

### Diseño de la Solución

#### 1. Generación de Datos (`CustomerAnalytics.generate_transaction_data`)

```python
# Ejemplo de uso
from datetime import datetime
from src.customer_analytics import CustomerAnalytics

analytics = CustomerAnalytics()
transactions = analytics.generate_transaction_data(
    num_transactions=100000,
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31),
    num_customers=10000
)
```

**Decisiones de Diseño:**
- Uso de `dataclass` para objetos Transaction para una representación limpia de datos
- Las marcas de tiempo se generan aleatoriamente dentro del rango de fechas especificado
- Los IDs de cliente siguen un formato consistente (CUST000001)
- Los montos de transacción son realistas ($1-$1000)
- Los resultados se ordenan por marca de tiempo para simular un orden del mundo real

**Análisis de Complejidad:**
- Complejidad Temporal: O(n log n) donde n es num_transactions (debido al ordenamiento final)
- Complejidad Espacial: O(n) para almacenar n transacciones

#### 2. Análisis de Clientes Principales (`CustomerAnalytics.get_top_customers`)

```python
# Ejemplo de uso
top_customers = analytics.get_top_customers(
    transactions=transactions,
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 6, 30),
    top_n=10
)
```

**Decisiones de Diseño:**
- Utiliza un montículo mínimo (min-heap) para mantener los N clientes principales de manera eficiente
- Emplea un diccionario para contar las frecuencias de los clientes
- Devuelve resultados ordenados por frecuencia (descendente) y ID de cliente

**Análisis de Complejidad:**
- Complejidad Temporal: O(n log k) donde:
  - n = número de transacciones
  - k = número de clientes principales solicitados (típicamente 10)
- Complejidad Espacial: O(m) donde m es el número de clientes únicos

**Características Principales:**
- Manejo eficiente de grandes conjuntos de datos
- Filtrado por rango de fechas
- Desempate por ID de cliente
- Validación de entrada
- Eficiente en memoria para procesamiento de datos en streaming

## Pregunta 2: Gestión de Rutas de Transporte Público

### Descripción del Problema
Diseñar una estructura de datos para gestionar rutas de transporte público con operaciones eficientes para:
- Gestión de rutas y paradas
- Operaciones de consulta por parada
- Adición/eliminación de paradas

### Diseño de la Solución

#### Estructura de Datos (`TransportRouteSystem`)

```python
# Ejemplo de uso
from src.transport_routes import TransportRouteSystem, Stop

system = TransportRouteSystem()

# Agregar rutas y paradas
system.add_route("route1")
stop = Stop("stop1", "Estación Central")
system.add_stop_to_route("route1", stop)

# Consultar rutas por parada
routes = system.get_routes_by_stop("stop1")
```

**Decisiones de Diseño:**
1. Mapeo Bidireccional:
   - `routes: Dict[str, Set[Stop]]` para el mapeo ruta → paradas
   - `stop_to_routes: Dict[str, Set[str]]` para el mapeo parada → rutas

2. Uso de Conjuntos (Sets):
   - Operaciones O(1) para agregar/eliminar paradas
   - Pruebas de pertenencia O(1)
   - Sin paradas duplicadas en rutas

**Análisis de Complejidad:**

Todas las operaciones tienen complejidad temporal O(1):
- `add_route`: O(1)
- `add_stop_to_route`: O(1)
- `remove_stop_from_route`: O(1)
- `get_routes_by_stop`: O(1)
- `get_stops_in_route`: O(1)

Complejidad Espacial:
- O(R * S) donde:
  - R = número de rutas
  - S = promedio de paradas por ruta

**Características Principales:**
- Consultas eficientes en ambas direcciones
- Mantiene consistencia de datos
- Validación exhaustiva de entradas
- Mensajes de error claros
- Implementación eficiente en memoria

### Estrategia de Pruebas

Ambas soluciones incluyen suites de pruebas completas que cubren:
1. Funcionalidad básica
2. Casos extremos y validación de entrada
3. Pruebas de rendimiento con grandes conjuntos de datos
4. Escenarios complejos
5. Consistencia de datos

Para ejecutar las pruebas:
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pruebas con cobertura
pytest --cov=src tests/
```

## Decisiones de Diseño y Compensaciones

### Pregunta 1: Análisis de Clientes

1. Memoria vs Velocidad:
   - El enfoque de min-heap equilibra el uso de memoria con el rendimiento
   - Adecuado para procesamiento de datos en streaming
   - Puede manejar conjuntos de datos más grandes que la memoria disponible

2. Generación de Datos:
   - Distribución realista de datos
   - Salida ordenada para simulación del mundo real
   - Parámetros configurables para pruebas

### Pregunta 2: Rutas de Transporte

1. Elección de Estructura de Datos:
   - Mapeo bidireccional para operaciones O(1)
   - Conjuntos para búsquedas y unicidad eficientes
   - Uso adicional de memoria justificado por las ganancias en rendimiento

2. Diseño de API:
   - Nombres y firmas de métodos claros
   - Manejo consistente de errores
   - Objetos Stop inmutables para integridad de datos