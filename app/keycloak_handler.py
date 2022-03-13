from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi_keycloak import FastAPIKeycloak, OIDCUser
from main import app

idp = FastAPIKeycloak(
    server_url=os.getenv("KEYCLOAK_SERVER_URL"), 
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret=os.getenv("KEYCLOAK_CLIENT_SECRET"), 
    admin_client_secret=os.getenv("KEYCLOAK_ADMIN_CLIENT_SECRET"),
    realm=os.getenv("KEYCLOAK_REALM"),
    callback_uri=os.getenv("KEYCLOAK_CALLBACK_URI")
)
idp.add_swagger_config(app)

def current_users(user: OIDCUser = Depends(idp.get_current_user())):
    return user

def company_admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    return f'Hi admin premium user {user}'

def user_roles(user: OIDCUser = Depends(idp.get_current_user)):
    return f'{user.roles}'

def login_redirect():
    return RedirectResponse(idp.login_uri)

def callback(session_state: str, code: str):
    return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token