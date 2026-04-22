# Analytics Service (AWS Athena)

Microservicio para generación de reportes de negocio consultando datos en S3 vía AWS Athena.

## Requisitos Previos
* **Python 3.12.3**

## Endpoints
* **GET `/api/analytics/total-sales`**: Suma total de ingresos.
* **GET `/api/analytics/sales-by-date`**: Histórico de ventas por día.
* **GET `/api/analytics/top-products`**: Ranking de productos más vendidos.
* **GET `/api/analytics/top-users`**: Clientes con mayor volumen de compra.

## Cómo correr localmente (Windows)

1. **Activar entorno**:
   ```powershell
   .\venv\Scripts\activate
   ```
2. **Instalar dependencias**:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Ejecutar**:
   ```powershell
   .\venv\Scripts\python.exe main.py
   ```

## Configuración (.env)
Asegúrate de editar el archivo `.env` con tus datos de AWS:
```env
AWS_ACCESS_KEY_ID=TU_LLAVE
AWS_SECRET_ACCESS_KEY=TU_SECRETO
AWS_REGION=us-east-1
ATHENA_DATABASE=ecommerce_analytics
ATHENA_OUTPUT_LOCATION=s3://tu-bucket-resultados/
```
