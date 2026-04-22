# Products Microservice - E-commerce

Este es el microservicio encargado de la gestión de productos y categorías para el sistema de E-commerce. Está construido utilizando **Java 21**, **Spring Boot**, y **AWS S3** para el almacenamiento de imágenes.

## Tecnologías Utilizadas
- **Java 21+**
- **Spring Boot**: Framework principal para el backend.
- **AWS SDK v2**: Integración con Amazon S3 para almacenamiento de archivos.
- **Spring Data JPA & Hibernate**: ORM para la interacción con la base de datos MySQL.
- **Lombok**: Reducción de código repetitivo.
- **Spring Security & JWT**: Autenticación para endpoints protegidos.
- **SpringDoc OpenAPI (Swagger)**: Documentación de la API.

---

## Modelos de Datos

### Producto (Product)
- `id`: Identificador único (Long)
- `nombre`: Nombre del producto (String)
- `descripcion`: Detalles del producto (String)
- `precio`: Precio actual (BigDecimal)
- `stock`: Cantidad disponible (Integer)
- `activo`: Estado disponible (Booleano)
- `categoriaId`: ID de la categoría (Long)
- `imageUrl`: URL pública de la imagen en S3 (String)

---

## Endpoints de la API

### 📦 Productos (`/api/products`)

#### 📷 Subir Imagen de Producto
- **Método:** `POST`
- **Ruta:** `/api/products/{id}/upload-image`
- **Descripción:** Sube una imagen a AWS S3 y actualiza la URL del producto.
- **Requisito:** Token JWT (`Authorization: Bearer <token>`)
- **Body (Multipart):** `file` (Archivo de imagen)

---

## Instalación y Ejecución

1. **Configuración de variables de entorno (.env)**
   ```env
   DB_HOST=127.0.0.1
   DB_NAME=products_db
   DB_USERNAME=app_user
   DB_PASSWORD=app_pass
   JWT_SECRET=super_secret_jwt_key_...
   
   # AWS S3
   AWS_ACCESS_KEY_ID=TU_ACCESS_KEY
   AWS_SECRET_ACCESS_KEY=TU_SECRET_KEY
   AWS_SESSION_TOKEN=TU_TOKEN (Si usas llaves ASIA)
   AWS_REGION=us-east-1
   S3_BUCKET=nombre-de-tu-bucket
   ```

2. **Ejecutar el servidor**
   ```bash
   mvn spring-boot:run
   ```

## Pruebas
Puedes importar la colección de Postman ubicada en: `products_collection.json`
