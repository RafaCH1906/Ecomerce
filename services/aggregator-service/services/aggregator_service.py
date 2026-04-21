from clients.user_client import UserClient
from clients.product_client import ProductClient
from clients.order_client import OrderClient
from fastapi import HTTPException

class AggregatorService:
    def __init__(self):
        self.user_client = UserClient()
        self.product_client = ProductClient()
        self.order_client = OrderClient()

    async def get_full_user_profile(self, user_id: int, token: str):
        # 1. Obtener datos básicos del usuario
        user_data = await self.user_client.get_user_profile(user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # 2. Obtener órdenes del usuario
        orders = await self.order_client.get_user_orders(user_id, token)

        # 3. Enriquecer cada orden con detalles de productos
        full_orders = []
        for order in orders:
            enriched_products = []
            for item in order.get("productos", []):
                product_detail = await self.product_client.get_product_detail(item["product_id"])
                enriched_products.append({
                    "product_id": item["product_id"],
                    "cantidad": item["cantidad"],
                    "precio_unitario_en_orden": item["precio_unitario"],
                    "subtotal": item["subtotal"],
                    "detalle_producto": product_detail
                })
            
            order["productos"] = enriched_products
            full_orders.append(order)

        # 4. Consolidar respuesta
        return {
            "usuario": user_data,
            "resumen_actividad": {
                "total_ordenes": len(orders),
                "ordenes": full_orders
            }
        }

    async def get_order_details_full(self, order_id: str, token: str):
        # 1. Obtener orden
        order = await self.order_client.get_order_by_id(order_id, token)
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")

        # 2. Enriquecer productos
        enriched_products = []
        for item in order.get("productos", []):
            product_detail = await self.product_client.get_product_detail(item["product_id"])
            enriched_products.append({
                **item,
                "detalle_completo": product_detail
            })
        
        order["productos"] = enriched_products
        
        # 3. Obtener datos del usuario de la orden
        user_data = await self.user_client.get_user_profile(order["user_id"])
        order["datos_usuario"] = user_data

        return order
