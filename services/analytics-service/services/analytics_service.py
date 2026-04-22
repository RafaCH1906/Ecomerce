from aws.athena_client import AthenaClient

class AnalyticsService:
    def __init__(self):
        self.athena = AthenaClient()

    async def get_total_sales(self):
        query = "SELECT SUM(total) as total_ventas FROM orders WHERE estado = 'completado'"
        return await self.athena.execute_query(query)

    async def get_sales_by_date(self):
        query = """
            SELECT SUBSTR(created_at, 1, 10) as fecha, SUM(total) as ventas_diarias 
            FROM orders 
            GROUP BY SUBSTR(created_at, 1, 10) 
            ORDER BY fecha DESC
        """
        return await self.athena.execute_query(query)

    async def get_top_products(self):
        query = """
            SELECT p.nombre, SUM(o.cantidad) as total_vendido
            FROM orders o
            JOIN products p ON o.product_id = p.id
            GROUP BY p.nombre
            ORDER BY total_vendido DESC
            LIMIT 5
        """
        return await self.athena.execute_query(query)

    async def get_top_users(self):
        query = """
            SELECT user_id, COUNT(*) as numero_compras, SUM(total) as total_gastado
            FROM orders
            GROUP BY user_id
            ORDER BY total_gastado DESC
            LIMIT 5
        """
        return await self.athena.execute_query(query)
