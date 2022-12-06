from datetime import datetime

from flask import request, abort


def get_date_or_400(param: str) -> datetime:
    raw = request.args.get(param)
    if not raw:
        abort(400, f'{param} is required')

    try:
        parsed = datetime.strptime(raw, '%Y-%m-%d')
    except ValueError:
        abort(400, f'{param} should have format YYYY-MM-DD')

    return parsed