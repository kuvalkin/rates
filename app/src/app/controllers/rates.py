from flask import abort, request, jsonify

from ..db.aggregation import get_ports, get_averages
from ..helpers.request import get_date_or_400
from ..lib.port import is_port


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
        origin = origin
        origin_ports = get_ports(origin)
        if len(origin_ports) <= 0:
            abort(404, f'region {origin} not found')
        origin = origin_ports

    if not is_port(destination):
        destination_ports = get_ports(destination)
        if len(destination_ports) <= 0:
            abort(404, f'region {destination} not found')
        destination = destination_ports

    averages = get_averages(origin, destination, date_from, date_to)

    return jsonify([average.to_dict() for average in averages])


