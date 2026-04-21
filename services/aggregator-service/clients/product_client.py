import httpx
import os
from fastapi import HTTPException

class ProductClient:
    def __init__(self):
        self.base_url = os.getenv("PRODUCTS_SERVICE_URL")

    async def get_product_detail(self, product_id: int):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/{product_id}")
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(status_code=502, detail=f"Error conectando con Product Service: {str(e)}")
