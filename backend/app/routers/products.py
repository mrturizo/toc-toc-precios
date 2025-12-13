from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..repositories.products import get_product_detail, list_products_with_prices
from ..routers.auth import get_current_user
from ..schemas import ProductDetail, ProductSummary
from ..models import User

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductSummary])
async def list_products(
    date_value: date = Query(..., alias="date"),
    city_id: Optional[int] = None,
    chain_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ProductSummary]:
    _ = current_user  # solo para marcar dependencia de seguridad
    return await list_products_with_prices(
        db=db,
        price_date=date_value,
        city_id=city_id,
        chain_id=chain_id,
        search=search,
    )


@router.get("/{product_id}", response_model=ProductDetail)
async def product_detail(
    product_id: int,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    city_id: Optional[int] = None,
    chain_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProductDetail:
    _ = current_user
    detail = await get_product_detail(
        db=db,
        product_id=product_id,
        from_date=from_date,
        to_date=to_date,
        city_id=city_id,
        chain_id=chain_id,
    )
    if detail is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return detail


