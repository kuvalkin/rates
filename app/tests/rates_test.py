import pytest
import requests

# todo to env
ENDPOINT = 'http://localhost:5000/rates'


def make_request(date_from=None, date_to=None, origin=None, destination=None) -> requests.Response:
    params = {}
    if date_from is not None:
        params['date_from'] = date_from
    if date_to is not None:
        params['date_to'] = date_to
    if origin is not None:
        params['origin'] = origin
    if destination is not None:
        params['destination'] = destination

    return requests.get(ENDPOINT, params)


def test_no_params_400():
    assert make_request().status_code == 400


def test_wrong_date_format_400():
    response = make_request('18.02.2022', '18.02.2022', 'CNYTN', 'SESTO')
    assert response.status_code == 400


def test_region_not_exists_404():
    response = make_request('2022-11-05', '2022-12-05', 'this_region_does_not_exists', 'SESTO')
    assert response.status_code == 404


def test_not_overlapping_dates_400():
    response = make_request(
        '2022-12-05', # date_from is bigger than date_to
        '2022-11-05',
        'CNYTN',
        'SESTO'
    )
    assert response.status_code == 400


@pytest.mark.parametrize(
    'date_from,date_to,origin,destination,expected',
    [
        ('2016-05-05', '2016-08-12', 'CNYTN', 'SESTO', []),
        ('2016-01-19', '2016-01-19', 'CNYTN', 'SESTO', [{'average_price': 1325, 'day': '2016-01-19'}]),
    ],
)
def test_valid_input_200(date_from: str, date_to: str, origin: str, destination: str, expected: list):
    response = make_request(date_from, date_to, origin, destination)
    assert response.status_code == 200

    payload = response.json()
    assert payload == expected
