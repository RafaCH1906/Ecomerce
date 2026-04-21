# Products Microservice - E-commerce

Este es el microservicio encargado de la gestión de productos y categorías para el sistema de E-commerce. Está construido utilizando **Java 21**, **Spring Boot**, y **Spring Data JPA** con conexión a **MySQL**.

## Tecnologías Utilizadas
- **Java 21+**
- **Spring Boot**: Framework principal para el backend.
- **Spring Data JPA & Hibernate**: ORM para la interacción con la base de datos MySQL.
- **Lombok**: Reducción de código repetitivo (getters, setters, constructores, etc.).
- **Spring Security & JWT**: Autenticación para endpoints protegidos.
- **SpringDoc OpenAPI (Swagger)**: Para documentación automática de la API.
- **MySQL**: Base de datos relacional.

---

## Modelos de Datos

### Categoría (Category)
Representa un rubro o grupo principal para organizar los productos.
- `id`: Identificador único (Long)
- `nombre`: Nombre de la categoría (String, Obligatorio)
- `descripcion`: Descripción detallada (String, Opcional)

### Producto (Product)
Representa el ítem de venta dentro del catálogo.
- `id`: Identificador único (Long)
- `nombre`: Nombre del producto (String, Obligatorio)
- `descripcion`: Detalles del producto (String, Opcional)
- `precio`: Precio actual (BigDecimal, > 0)
- `stock`: Cantidad disponible (Integer, >= 0)
- `activo`: Estado disponible para la compra (Booleano)
- `categoriaId`: ID de la categoría a la que pertenece (Long, Clave foránea)

---

## Endpoints de la API

### 🏷️ Categorías (`/api/categories`)

#### 1. Obtener todas las categorías
- **Método:** `GET`
- **Ruta:** `/api/categories`
- **Descripción:** Retorna una lista de todas las categorías. (Público)

#### 2. Crear una categoría
- **Método:** `POST`
- **Ruta:** `/api/categories`
- **Descripción:** Crea una nueva categoría.
- **Requisito:** Token JWT (`Authorization: Bearer <token>`)
- **Body (JSON):**
  ```json
  {
    "nombre": "Electrónica",
    "descripcion": "Todos los dispositivos y componentes electrónicos"
  }
  ```

#### 3. Obtener categoría por ID
- **Método:** `GET`
- **Ruta:** `/api/categories/{id}`
- **Descripción:** Retorna los detalles de una categoría específica. (Público)

#### 4. Actualizar una categoría
- **Método:** `PUT`
- **Ruta:** `/api/categories/{id}`
- **Descripción:** Modifica los datos de una categoría.
- **Requisito:** Token JWT
- **Body (JSON):** (Campos obligatorios deben incluirse)
  ```json
  {
    "nombre": "Electrónica y Hogar",
    "descripcion": "Dispositivos para el hogar inteligente"
  }
  ```

#### 5. Eliminar una categoría
- **Método:** `DELETE`
- **Ruta:** `/api/categories/{id}`
- **Descripción:** Elimina una categoría del sistema.
- **Requisito:** Token JWT

---

### 📦 Productos (`/api/products`)

#### 1. Obtener todos los productos (Paginado)
- **Método:** `GET`
- **Ruta:** `/api/products`
- **Descripción:** Retorna una lista paginada de todos los productos en el catálogo. (Público)
- **Parámetros de consulta:** `page` (int, default=0), `size` (int, default=10)

#### 2. Obtener productos por categoría (Paginado)
- **Método:** `GET`
- **Ruta:** `/api/products/categoria/{categoriaId}`
- **Descripción:** Retorna los productos pertenecientes a una categoría. (Público)
- **Parámetros de consulta:** `page`, `size`

#### 3. Crear un producto
- **Método:** `POST`
- **Ruta:** `/api/products`
- **Descripción:** Añade un nuevo producto al catálogo.
- **Requisito:** Token JWT
- **Body (JSON):**
  ```json
  {
    "nombre": "Laptop Gamer V2",
    "descripcion": "Laptop de alto rendimiento 16GB RAM",
    "precio": 1250.99,
    "stock": 15,
    "activo": true,
    "categoriaId": 1
  }
  ```

#### 4. Obtener producto por ID
- **Método:** `GET`
- **Ruta:** `/api/products/{id}`
- **Descripción:** Retorna los detalles de un producto específico. (Público)

#### 5. Actualizar un producto
- **Método:** `PUT`
- **Ruta:** `/api/products/{id}`
- **Descripción:** Actualiza los detalles de un producto existente.
- **Requisito:** Token JWT

#### 6. Eliminar un producto
- **Método:** `DELETE`
- **Ruta:** `/api/products/{id}`
- **Descripción:** Inactiva o elimina un producto de la base de datos de manera lógica (soft delete).
- **Requisito:** Token JWT

---

## Instalación y Ejecución

1. **Ejecutar la Base de Datos (MySQL)**
   Asegúrate de que tus contenedores de base de datos están activos. Usando `docker-compose.yml`:
   ```bash
   docker compose up -d
   ```

2. **Configuración de variables de entorno**
   Crea o verifica tu archivo `.env` en la raíz del proyecto (`products-service`):
   ```env
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=products_db
   DB_USERNAME=root
   DB_PASSWORD=secret
   JWT_SECRET=supersecretjwtkeythatisverylongandsecure
   JWT_EXPIRATION=86400000
   ```

3. **Ejecutar el servidor de Spring Boot**
   En tu terminal Windows (PowerShell/CMD) usa Maven para correr el proyecto:
   ```bash
   mvn spring-boot:run
   ```

4. **Documentación Swagger**
   - Una vez levantado el servidor (por defecto en el puerto `8080`), la documentación de OpenAPI (Swagger UI) estará disponible en:
     [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)
