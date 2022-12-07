from dataclasses import dataclass, field
from datetime import datetime
from functools import partial

from dataclasses_json import config, dataclass_json

from ..helpers.config import get_date_format


@dataclass_json
@dataclass
class Average:
    day: datetime = field(
        metadata=config(
            encoder=partial(datetime.strftime, format=get_date_format())
        )
    )
    average_price: int | None
