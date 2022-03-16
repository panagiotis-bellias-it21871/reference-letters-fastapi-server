from fastapi import Depends
from fastapi.responses import RedirectResponse
from fastapi_keycloak import FastAPIKeycloak, OIDCUser
from main import app

import env_store as env

idp = FastAPIKeycloak(
    server_url=env.server_url, 
    client_id=env.client_id,
    client_secret=env.client_secret, 
    admin_client_secret=env.admin_client_secret,
    realm=env.realm,
    callback_uri=env.callback_uri
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