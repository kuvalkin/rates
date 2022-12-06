from dataclasses import dataclass
from datetime import datetime


@dataclass
class Average:
    day: datetime
    average_price: int | None
