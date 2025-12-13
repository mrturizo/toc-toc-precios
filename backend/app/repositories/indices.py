from datetime import date
from typing import List, Optional

from sqlalchemy import Select, and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import HistoricalPrice
from ..schemas import DailyIndexPoint


async def get_daily_index(
    db: AsyncSession,
    from_date: date,
    to_date: date,
    city_id: Optional[int] = None,
    chain_id: Optional[int] = None,
) -> List[DailyIndexPoint]:
    conditions = [
        HistoricalPrice.price_date >= from_date,
        HistoricalPrice.price_date <= to_date,
    ]
    if city_id is not None:
        conditions.append(HistoricalPrice.city_id == city_id)
    if chain_id is not None:
        conditions.append(HistoricalPrice.store_chain_id == chain_id)

    stmt: Select = (
        select(
            HistoricalPrice.price_date.label("date"),
            func.avg(HistoricalPrice.price).label("index_value"),
        )
        .where(and_(*conditions))
        .group_by(HistoricalPrice.price_date)
        .order_by(HistoricalPrice.price_date)
    )

    result = await db.execute(stmt)
    rows = result.all()

    return [
        DailyIndexPoint(date=row.date, index_value=row.index_value) for row in rows
    ]


