from aws.athena_client import AthenaClient

class AnalyticsService:
    def __init__(self):
        self.athena = AthenaClient()

    async def get_total_sales(self):
        query = "SELECT SUM(total) as total_ventas FROM orders_table WHERE estado = 'completada'"
        return await self.athena.execute_query(query)

    async def get_sales_by_date(self):
        query = """
            SELECT date(created_at) as fecha, SUM(total) as ventas_diarias 
            FROM orders_table 
            GROUP BY date(created_at) 
            ORDER BY fecha DESC
        """
        return await self.athena.execute_query(query)

    async def get_top_products(self):
        query = """
            SELECT p.product_id, p.nombre, SUM(p.cantidad) as total_vendido
            FROM orders_table CROSS JOIN UNNEST(productos) as t(p)
            GROUP BY p.product_id, p.nombre
            ORDER BY total_vendido DESC
            LIMIT 5
        """
        return await self.athena.execute_query(query)

    async def get_top_users(self):
        query = """
            SELECT user_id, COUNT(*) as numero_compras, SUM(total) as total_gastado
            FROM orders_table
            GROUP BY user_id
            ORDER BY total_gastado DESC
            LIMIT 5
        """
        return await self.athena.execute_query(query)
