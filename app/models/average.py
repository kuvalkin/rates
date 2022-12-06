from dataclasses import dataclass, field
from datetime import datetime
from functools import partial

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class Average:
    day: datetime = field(
        metadata=config(
            # todo format to config
            encoder=partial(datetime.strftime, format='%Y-%m-%d')
        )
    )
    average_price: int | None
