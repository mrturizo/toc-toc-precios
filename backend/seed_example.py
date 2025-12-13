import asyncio
from datetime import date, timedelta

from app.db import Base, engine, AsyncSessionLocal
from app.models import City, StoreChain, Product, HistoricalPrice


async def seed() -> None:
  """Inserta datos de ejemplo para probar el MVP."""
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  async with AsyncSessionLocal() as session:
    # Ciudad
    bogota = City(name="Bogotá", country="CO")
    session.add(bogota)
    await session.flush()

    # Cadenas
    olimpica = StoreChain(name="Olimpica", city=bogota)
    d1 = StoreChain(name="D1", city=bogota)
    sipsa = StoreChain(name="SIPSA", city=bogota)
    session.add_all([olimpica, d1, sipsa])
    await session.flush()

    # Productos
    tomate = Product(code="TOM-001", name="Tomate Chonto x Kg", unit="kg")
    banano = Product(code="BAN-001", name="Banano Maduro x Kg", unit="kg")
    session.add_all([tomate, banano])
    await session.flush()

    # Precios para últimos 5 días
    today = date.today()
    rows: list[HistoricalPrice] = []
    for i in range(5):
      day = today - timedelta(days=i)
      rows.extend(
        [
          HistoricalPrice(
            product_id=tomate.id,
            store_chain_id=olimpica.id,
            city_id=bogota.id,
            price_date=day,
            price=3800 + i * 50,
          ),
          HistoricalPrice(
            product_id=tomate.id,
            store_chain_id=d1.id,
            city_id=bogota.id,
            price_date=day,
            price=3700 + i * 40,
          ),
          HistoricalPrice(
            product_id=tomate.id,
            store_chain_id=sipsa.id,
            city_id=bogota.id,
            price_date=day,
            price=3900 + i * 30,
          ),
          HistoricalPrice(
            product_id=banano.id,
            store_chain_id=olimpica.id,
            city_id=bogota.id,
            price_date=day,
            price=2500 + i * 20,
          ),
          HistoricalPrice(
            product_id=banano.id,
            store_chain_id=d1.id,
            city_id=bogota.id,
            price_date=day,
            price=2400 + i * 25,
          ),
          HistoricalPrice(
            product_id=banano.id,
            store_chain_id=sipsa.id,
            city_id=bogota.id,
            price_date=day,
            price=2600 + i * 15,
          ),
        ]
      )

    session.add_all(rows)
    await session.commit()

  print("✅ Datos de ejemplo insertados correctamente.")


if __name__ == "__main__":
  asyncio.run(seed())


