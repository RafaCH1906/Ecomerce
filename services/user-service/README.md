# Users Microservice - E-commerce

Este es el microservicio encargado de la gestión de usuarios y sus direcciones asociadas para el sistema de E-commerce. Está construido utilizando **Python 3**, **FastAPI**, y **SQLAlchemy** con conexión a **PostgreSQL**.

## Tecnologías Utilizadas

* **Python 3.12.3+** (Instalador oficial de python.org recomendado)
* **FastAPI**: Framework web de alto rendimiento.
* **SQLAlchemy**: ORM para la interacción con la base de datos.
* **Pydantic**: Validación de datos y gestión de esquemas.
* **Uvicorn**: Servidor ASGI.
* **PostgreSQL**: Base de datos relacional.

---

## ⚠️ Requisito Crítico (Windows)

Para evitar errores de compilación y conflictos de conexión:
1. Usa el **instalador oficial de Python 3.12.3** (64-bit) de [python.org](https://www.python.org/downloads/windows/). Evita versiones de MSYS2 o Microsoft Store.
2. Si tienes PostgreSQL instalado localmente en Windows, **asegúrate de detener el servicio** antes de levantar el contenedor de Docker para liberar el puerto **5432**.

---

## Modelos de Datos

### Usuario (User)

Representa un cliente o usuario en el sistema.

* `id`: Identificador único (Entero)
* `nombre`: Nombre completo (String)
* `email`: Correo electrónico (String, Único)
* `password`: Contraseña (String - debe ser hasheada en producción)
* `telefono`: Número de teléfono (String, Opcional)
* `activo`: Estado de la cuenta (Booleano, por defecto `true`)
* `created_at`: Fecha y hora de creación (Datetime)

### Dirección (Address)

Representa una dirección física asociada a un usuario.

* `id`: Identificador único (Entero)
* `user_id`: ID del usuario propietario (Entero, Clave foránea)
* `direccion`: Calle, número, etc. (String)
* `ciudad`: Ciudad (String)
* `pais`: País (String)
* `codigo_postal`: Código postal (String)
* `principal`: Indica si es la dirección por defecto (Booleano, por defecto `false`)

---

## Endpoints de la API

### 👤 Usuarios (`/api/users`)

#### 1. Obtener todos los usuarios

* **Método:** `GET`
* **Ruta:** `/api/users`
* **Descripción:** Retorna una lista paginada de todos los usuarios registrados.
* **Parámetros:** `skip` (int, default=0), `limit` (int, default=100)

#### 2. Crear un usuario

* **Método:** `POST`
* **Ruta:** `/api/users`
* **Body:**

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

* **Método:** `GET`
* **Ruta:** `/api/users/{user_id}`

#### 4. Actualizar un usuario

* **Método:** `PUT`
* **Ruta:** `/api/users/{user_id}`

#### 5. Eliminar un usuario

* **Método:** `DELETE`
* **Ruta:** `/api/users/{user_id}`

---

### 🏠 Direcciones

#### 1. Obtener direcciones de un usuario

* **Método:** `GET`
* **Ruta:** `/api/users/{user_id}/addresses`

#### 2. Crear dirección

* **Método:** `POST`
* **Ruta:** `/api/users/{user_id}/addresses`

#### 3. Actualizar dirección

* **Método:** `PUT`
* **Ruta:** `/api/addresses/{address_id}`

#### 4. Eliminar dirección

* **Método:** `DELETE`
* **Ruta:** `/api/addresses/{address_id}`

---

## Instalación y Ejecución

### 1. Levantar PostgreSQL con Docker Compose

Es la opción recomendada para evitar conflictos de puertos en Windows:

```bash
docker-compose up -d
```
*Nota: Se usa el puerto **5433** para evitar conflictos con servicios nativos de Windows.*

---

### 2. Crear entorno virtual

```bash
python -m venv venv
```

Activar entorno:

* Windows:

```bash
venv\Scripts\activate
```

* Linux/Mac:

```bash
source venv/bin/activate
```

---

### 3. Instalar dependencias

Si tienes `requirements.txt`:

```bash
pip install -r requirements.txt
```

Si no lo tienes, instala manualmente:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

---

### 4. Configurar Base de Datos

Configura la variable en tu archivo `.env`:

```bash
DATABASE_URL=postgresql://usuario:password@localhost:5433/ecommerce_bd
```

---

### 5. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

⚠️ En Windows, si `uvicorn` no es reconocido:

```bash
python -m uvicorn main:app --reload
```

---

### 6. Documentación Swagger

Disponible en:

```
http://localhost:8000/docs
```

---

## Notas

* Asegúrate de que PostgreSQL esté corriendo antes de iniciar el servicio.
* No usar contraseñas en texto plano en producción.
* Considera usar Docker para todo el microservicio en entornos reales.
