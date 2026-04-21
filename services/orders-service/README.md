# Orders Service

Microservicio para la gestión de órdenes en un sistema e-commerce. Construido con Node.js, Express y MongoDB (Mongoose).

## Comunicación entre Microservicios

Este servicio utiliza **Axios** para validar la integridad de los datos consultando a otros servicios:
* **Users Service**: Valida que el `user_id` exista antes de crear la orden.
* **Products Service**: Valida que cada `product_id` exista antes de crear la orden.

> [!IMPORTANT]
> Para que el `POST /api/orders` funcione correctamente, los servicios de **Usuarios** y **Productos** deben estar en ejecución, o de lo contrario el servicio de órdenes devolverá un error de validación.

## Endpoints

* **GET** `/api/orders` - Obtener todas las órdenes.
* **GET** `/api/orders/{id}` - Obtener una orden por ID.
* **POST** `/api/orders` - Crear una nueva orden (Valida existencia de usuario y productos).
* **PATCH** `/api/orders/{id}/status` - Actualizar el estado de una orden.
* **DELETE** `/api/orders/{id}` - Eliminar una orden por ID.
* **GET** `/api/orders/user/{user_id}` - Obtener todas las órdenes de un usuario.

## Ejemplo de Request (POST `/api/orders`)

```json
{
  "user_id": 1,
  "estado": "pendiente",
  "productos": [
    {
      "product_id": "1",
      "nombre": "Laptop",
      "precio_unitario": 1200,
      "cantidad": 1
    }
  ],
  "direccion_envio": {
    "direccion": "Calle Falsa 123",
    "ciudad": "Ciudad de México",
    "pais": "México",
    "codigo_postal": "01000"
  }
}
```

## Cómo correr el proyecto localmente

1. Clona el repositorio y ve a la carpeta del microservicio:
   `cd services/orders-service`

2. Instala las dependencias:
   `npm install`

3. Crea un archivo `.env` basado en `.env.example`:
   `cp .env.example .env` (en Windows: `copy .env.example .env`)

4. Levanta la base de datos de MongoDB utilizando Docker:
   `docker-compose up -d`

5. Inicia el servidor en modo desarrollo:
   `npm run dev` (o `npm start` para producción).

6. Visita `http://localhost:3003/api-docs` para ver la documentación interactiva en Swagger.
