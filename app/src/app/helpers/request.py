from datetime import datetime

from flask import request, abort

from ..helpers import config


def get_date_or_400(param: str) -> datetime:
    raw = request.args.get(param)
    if not raw:
        abort(400, f'{param} is required')

    try:
        parsed = datetime.strptime(raw, config.get_date_format())
    except ValueError:
        abort(400, f'{param} should have format {config.get_date_format()}')

    return parsed