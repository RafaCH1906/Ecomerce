from fastapi import APIRouter, Header, HTTPException, Depends
from services.aggregator_service import AggregatorService
from typing import Optional

router = APIRouter(prefix="/api/aggregator", tags=["Aggregator"])
aggregator_service = AggregatorService()

async def get_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Se requiere el header Authorization: Bearer <token>")
    return authorization

@router.get("/user/{user_id}/full-profile")
async def get_user_full_profile(user_id: int, token: str = Depends(get_token)):
    """
    Obtiene el perfil completo del usuario, incluyendo su historial de órdenes 
    con los detalles de cada producto dentro de las órdenes.
    """
    return await aggregator_service.get_full_user_profile(user_id, token)

@router.get("/orders/{order_id}/detail")
async def get_order_detail(order_id: str, token: str = Depends(get_token)):
    """
    Obtiene el detalle completo de una orden específica, enriqueciendo la 
    información de los productos y del usuario.
    """
    return await aggregator_service.get_order_details_full(order_id, token)
