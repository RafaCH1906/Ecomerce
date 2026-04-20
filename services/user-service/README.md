# Users Microservice - E-commerce

Este es el microservicio encargado de la gestión de usuarios y sus direcciones asociadas para el sistema de E-commerce. Está construido utilizando **Python 3**, **FastAPI**, y **SQLAlchemy** con conexión a **PostgreSQL**.

## Tecnologías Utilizadas
- **Python 3.12+**
- **FastAPI**: Framework web de alto rendimiento.
- **SQLAlchemy**: ORM para la interacción con la base de datos.
- **Pydantic**: Validación de datos y gestión de esquemas.
- **Uvicorn**: Servidor ASGI.
- **PostgreSQL**: Base de datos relacional.

---

## Modelos de Datos

### Usuario (User)
Representa un cliente o usuario en el sistema.
- `id`: Identificador único (Entero)
- `nombre`: Nombre completo (String)
- `email`: Correo electrónico (String, Único)
- `password`: Contraseña (String - debe ser hasheada en producción)
- `telefono`: Número de teléfono (String, Opcional)
- `activo`: Estado de la cuenta (Booleano, por defecto `true`)
- `created_at`: Fecha y hora de creación (Datetime)

### Dirección (Address)
Representa una dirección física asociada a un usuario.
- `id`: Identificador único (Entero)
- `user_id`: ID del usuario propietario (Entero, Clave foránea)
- `direccion`: Calle, número, etc. (String)
- `ciudad`: Ciudad (String)
- `pais`: País (String)
- `codigo_postal`: Código postal (String)
- `principal`: Indica si es la dirección por defecto (Booleano, por defecto `false`)

---

## Endpoints de la API

### 👤 Usuarios (`/api/users`)

#### 1. Obtener todos los usuarios
- **Método:** `GET`
- **Ruta:** `/api/users`
- **Descripción:** Retorna una lista paginada de todos los usuarios registrados.
- **Parámetros de consulta:** `skip` (int, default=0), `limit` (int, default=100)

#### 2. Crear un usuario
- **Método:** `POST`
- **Ruta:** `/api/users`
- **Descripción:** Registra un nuevo usuario.
- **Body (JSON):**
  ```json
  {
    "nombre": "Juan Pérez",
    "email": "juan@example.com",
    "telefono": "+1234567890",
    "activo": true,
    "password": "mi_password_seguro"
  }
  ```

#### 3. Obtener usuario por ID
- **Método:** `GET`
- **Ruta:** `/api/users/{user_id}`
- **Descripción:** Retorna los detalles de un usuario específico.

#### 4. Actualizar un usuario
- **Método:** `PUT`
- **Ruta:** `/api/users/{user_id}`
- **Descripción:** Actualiza total o parcialmente los datos de un usuario.
- **Body (JSON):** (Todos los campos son opcionales)
  ```json
  {
    "nombre": "Juan Pérez Actualizado",
    "telefono": "+0987654321"
  }
  ```

#### 5. Eliminar un usuario
- **Método:** `DELETE`
- **Ruta:** `/api/users/{user_id}`
- **Descripción:** Elimina un usuario de la base de datos (y en cascada sus direcciones asociadas).

---

### 🏠 Direcciones

#### 1. Obtener direcciones de un usuario
- **Método:** `GET`
- **Ruta:** `/api/users/{user_id}/addresses`
- **Descripción:** Retorna todas las direcciones asociadas a un usuario específico.

#### 2. Crear dirección para un usuario
- **Método:** `POST`
- **Ruta:** `/api/users/{user_id}/addresses`
- **Descripción:** Añade una nueva dirección.
- **Body (JSON):**
  ```json
  {
    "direccion": "Calle Falsa 123",
    "ciudad": "Springfield",
    "pais": "EEUU",
    "codigo_postal": "12345",
    "principal": true
  }
  ```

#### 3. Actualizar una dirección
- **Método:** `PUT`
- **Ruta:** `/api/addresses/{address_id}`
- **Descripción:** Modifica los datos de una dirección.
- **Body (JSON):** (Todos los campos son opcionales)
  ```json
  {
    "ciudad": "Nueva Ciudad"
  }
  ```

#### 4. Eliminar una dirección
- **Método:** `DELETE`
- **Ruta:** `/api/addresses/{address_id}`
- **Descripción:** Elimina permanentemente una dirección por su ID.

---

## Instalación y Ejecución

1. **Ejecutar la Base de Datos (PostgreSQL)**
   La forma más sencilla de levantar la base de datos es usando Docker:
   ```bash
   docker run --name ecommerce_db -e POSTGRES_USER=usuario -e POSTGRES_PASSWORD=password -e POSTGRES_DB=ecommerce_bd -p 5432:5432 -d postgres
   ```
   *(Asegúrate de cambiar `usuario`, `password` y `ecommerce_bd` por los valores correctos o los configurados en tus variables de entorno).*

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   venv\bin\activate     # En Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Base de Datos**
   - Asegúrate de tener PostgreSQL ejecutándose.
   - Configura la variable de entorno `DATABASE_URL` o edita `database.py` si es estrictamente necesario, usando el formato:
     `postgresql://usuario:password@localhost/ecommerce_bd`

5. **Ejecutar el servidor**
   ```bash
   uvicorn main:app --reload
   ```

6. **Documentación Swagger**
   - Una vez levantado el servidor, la documentación automática (Swagger UI) estará disponible en: `http://localhost:8000/docs`
