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