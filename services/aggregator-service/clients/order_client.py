import httpx
import os
from fastapi import HTTPException

class OrderClient:
    def __init__(self):
        self.base_url = os.getenv("ORDERS_SERVICE_URL")

    async def get_user_orders(self, user_id: int, token: str):
        headers = {"Authorization": token} # Pasamos el token recibido
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/user/{user_id}", headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"Error conectando con Order Service: {str(e)}")

    async def get_order_by_id(self, order_id: str, token: str):
        headers = {"Authorization": token}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/{order_id}", headers=headers)
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"Error conectando con Order Service: {str(e)}")
