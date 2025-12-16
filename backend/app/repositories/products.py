from datetime import date
from typing import Iterable, List, Optional

from sqlalchemy import Select, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import City, HistoricalPrice, Product, StoreChain
from ..schemas import (
    HistoricalPricePoint,
    PriceByChain,
    ProductDetail,
    ProductSummary,
)


async def list_products_with_prices(
    db: AsyncSession,
    price_date: date,
    city_id: Optional[int] = None,
    chain_id: Optional[int] = None,
    search: Optional[str] = None,
) -> List[ProductSummary]:
    conditions: list = [HistoricalPrice.price_date == price_date]

    if city_id is not None:
        conditions.append(HistoricalPrice.city_id == city_id)
    if chain_id is not None:
        conditions.append(HistoricalPrice.store_chain_id == chain_id)

    stmt: Select = (
        select(
            Product.id,
            Product.code,
            Product.name,
            Product.unit,
            StoreChain.id.label("chain_id"),
            StoreChain.name.label("chain_name"),
            HistoricalPrice.price,
        )
        .join(HistoricalPrice, HistoricalPrice.product_id == Product.id)
        .join(StoreChain, StoreChain.id == HistoricalPrice.store_chain_id)
        .where(and_(*conditions))
    )

    if search:
        ilike = f"%{search.lower()}%"
        stmt = stmt.where(
            func.lower(Product.name).like(ilike) | func.lower(Product.code).like(ilike)
        )

    result = await db.execute(stmt)

    rows = result.all()

    products_map: dict[int, ProductSummary] = {}
    for row in rows:
        if row.id not in products_map:
            products_map[row.id] = ProductSummary(
                id=row.id,
                code=row.code,
                name=row.name,
                unit=row.unit,
                prices=[],
            )
        products_map[row.id].prices.append(
            PriceByChain(
                chain_id=row.chain_id,
                chain_name=row.chain_name,
                price=row.price,
            )
        )

    return list(products_map.values())


async def get_product_detail(
    db: AsyncSession,
    product_id: int,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    city_id: Optional[int] = None,
    chain_id: Optional[int] = None,
) -> Optional[ProductDetail]:
    product_stmt = select(Product).where(Product.id == product_id)
    product_result = await db.execute(product_stmt)
    product = product_result.scalar_one_or_none()
    if product is None:
        return None

    conditions: list = [HistoricalPrice.product_id == product_id]

    if from_date is not None:
        conditions.append(HistoricalPrice.price_date >= from_date)
    if to_date is not None:
        conditions.append(HistoricalPrice.price_date <= to_date)
    if city_id is not None:
        conditions.append(HistoricalPrice.city_id == city_id)
    if chain_id is not None:
        conditions.append(HistoricalPrice.store_chain_id == chain_id)

    stmt: Select = (
        select(
            HistoricalPrice.price_date,
            StoreChain.id.label("chain_id"),
            StoreChain.name.label("chain_name"),
            HistoricalPrice.price,
        )
        .join(StoreChain, StoreChain.id == HistoricalPrice.store_chain_id)
        .where(and_(*conditions))
        .order_by(HistoricalPrice.price_date)
    )

    result = await db.execute(stmt)
    rows: Iterable = result.all()

    history: List[HistoricalPricePoint] = [
        HistoricalPricePoint(
            date=row.price_date,
            chain_id=row.chain_id,
            chain_name=row.chain_name,
            price=row.price,
        )
        for row in rows
    ]

    return ProductDetail(
        id=product.id,
        code=product.code,
        name=product.name,
        unit=product.unit,
        category=product.category,
        history=history,
    )



