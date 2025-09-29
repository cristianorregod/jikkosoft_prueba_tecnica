# Prueba Técnica Jikkosoft

Este repositorio contiene la solución a la prueba técnica de Jikkosoft, que abarca tres secciones principales:
estructuras de datos y Ambos scripts de demostración (`analyze_customers.py` y `demo_transport_routes.py`) están completamente documentados y sirven como referencia para la implementación de casos de uso personalizados.


## Enlaces Importantes

- [Prueba Técnica Original](PRUEBA_TECNICA.md)
- [Solución Sección 1: Estructuras de Datos y Algoritmos](SOLUCION_SECCION_1.md)
- [Solución Sección 2: Diseño de Sistemas](SOLUCION_SECCION_2.md)
- [Solución Sección 3: API RESTful](SOLUCION_SECCION_3.md)

## Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual de Python (recomendado)

## Procedimiento de Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/cristianorregod/jikkosoft_prueba_tecnica.git
cd jikkosoft_prueba_tecnica
```

2. Creación y activación del entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
# O en Windows:
# .venv\Scripts\activate
```

3. Instalación de dependencias:
```bash
pip install -r requirements.txt
```

4. Instalación del paquete en modo desarrollo:
```bash
pip install -e .
```

## Estructura del Proyecto

```
├── src/
│   ├── api/                    # API RESTful (Sección 3)
│   │   ├── main.py            # Endpoints de la API
│   │   ├── models.py          # Modelos de datos
│   │   └── service.py         # Lógica de negocio
│   ├── customer_analytics.py   # Análisis de clientes (Sección 1)
│   └── transport_routes.py     # Sistema de rutas (Sección 1)
├── tests/                      # Tests unitarios
├── media/                      # Diagramas y recursos visuales
└── requirements.txt           # Dependencias del proyecto
```

## Ejecución de Tests

Para ejecutar todos los tests con cobertura:

```bash
pytest tests/ -v --cov=src
```

Para ejecutar tests específicos:

```bash
# Tests de la API
pytest tests/test_order_api.py -v

# Tests del sistema de rutas
pytest tests/test_transport_routes.py -v

# Tests del análisis de clientes
pytest tests/test_customer_analytics.py -v
```

## Pruebas de las Soluciones

### Sección 1: Análisis de Clientes y Sistema de Rutas

El proyecto incluye scripts de demostración listos para ejecutar que muestran el funcionamiento de ambos sistemas.

#### Análisis de Clientes

Para ejecutar el script de demostración que ya está implementado:

```bash
python src/analyze_customers.py
```

Este script contiene un ejemplo completo del análisis de clientes. El código fuente permite modificaciones para probar diferentes escenarios, como:
- Modificación del número de transacciones generadas
- Ajuste del rango de fechas
- Configuración de límites de clientes a mostrar
- Personalización de rangos de montos de transacciones

La clase también puede ser utilizada en código personalizado:

```python
from src.customer_analytics import CustomerAnalytics

# Crear una instancia del analizador
analyzer = CustomerAnalytics()

# Generar datos de ejemplo
analyzer.generate_transaction_data(100)  # Genera 100 transacciones aleatorias

# Obtener top clientes
top_customers = analyzer.get_top_customers(
    start_date="2025-01-01",
    end_date="2025-12-31",
    limit=10
)

print("Top 10 clientes por monto total de compras:")
for customer in top_customers:
    print(f"Cliente ID: {customer.customer_id}")
    print(f"Monto Total: ${customer.total_amount}")
    print(f"Número de Transacciones: {customer.transaction_count}")
    print("---")
```

#### Sistema de Rutas

El script de demostración se puede ejecutar con el siguiente comando:

```bash
python src/demo_transport_routes.py
```

Este script incluye un ejemplo completo del sistema de rutas con varios escenarios. El código fuente permite:
- Adición de más rutas y paradas
- Evaluación de diferentes patrones de conexión entre paradas
- Simulación de casos de uso específicos
- Validación del comportamiento con datos personalizados

La clase también puede ser utilizada en código personalizado:

```python
from src.transport_routes import TransportRouteSystem

# Crear sistema de rutas
route_system = TransportRouteSystem()

# Agregar rutas
route_system.add_route("R1", "Ruta Norte")
route_system.add_stop_to_route("R1", "Parada A")
route_system.add_stop_to_route("R1", "Parada B")

# Consultar paradas en una ruta
stops = route_system.get_stops_in_route("R1")
print(f"Paradas en R1: {stops}")

# Consultar rutas por parada
routes = route_system.get_routes_by_stop("Parada A")
print(f"Rutas que pasan por Parada A: {routes}")
```

Los scripts de demostración (`analyze_customers.py` y `demo_transport_routes.py`) están completamente documentados y sirven como referencia para la implementación de casos de uso personalizados.

### Sección 2: Diseño de Sistema y Arquitectura

La solución propuesta aborda el rediseño del sistema backend para una start-up de reparto de comida a domicilio, transformando una aplicación monolítica en una arquitectura distribuida. Los aspectos principales del diseño incluyen:

**Componentes Principales:**
- **API Gateway**: Control centralizado de seguridad, autenticación JWT, rate limiting y routing
- **Auth Service**: Gestión de autenticación y roles (cliente, restaurante, driver, admin)
- **Order Service**: Gestión de pedidos con Postgres y Redis para caché
- **Restaurant Service**: Administración de catálogo y disponibilidad
- **Driver Service**: Gestión de domiciliarios con tracking en tiempo real
- **Matching Service**: Algoritmo de emparejamiento pedido-domiciliario
- **Payment Service**: Procesamiento de pagos y manejo de pasarelas
- **Notification Service**: Envío de notificaciones multicanal

El diseño incorpora comunicación tanto síncrona como asíncrona mediante eventos de negocio (`order.created`, `payment.completed`, etc.), utilizando un broker de mensajes para garantizar la resiliencia del sistema.

La documentación completa incluye:
- [Diseño detallado de la arquitectura](SOLUCION_SECCION_2.md)
- [Diagrama completo del sistema](/media/system_design_jijkkosoft.png)
- [Esquema de base de datos relacional](/media/base_database_schema.png)
- [Especificación OpenAPI de los endpoints](api_design.yaml)
- [Flujos de procesos principales](/media/create_order_flow.png)
- [Documentación API](https://app.swaggerhub.com/apis-docs/colraices/Jikkosoft_Delivery_API/1.0.0)

Para más detalles sobre la arquitectura, patrones utilizados y decisiones de diseño, se recomienda consultar la [documentación completa de la solución](SOLUCION_SECCION_2.md).

### Sección 3: API RESTful

La API está implementada usando FastAPI. Instrucciones de ejecución:

1. Iniciar el servidor:
```bash
uvicorn src.api.main:app --reload
```

2. Ejemplo de creación de una orden mediante curl:
```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d '{
    "products": [
      {
        "id": "1",
        "name": "Producto 1",
        "price": "100.00",
        "quantity": 2
      }
    ],
    "stratum": 3,
    "address": "Calle 123 #45-67"
  }'
```

3. Documentación de la API disponible en:
- OpenAPI (Swagger): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Diagramas y Documentación

- [Diagrama del Sistema](media/system_design_jikkosoft.png)
- [Flujo de Creación de Órdenes](media/create_order_flow.png)
- [Esquema de Base de Datos](media/base_database_schema.png)

## Tecnologías Utilizadas

- FastAPI: Framework web para la API RESTful
- Pydantic: Validación de datos y serialización
- pytest: Framework de testing
- coverage: Medición de cobertura de código

## Detalles de Implementación

- Uso de Decimal para cálculos monetarios, evitando problemas de precisión con números flotantes
- Validación de datos a nivel de modelo mediante Pydantic
- Cobertura de tests para casos positivos y negativos
- Sistema de descuentos basado en el monto total de la orden
- Cálculo de costo de envío según estrato socioeconómico

## Mejoras Propuestas

- Implementación de autenticación y autorización
- Incorporación de caché para optimización de consultas
- Implementación de rate limiting
- Incorporación de logging detallado
- Integración con sistema de base de datos persistente