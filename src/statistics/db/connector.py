from typing import Optional

import postgresql


class Connector:
    __ref_instance = None
    # Connection
    _connection = None

    def __new__(cls, *args, **kwargs):
        if cls.__ref_instance is None:
            cls.__ref_instance = cls.__init__()

    def get_connection(self, login: Optional[str] = "postgres", password: Optional[str] = "admin"):
        if self._connection is None:
            self._connection = postgresql.open('pq://{0}:{1}@localhost:5433/postgres'.format(
                login,
                password
            ))
        return self._connection
