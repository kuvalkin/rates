import re

from dataclasses import dataclass
from flask import Flask, request
from datetime import datetime
from psycopg_pool import ConnectionPool
from psycopg.rows import class_row

app = Flask(__name__)


# todo move to a separate file
class PoolWrapper:
    def __init__(self):
        # todo move to secrets or env variables
        self.__pool = ConnectionPool('secret', open=False)

    def __del__(self):
        if self.__pool:
            self.__pool.close()

    @property
    def pool(self) -> ConnectionPool:
        self.__pool.open()
        return self.__pool


pool_wrapper = PoolWrapper()


@dataclass
class Average:
    day: datetime
    average_price: int | None


@app.get("/rates")
def rates():
    date_from = get_date_from_request('date_from')
    date_to = get_date_from_request('date_to')
    origin = request.args.get('origin')
    destination = request.args.get('destination')

    # todo validation, 400 and stuff

    if not is_port(origin):
        origin = get_ports(origin)

    if not is_port(destination):
        destination = get_ports(destination)

    return get_averages(origin, destination, date_from, date_to)


def get_date_from_request(param: str) -> datetime:
    return datetime.strptime(request.args.get(param), '%Y-%m-%d')


def is_port(slug: str) -> bool:
    match = re.search('^[A-Z]{5}$', slug)

    return match is not None


def get_ports(region_slug: str) -> list[str]:
    with pool_wrapper.pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                WITH RECURSIVE regions_tree (slug)
                AS (
                    SELECT slug FROM regions WHERE slug = %s
                    UNION ALL
                    SELECT regions.slug FROM regions, regions_tree
                        WHERE regions.parent_slug IS NOT NULL AND regions.parent_slug = regions_tree.slug
                )
                SELECT ports.code FROM ports WHERE ports.parent_slug IN (SELECT regions_tree.slug FROM regions_tree);
            ''', [region_slug])

            ports = []
            for row in cur:
                ports.append(row[0])
            return ports


def get_averages(
    origin: str | list[str],
    destination: str | list[str],
    date_from: datetime,
    date_to: datetime,
) -> list[Average]:
    if origin is not list:
        origin = [origin]

    if destination is not list:
        destination = [destination]

    with pool_wrapper.pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Average)) as cur:
            cur.execute('''
                SELECT
                    day,
                    CASE
                        WHEN COUNT(*) >= 3
                        THEN CAST(AVG(price) AS INTEGER)
                    ELSE
                        NULL
                    END average_price
                FROM prices
                WHERE
                    orig_code = ANY(%s)
                    AND dest_code = ANY(%s)
                    AND day BETWEEN %s AND %s
                GROUP BY day;
            ''', (origin, destination, date_from, date_to))

            return cur.fetchall()