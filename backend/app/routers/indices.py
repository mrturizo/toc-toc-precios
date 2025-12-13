from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models import User
from ..repositories.indices import get_daily_index
from ..routers.auth import get_current_user
from ..schemas import DailyIndexPoint

router = APIRouter(prefix="/indices", tags=["indices"])


@router.get("/daily", response_model=List[DailyIndexPoint])
async def daily_index(
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    city_id: Optional[int] = None,
    chain_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[DailyIndexPoint]:
    _ = current_user
    return await get_daily_index(
        db=db,
        from_date=from_date,
        to_date=to_date,
        city_id=city_id,
        chain_id=chain_id,
    )


