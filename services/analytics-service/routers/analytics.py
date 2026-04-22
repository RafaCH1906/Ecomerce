from fastapi import APIRouter, Depends, HTTPException, Header
from services.analytics_service import AnalyticsService
from typing import Optional

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])
analytics_service = AnalyticsService()

@router.get("/total-sales")
async def total_sales():
    """Retorna la suma total de todas las ventas completadas."""
    return await analytics_service.get_total_sales()

@router.get("/sales-by-date")
async def sales_by_date():
    """Retorna las ventas agrupadas por fecha."""
    return await analytics_service.get_sales_by_date()

@router.get("/top-products")
async def top_products():
    """Retorna los 5 productos más vendidos."""
    return await analytics_service.get_top_products()

@router.get("/top-users")
async def top_users():
    """Retorna los 5 usuarios que más han gastado."""
    return await analytics_service.get_top_users()
