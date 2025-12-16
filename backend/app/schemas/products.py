from datetime import date
from typing import List

from pydantic import BaseModel


class PriceByChain(BaseModel):
    chain_id: int
    chain_name: str
    price: float


class ProductSummary(BaseModel):
    id: int
    code: str
    name: str
    unit: str
    prices: List[PriceByChain]

    class Config:
        from_attributes = True


class HistoricalPricePoint(BaseModel):
    date: date
    chain_id: int
    chain_name: str
    price: float


class ProductDetail(BaseModel):
    id: int
    code: str
    name: str
    unit: str
    category: str | None
    history: List[HistoricalPricePoint]

    class Config:
        from_attributes = True



