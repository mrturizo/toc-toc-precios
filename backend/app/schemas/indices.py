from datetime import date

from pydantic import BaseModel


class DailyIndexPoint(BaseModel):
    date: date
    index_value: float



