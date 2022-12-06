from flask import abort, request

from app.db.aggregation import get_ports, get_averages
from app.helpers.request import get_date_or_400
from app.lib.port import is_port


def get():
    date_from = get_date_or_400('date_from')
    date_to = get_date_or_400('date_to')

    if date_from > date_to:
        abort(400, 'incorrect time period')

    origin = request.args.get('origin')
    if not origin:
        abort(400, 'origin is required')

    destination = request.args.get('destination')
    if not destination:
        abort(400, 'destination is required')

    if not is_port(origin):
        origin = get_ports(origin)
        if len(origin) <= 0:
            abort(404, f'region {origin} not found')

    if not is_port(destination):
        destination = get_ports(destination)
        if len(destination) <= 0:
            abort(404, f'region {destination} not found')

    return get_averages(origin, destination, date_from, date_to)


