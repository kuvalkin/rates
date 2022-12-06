from datetime import datetime

from psycopg.rows import class_row

from app.db.service import pool_wrapper
from app.models.average import Average


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
                    date_range.day::date,
                    avg_prices.average_price
                FROM
                    generate_series(%(date_from)s, %(date_to)s, interval '1 day') AS date_range(day)
                    LEFT JOIN (
                        SELECT
                            day,
                            CASE
                                WHEN COUNT(*) >= 3
                                THEN AVG(price)::int
                            ELSE
                                NULL
                            END average_price
                        FROM prices
                        WHERE
                            orig_code = ANY(%(origin)s)
                            AND dest_code = ANY(%(destination)s)
                            AND day BETWEEN %(date_from)s AND %(date_to)s
                            GROUP BY day
                    ) AS avg_prices
                    ON date_range.day = avg_prices.day;
            ''', {'date_from': date_from, 'date_to': date_to, 'origin': origin, 'destination': destination})

            return cur.fetchall()