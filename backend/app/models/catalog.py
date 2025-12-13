from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    country: Mapped[str] = mapped_column(String(100), default="CO")

    locals: Mapped[list["StoreChain"]] = relationship(back_populates="city")
    prices: Mapped[list["HistoricalPrice"]] = relationship(back_populates="city")


class StoreChain(Base):
    """Representa una cadena o cliente (Olimpica, D1, etc.)."""

    __tablename__ = "store_chains"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)

    city_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("cities.id"),
        nullable=True,
    )

    city: Mapped[City | None] = relationship(back_populates="locals")
    prices: Mapped[list["HistoricalPrice"]] = relationship(back_populates="store_chain")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    unit: Mapped[str] = mapped_column(String(50), default="kg")
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)

    prices: Mapped[list["HistoricalPrice"]] = relationship(back_populates="product")


class HistoricalPrice(Base):
    __tablename__ = "historical_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        index=True,
    )
    store_chain_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("store_chains.id"),
        index=True,
    )
    city_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cities.id"),
        index=True,
    )
    price_date: Mapped[date] = mapped_column(Date, index=True)
    price: Mapped[float] = mapped_column(Float)

    product: Mapped[Product] = relationship(back_populates="prices")
    store_chain: Mapped[StoreChain] = relationship(back_populates="prices")
    city: Mapped[City] = relationship(back_populates="prices")


