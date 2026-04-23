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


### ⚠️ Importante: Usa siempre el Python de Windows

No uses MSYS2, Git Bash ni terminales de MinGW para crear el entorno virtual ni instalar dependencias. Usa **PowerShell** o **CMD** de Windows y asegúrate de que el comando `python` apunte a la instalación oficial de Windows (puedes verificar con `python --version`).

Si tienes problemas con dependencias como `pydantic-core` o `uvicorn`, sigue estos pasos:

1. **Borra la carpeta `venv` si existe:**
    ```powershell
    Remove-Item -Recurse -Force venv
    ```
2. **Cierra todas las terminales MSYS2/Git Bash. Abre una nueva PowerShell.**
3. **Crea el entorno virtual:**
    ```powershell
    python -m venv venv
    ```
4. **Activa el entorno virtual:**
    ```powershell
    .\venv\Scripts\activate
    ```
5. **Actualiza pip y wheel:**
    ```powershell
    python -m pip install --upgrade pip setuptools wheel
    ```
6. **Instala dependencias:**
    ```powershell
    pip install -r requirements.txt
    ```
   Si falla con pydantic, instala una versión compatible:
    ```powershell
    pip install pydantic==2.6.4
    pip install fastapi uvicorn httpx python-dotenv python-multipart PyJWT
    ```
7. **Ejecuta el servicio:**
    ```powershell
    python main.py
    ```

---

## Configuración (.env)
Crea un archivo `.env` basado en el secreto compartido del sistema:
```env
USERS_SERVICE_URL=http://localhost:8000/api/users
PRODUCTS_SERVICE_URL=http://localhost:8081/api/products
ORDERS_SERVICE_URL=http://localhost:3003/api/orders
JWT_SECRET=tu_clave_secreta_compartida
```
