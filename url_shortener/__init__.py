from flask import Flask
import sqlalchemy
from google.cloud import secretmanager
from config import Config


# Initiate the Secret Manager client.
client = secretmanager.SecretManagerServiceClient()
# Access the secret.
secret = client.access_secret_version(request={
    "name": f"projects/{Config.PROJECT_ID}/secrets/URL_SHORTENER_KEY/versions/latest"
})
# Initiate Flask app
app = Flask(__name__)
# Define app's secret key
app.secret_key = secret.payload.data.decode('UTF-8')
# App's configuration
app.config.from_object(Config)


def init_unix_connection_engine(db_config):
    db_user = app.config['DB_USER']
    db_pass = app.config['DB_PASS']
    db_name = app.config['DB_NAME']
    db_socket_dir = app.config['DB_SOCKET_DIR']
    cloud_sql_connection_name = app.config['CLOUD_SQL_CONNECTION_NAME']

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # postgresql+pg8000://<db_user>:<db_pass>@/<db_name>
        # ?unix_sock=<socket_path>/<cloud_sql_instance_name>/.s.PGSQL.5432
        sqlalchemy.engine.url.URL.create(
            drivername="postgresql+pg8000",
            username=db_user,
            password=db_pass,
            database=db_name,
            query={
                "unix_sock": "{}/{}/.s.PGSQL.5432".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )
    pool.dialect.description_encoding = None
    return pool


def init_connection_engine():
    return init_unix_connection_engine(app.config['DB_CONFIG'])

from url_shortener import routes
