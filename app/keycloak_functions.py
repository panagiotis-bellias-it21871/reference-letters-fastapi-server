import os

APP_BASE_URL = os.getenv("APP_BASE_URL")
KEYCLOAK_BASE_URL = os.getenv("KEYCLOAK_BASE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
AUTH_URL = (
    f"{KEYCLOAK_BASE_URL}/auth/realms/Clients/protocol/openid-connect/auth?client_id={CLIENT_ID}&response_type=code"
)
TOKEN_URL = (
    f"{KEYCLOAK_BASE_URL}/auth/realms/Clients/protocol/openid-connect/token"
)

