# Aggregator Service

Microservicio encargado de orquestar y consolidar la información de los servicios de Usuarios, Productos y Órdenes.

## Requisitos Previos
* **Python 3.12+** (Importante para compatibilidad de librerías)

## Endpoints

1.  **GET `/api/aggregator/user/{id}/full-profile`**
    *   Devuelve los datos del usuario + su historial de órdenes detallado (con info de productos).
    *   Requiere Header: `Authorization: Bearer <token>`
2.  **GET `/api/aggregator/orders/{id}/detail`**
    *   Devuelve el detalle completo de una orden enriquecido con los datos del usuario y de cada producto.
    *   Requiere Header: `Authorization: Bearer <token>`

## Cómo correr el proyecto (Instalación limpia)

1.  **Crear entorno virtual**:
    ```powershell
    python -m venv venv
    ```
2.  **Activar entorno**:
    *   Windows: `.\venv\Scripts\activate`
    *   Linux/macOS: `source venv/bin/activate`
3.  **Actualizar PIP (Crucial)**:
    ```powershell
    python -m pip install --upgrade pip
    ```
4.  **Instalar dependencias**:
    ```powershell
    pip install -r requirements.txt
    ```
5.  **Ejecutar**:
    ```powershell
    python main.py
    ```

## Configuración (.env)
Crea un archivo `.env` basado en el secreto compartido del sistema:
```env
USERS_SERVICE_URL=http://localhost:8000/api/users
PRODUCTS_SERVICE_URL=http://localhost:8081/api/products
ORDERS_SERVICE_URL=http://localhost:3003/api/orders
JWT_SECRET=tu_clave_secreta_compartida
```
