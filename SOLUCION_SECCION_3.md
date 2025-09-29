# Soluciones de la Prueba Técnica

## Sección 3: API RESTful de Procesamiento de Pedidos

### Descripción del Problema
Desarrollar un endpoint de API RESTful que gestione pedidos de una plataforma de delivery, incluyendo:
1. Procesamiento de pedidos con múltiples productos
2. Cálculo de costos incluyendo envío basado en estrato
3. Aplicación de descuentos según el monto total
4. Respuesta JSON con detalles del pedido

### Diseño de la Solución

#### 1. Modelos de Datos (`models.py`)

```python
# Ejemplo de uso
from src.api.models import Product, OrderRequest

order_request = OrderRequest(
    products=[
        Product(
            id="1",
            name="Product 1",
            price=Decimal("50000"),
            quantity=2
        )
    ],
    stratum=3,
    address="Calle 123 #45-67"
)
```

**Decisiones de Diseño:**
- Uso de `Pydantic` para validación automática de datos
- Modelos inmutables para garantizar integridad de datos
- Uso de `Decimal` para precisión en cálculos monetarios
- Validación incorporada de rangos y valores permitidos
- Separación clara entre modelos de solicitud y respuesta

**Estructura de Modelos:**
- `Product`: Representa productos individuales con precio y cantidad
- `OrderRequest`: Encapsula productos y datos de envío
- `OrderResponse`: Estructura la respuesta con todos los costos

#### 2. Lógica de Negocio (`service.py`)

```python
# Ejemplo de uso
from src.api.service import OrderService

subtotal, shipping, discount, total = OrderService.calculate_order_totals(order)
```

**Decisiones de Diseño:**
- Separación de la lógica de negocio en una clase de servicio
- Uso de constantes para configuración de negocio
- Cálculos precisos con `Decimal`
- Reglas de descuento escalonadas
- Tarifas de envío basadas en estrato

**Reglas de Negocio Implementadas:**
1. Sistema de Descuentos:
   - 10% para pedidos > $100,000
   - 5% para pedidos > $50,000
   - 2% para pedidos > $20,000

2. Tarifas de Envío por Estrato:
   - Estrato 1: $2,000
   - Estrato 2: $3,000
   - Estrato 3: $4,000
   - Estrato 4: $5,000
   - Estrato 5: $6,000
   - Estrato 6: $7,000

#### 3. API Endpoint (`main.py`)

```python
# Ejemplo de solicitud HTTP
POST /api/v1/orders
{
    "products": [
        {
            "id": "1",
            "name": "Product 1",
            "price": "50000.00",
            "quantity": 2
        }
    ],
    "stratum": 3,
    "address": "Calle 123 #45-67"
}
```

**Características de la API:**
- Endpoint RESTful con FastAPI
- Validación automática de entrada
- Manejo consistente de errores
- Documentación automática (Swagger/OpenAPI)
- Respuestas tipadas

**Formato de Respuesta:**
```json
{
    "subtotal": "100000.00",
    "shipping_fee": "4000.00",
    "discount_amount": "5000.00",
    "total": "99000.00"
}
```

### Estrategia de Pruebas

La solución incluye pruebas exhaustivas que cubren:

1. Pruebas de Integración:
   - Procesamiento completo de pedidos
   - Validación de entrada
   - Códigos de estado HTTP
   - Formato de respuesta

2. Pruebas de Servicio:
   - Cálculo de descuentos
   - Tarifas de envío por estrato
   - Cálculos de totales
   - Manejo de casos límite

3. Casos de Prueba Específicos:
   - Pedidos sin descuento
   - Pedidos con diferentes niveles de descuento
   - Validación de estratos
   - Datos de productos inválidos
   - Casos límite de cantidades y precios

Para ejecutar las pruebas:
```bash
pytest tests/test_order_api.py -v
```

## Decisiones de Diseño y Compensaciones

### 1. Arquitectura y Organización

1. Separación de Responsabilidades:
   - Modelos para validación de datos
   - Servicio para lógica de negocio
   - API para manejo de HTTP
   - Tests independientes por componente

2. Elección de Tecnologías:
   - FastAPI por su rendimiento y tipado
   - Pydantic para validación robusta
   - Decimal para precisión monetaria

### 2. Consideraciones de Rendimiento

1. Validación Eficiente:
   - Validación temprana con Pydantic
   - Fail-fast para datos inválidos
   - Cálculos optimizados en el servicio

2. Manejo de Errores:
   - Errores HTTP apropiados
   - Mensajes de error descriptivos
   - Validación automatizada

### 3. Extensibilidad

La solución está diseñada para ser fácilmente extensible:
- Nuevas reglas de descuento
- Modificación de tarifas por estrato
- Adición de nuevos campos
- Versioning de API incluido