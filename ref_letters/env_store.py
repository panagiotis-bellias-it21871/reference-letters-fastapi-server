import os

# Keycloak
server_url=os.getenv("KEYCLOAK_SERVER_URL"), 
client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"), 
admin_client_secret=os.getenv("KEYCLOAK_ADMIN_CLIENT_SECRET"),
realm=os.getenv("KEYCLOAK_REALM"),
callback_uri=os.getenv("KEYCLOAK_CALLBACK_URI")