import os

from psycopg_pool import ConnectionPool


class PoolWrapper:
    def __init__(self):
        config = {
            'host': os.getenv('APP_DB_HOST'),
            'dbname': os.getenv('APP_DB_NAME'),
            'user': os.getenv('APP_DB_USER'),
            'password': os.getenv('APP_DB_PASSWORD'),
        }

        conn_str = ''
        for key, value in config.items():
            if value is not None:
                conn_str += '%s=%s ' % (key, value)

        self.__pool = ConnectionPool(conn_str, open=False)

    def __del__(self):
        self.__pool.close()

    @property
    def pool(self) -> ConnectionPool:
        self.__pool.open()
        return self.__pool
