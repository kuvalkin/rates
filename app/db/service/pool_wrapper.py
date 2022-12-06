from psycopg_pool import ConnectionPool


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
