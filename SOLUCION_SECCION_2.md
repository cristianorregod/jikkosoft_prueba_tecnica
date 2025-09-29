# Soluciones de la Prueba Técnica

## Sección 2: Diseño y Arquitectura del Sistema

### Descripción del Problema
**Escenario:** Una start up local de reparto de comida a domicilio está 
experimentando un rápido crecimiento. Necesita rediseñar su sistema 
backend para mejorar la escalabilidad, la fiabilidad y la facilidad de 
mantenimiento. El sistema actual es una aplicación monolítica con un 
rendimiento limitado.  
**Diseñe**  una arquitectura de sistema distribuida que aborde estos 
desafíos. Considere factores como el diseño de la base de datos, el 
diseño de la API, las colas de mensajes y el almacenamiento en 
caché

### Diseño de la Solución

**1. Arquitectura**

Sistema orientado a microservicios, event-driven para escalabilidad y resiliencia, con consistencia eventual en flujos de negocio que no requieren bloqueo fuerte (p. ej. asignación de repartidor).

**Diagrama lógico simplificado del diseño del sistema**
<img src="https://res.cloudinary.com/dvjzp6scj/image/upload/v1759122481/projects/system_design_jikkosoft_orinao.svg" />

**Componentes y Responsabilidades**

**API Gateway**
- Funciones: Centraliza el control de seguridad y políticas necesarias rediciendo la carga en los servicios, encargandose de la Autenticación ((JWT passthrough)), Rate limiting, TLS termination, Routing, Request/Response Logging, CORS.

**Auth Service**
- Funciones: Administra la autenticación al sistema, refresh tokens, roles (cliente, restaurante, driver, admin). Este bien uede ser un servicio de terceros o propiamente desarrollado a la medida que se requiera.

**Order Service**
- Funciones: Se encargar de la creación de los pedidos, actualización de estados, historial.
- Almacenamiento: Aquí la planteación es Postgres y uso de una Caché como Redis.
- Eventos: El servicio expone eventos en la creación y actualización de las ordenes [`order.created`, `order.updated`, `order.cancelled`].

**Restaurant Service**
- Funciones: Catálogo de restaurantes, menús, disponibilidad, tiempos estimados.
- Almacenamiento: Postgres para datos maestros y caché en Redis.

**Driver Service**
- Funciones: Perfiles de domiciliarios, estado, ubicación en tiempo real.
- Ubicación: Con geo-index en Redis y en Postgres persistir últimas posisciones para temas de auditoría y análisis.
- Comunicación: Implementación de wensockets para comunicación inmediata.

**Matching Service**
- Funciones: Algoritmo de emparejamiento de pedidos con el domiciliario (Driver) más óptimo teniendo en cuenta variables como (distancia, rating, tiempo estimado, carga).
- Herramientas: Utilizar indexación geoespacial para determinar los Drivers cercanos

**Payment Service**
- Funciones: Cobros, reembolsos, conciliación, handler de pasarelas de pago.
- Restricciones: Al tratarse de un servicio de pagos, es sensible a PCI por lo cual no se deben almacenar PAN completos, en lugar de ello utilizar tokens de las pasarelas de pago.

**Notification Service**
- Funciones: Envío de correos, SMS, notificaciones push.
- Eventos: Este servicio se suscribe a eventos de ordenes y driver

**2. Comunicación entre servicios**

En este escenario se opta por `sincronía` y `asincronía` según determinados momentos o casos.
- **Comunicación Síncrona:** En peticiones directas del cliente al sistema como autenticación, detalles de un pedido, entre otros.
- **Comunicación Asíncrona:** Utilizar algún Broker de mensajes (Kafka/RabbitMQ) para eventos de negocio para asegurar resiliencia y re-procesamiento (colas, sistema de reintentos).

**3. Diseño de base de datos**
Se plantean las tablas que considero más importantes para el sistema optando en este escenario por un esquema SQL.
<img src="https://res.cloudinary.com/dvjzp6scj/image/upload/v1759122428/projects/base_database_schema_kdzr6u.png"/>

👉 <a href="/base_database_ddl.sql" target="_blank">DDL para creación de tablas</a>

**4. Topics para eventos**

A continuación listo algunos de los eventos que pueden emplearse en el sistema:

*Ordenes (order)*
- `order.created`
- `order.updated`
- `order.cancelled`

*Pagos (payment)*
- `payment.initiated`
- `payment.completed`

*Domiciliario (driver)*
- `driver.location.updated`
- `driver.status.changed`

**5. Flujo de Creación de Orden**

A muy alto nivel suministro un ejemplo de lo que sería el fluj basico para la creación de una orden pasando por el pago y asignación de domiciliario (Driver).
<img src="https://res.cloudinary.com/dvjzp6scj/image/upload/v1759119123/projects/create_order_flow_tyjcbl.png"/>

**6. Diseño de la API**

Para el ejercicio detallaré algunos de los endpoints principales para el sistema. Se realiza la estructura de la API en formato OpenAPI en archivo <a href="/api_design.yaml" target="_blank">api_design.yaml</a> y puede visualizarse en el siguiente enlace 👉 <a href="https://app.swaggerhub.com/apis-docs/colraices/Jikkosoft_Delivery_API/1.0.0" target="_blank">Jikkosoft_Delivery_API</a>
