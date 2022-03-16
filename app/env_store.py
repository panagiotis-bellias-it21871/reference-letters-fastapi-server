# Postgres
db_url=os.getenv("DATABASE_URL")

# Minio
bucket=os.getenv("MIN_IO_BUCKET_NAME")
access_key=os.getenv("MIN_IO_ACCESS_KEY")
secret_key=os.getenv("MIN_IO_SECRET_KEY")
minio_server=os.getenv("MIN_IO_SERVER", default="localhost")

# Keycloak
server_url=os.getenv("KEYCLOAK_SERVER_URL"), 
client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"), 
admin_client_secret=os.getenv("KEYCLOAK_ADMIN_CLIENT_SECRET"),
realm=os.getenv("KEYCLOAK_REALM"),
callback_uri=os.getenv("KEYCLOAK_CALLBACK_URI")