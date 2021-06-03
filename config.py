from os import environ


class Config(object):
    DB_CONFIG = {
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 20,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 10,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.

        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.

        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds

        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 180  # 3 minutes
    }
    DB_USER = environ['DB_USER']
    DB_PASS = environ['DB_PASS']
    DB_NAME = environ['DB_NAME']
    DB_SOCKET_DIR = environ.get('DB_SOCKET_DIR', '/cloudsql')
    CLOUD_SQL_CONNECTION_NAME = environ['CLOUD_SQL_CONNECTION_NAME']
    PROJECT_ID = environ['PROJECT_ID']
    TARGET_URL = environ['TARGET_URL']
