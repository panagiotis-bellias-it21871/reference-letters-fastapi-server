import json
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from keycloak import KeycloakOpenID

from .db import database, reference_letter_request_db, student_db, teacher_db
from .schemas import ReferenceLetterRequest, Student, Teacher, User

load_dotenv(verbose=True)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure client
keycloak_openid = KeycloakOpenID(server_url=os.getenv("KC_SERVER_URL", default="http://localhost:8080/auth/"),
                    client_id=os.getenv("KC_CLIENT_ID", default="example_client"),
                    realm_name=os.getenv("KC_REALM", default="example_realm"),
                    client_secret_key=os.getenv("KC_CLIENT_SECRET", default="some-client-secret"))

@app.on_event("startup")
async def connect():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
def read_root():
    return {"greetings": "Welcome to FastAPI Python"}

'''
KeyCloak NoAdmin Integration
'''
# Get Token
token = keycloak_openid.token("user", "password")

@app.get("/keycloak/test1")
async def keycloak_values1():
    # Get WellKnow
    config_well_known = keycloak_openid.well_known()
    # Get Token
    token2 = keycloak_openid.token("user", "password", totp="012345")
    return {
        "config_well_known": config_well_known,
        "token1": token,
        "token2": token2
    }

@app.get("/keycloak/userinfo")
async def keycloak_user_info():
    # Get Userinfo
    userinfo = keycloak_openid.userinfo(token['access_token'])
    return userinfo

@app.get("/keycloak/refresh")
async def keycloak_refresh():
    # Refresh token
    token = keycloak_openid.refresh_token(token['refresh_token'])
    return token

@app.get("/keycloak/logout")
async def keycloak_logout():
    # Logout
    keycloak_openid.logout(token['refresh_token'])

@app.get("/keycloak/test2")
async def keycloak_values2():
    # Get RPT (Entitlement)
    rpt = keycloak_openid.entitlement(token['access_token'], "resource_id")
    # Instropect RPT
    token_rpt_info = keycloak_openid.introspect(keycloak_openid.introspect(token['access_token'], rpt=rpt['rpt'],
                                     token_type_hint="requesting_party_token"))
    # Introspect Token
    token_info = keycloak_openid.introspect(token['access_token'])
    # Decode Token
    KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
    options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}
    token_info2 = keycloak_openid.decode_token(token['access_token'], key=KEYCLOAK_PUBLIC_KEY, options=options)
    # Get permissions by token
    keycloak_openid.load_authorization_config("example-authz-config.json")
    policies = keycloak_openid.get_policies(token['access_token'], method_token_info='decode', key=KEYCLOAK_PUBLIC_KEY)
    permissions = keycloak_openid.get_permissions(token['access_token'], method_token_info='introspect')
    # Get UMA-permissions by token
    permissions2 = keycloak_openid.uma_permissions(token['access_token'])
    # Get UMA-permissions by token with specific resource and scope requested
    permissions3 = keycloak_openid.uma_permissions(token['access_token'], permissions="Resource#Scope")
    # Get auth status for a specific resource and scope by token
    auth_status = keycloak_openid.has_uma_access(token['access_token'], "Resource#Scope")
    return {
        'rpt': rpt,
        'token_rpt_info': token_rpt_info,
        'token_info': token_info,
        'token_info2': token_info2,
        'policies': policies,
        'permissions': permissions,
        'permissions2': permissions2,
        'permissions3': permissions3,
        'auth_status': auth_status
    }
    

'''
KeyCloak Admin Integration
'''
from keycloak import KeycloakAdmin

keycloak_admin = KeycloakAdmin(server_url=os.getenv("KC_SERVER_URL", default="http://localhost:8080/auth/"),
                               username='example-admin',
                               password='secret',
                               realm_name=os.getenv("KC_REALM_ADMIN", default="master"),
                               user_realm_name="only_if_other_realm_than_master",
                               client_secret_key=os.getenv("KC_CLIENT_SECRET", default="some-client-secret"),
                               verify=True)

#admin_client_secret=os.getenv("KC_ADMIN_CLIENT_SECRET", default="admin-cli-secret"),
#callback_uri=os.getenv("KC_CALLBACK_URI", default="http://localhost:8081/callback")

@app.get("/keycloak/admin/users/new")
async def keycloak_admin_new_users():
    # Add user
    new_user1 = keycloak_admin.create_user({"email": "example1@example.com",
                    "username": "example1@example.com",
                    "enabled": True,
                    "firstName": "Example1",
                    "lastName": "Example1"})
    # Add user and raise exception if username already exists
    # exist_ok currently defaults to True for backwards compatibility reasons
    new_user2 = keycloak_admin.create_user({"email": "example2@example.com",
                    "username": "example2@example.com",
                    "enabled": True,
                    "firstName": "Example2",
                    "lastName": "Example2"},
                    exist_ok=False)
    # Add user and set password
    new_user3 = keycloak_admin.create_user({"email": "example3@example.com",
                    "username": "example3@example.com",
                    "enabled": True,
                    "firstName": "Example3",
                    "lastName": "Example3",
                    "credentials": [{"value": "secret","type": "password",}]})

    # Add user and specify a locale
    new_user4 = keycloak_admin.create_user({"email": "example@example.fr",
                    "username": "example@example.fr",
                    "enabled": True,
                    "firstName": "Example4",
                    "lastName": "Example4",
                    "attributes": {
                      "locale": ["fr"]
                    }})
    return {
        'new_user1': new_user1,
        'new_user2': new_user2,
        'new_user3': new_user3,
        'new_user4': new_user4,
    }

@app.get("/keycloak/admin/test")
async def keycloak_admin_values():
    # User counter
    count_users = keycloak_admin.users_count()
    # Get users Returns a list of users, filtered according to query parameters
    users = keycloak_admin.get_users({})
    # Get user ID from name
    user_id_keycloak = keycloak_admin.get_user_id("example@example.com")
    # Get User
    user = keycloak_admin.get_user("user-id-keycloak")
    # Update User
    response1 = keycloak_admin.update_user(user_id="user-id-keycloak",
                                      payload={'firstName': 'Example Update'})
    # Update User Password
    response2 = keycloak_admin.set_user_password(user_id="user-id-keycloak", password="secret", temporary=True)
    # Get User Credentials
    credentials = keycloak_admin.get_credentials(user_id='user_id')
    # Get User Credential by ID
    credential = keycloak_admin.get_credential(user_id='user_id', credential_id='credential_id')
    # Delete User Credential
    response3 = keycloak_admin.delete_credential(user_id='user_id', credential_id='credential_id')
    # Delete User
    response4 = keycloak_admin.delete_user(user_id="user-id-keycloak")
    # Get consents granted by the user
    consents = keycloak_admin.consents_user(user_id="user-id-keycloak")
    # Send User Action
    response5 = keycloak_admin.send_update_account(user_id="user-id-keycloak",
                                                payload=json.dumps(['UPDATE_PASSWORD']))
    # Send Verify Email
    response6 = keycloak_admin.send_verify_email(user_id="user-id-keycloak")
    # Get sessions associated with the user
    sessions = keycloak_admin.get_sessions(user_id="user-id-keycloak")
    # Get themes, social providers, auth providers, and event listeners available on this server
    server_info = keycloak_admin.get_server_info()
    # Get clients belonging to the realm Returns a list of clients belonging to the realm
    clients = keycloak_admin.get_clients()
    # Get client - id (not client-id) from client by name
    client_id = keycloak_admin.get_client_id("my-client")
    # Get representation of the client - id of client (not client-id)
    client = keycloak_admin.get_client(client_id="client_id")
    # Get all roles for the realm or client
    realm_roles1 = keycloak_admin.get_realm_roles()
    # Get all roles for the client
    client_roles = keycloak_admin.get_client_roles(client_id="client_id")
    # Get client role
    role = keycloak_admin.get_client_role(client_id="client_id", role_name="role_name")
    # Warning: Deprecated
    # Get client role id from name
    role_id1 = keycloak_admin.get_client_role_id(client_id="client_id", role_name="test")
    # Create client role
    keycloak_admin.create_client_role(client_role_id='client_id', payload={'name': 'roleName', 'clientRole': True})
    # Assign client role to user. Note that BOTH role_name and role_id appear to be required.
    keycloak_admin.assign_client_role(client_id="client_id", user_id="user_id", role_id="role_id", role_name="test")
    # Retrieve client roles of a user.
    keycloak_admin.get_client_roles_of_user(user_id="user_id", client_id="client_id")
    # Retrieve available client roles of a user.
    keycloak_admin.get_available_client_roles_of_user(user_id="user_id", client_id="client_id")
    # Retrieve composite client roles of a user.
    keycloak_admin.get_composite_client_roles_of_user(user_id="user_id", client_id="client_id")
    # Delete client roles of a user.
    keycloak_admin.delete_client_roles_of_user(client_id="client_id", user_id="user_id", roles={"id": "role-id"})
    keycloak_admin.delete_client_roles_of_user(client_id="client_id", user_id="user_id", roles=[{"id": "role-id_1"}, {"id": "role-id_2"}])
    # Get all client authorization resources
    client_resources = keycloak_admin.get_client_authz_resources(client_id="client_id")
    # Get all client authorization scopes
    client_scopes = keycloak_admin.get_client_authz_scopes(client_id="client_id")
    # Get all client authorization permissions
    client_permissions = keycloak_admin.get_client_authz_permissions(client_id="client_id")
    # Get all client authorization policies
    client_policies = keycloak_admin.get_client_authz_policies(client_id="client_id")
    # Create new group
    group1 = keycloak_admin.create_group({"name": "Example Group"})
    # Get all groups
    groups = keycloak_admin.get_groups()
    # Get group
    group2 = keycloak_admin.get_group(group_id='group_id')
    # Get group by name
    group3 = keycloak_admin.get_group_by_path(path='/group/subgroup', search_in_subgroups=True)
    # Function to trigger user sync from provider
    keycloak_admin.sync_users(storage_id="storage_di", action="action")
    # Get client role id from name
    role_id2 = keycloak_admin.get_client_role_id(client_id=client_id, role_name="test")
    # Get all roles for the realm or client
    realm_roles2 = keycloak_admin.get_roles()
    # Assign client role to user. Note that BOTH role_name and role_id appear to be required.
    keycloak_admin.assign_client_role(client_id=client_id, user_id=user_id_keycloak, role_id=role_id1, role_name="test")
    # Assign realm roles to user
    keycloak_admin.assign_realm_roles(user_id=user_id_keycloak, roles=realm_roles1)
    # Get all ID Providers
    idps = keycloak_admin.get_idps()
    # Create a new Realm
    keycloak_admin.create_realm(payload={"realm": "demo"}, skip_exists=False)

    return {
        'count_users': count_users,
        'users': users,
        'user_id_keycloak': user_id_keycloak,
        'user': user,
        'response1': response1,
        'response2': response2,
        'credentials': credentials,
        'credential': credential,
        'response3': response3,
        'response4': response4,
        'consents': consents,
        'response5': response5,
        'response6': response6,
        'sessions': sessions,
        'server_info': server_info,
        'clients': clients,
        'client_id': client_id,
        'client': client,
        'realm_roles1': realm_roles1,
        'client_roles': client_roles,
        'role': role,
        'role_id1': role_id1,
        'client_resources': client_resources,
        'client_scopes': client_scopes,
        'client_permissions': client_permissions,
        'client_policies': client_policies,
        'group1': group1,
        'groups': groups,
        'group2': group2,
        'group3': group3,
        'role_id2': role_id2,
        'realm_roles2': realm_roles2,
        'idps': idps
    }


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.post("/language/")
async def language(name: str = Form(...), type: str = Form(...)):
    return {"name": name, "type": type}

@app.get("/rl_requests")
async def get_rl_requests():
    query = reference_letter_request_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.get("/rl_requests/{rl_request_id}")
async def get_a_rl_request(rl_request_id: int):
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == rl_request_id)
    user = await database.fetch_one(query)
    return {**user}

@app.post("/rl_requests")
async def add_rl_request(rl_request: ReferenceLetterRequest):
    query = reference_letter_request_db.insert().values(
        name=rl_request.name,
        is_approved=rl_request.is_approved,
        is_declined=rl_request.is_declined,
        is_pending=rl_request.is_pending
    )
    record_id = await database.execute(query)
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.put("/rl_requests/{rl_request_id}")
async def update_rl_request(rl_request_id: int, rl_request: ReferenceLetterRequest):
    query = reference_letter_request_db.update().where(reference_letter_request_db.c.id == rl_request_id).values(
        name=rl_request.name,
        is_approved=rl_request.is_approved,
        is_declined=rl_request.is_declined,
        is_pending=rl_request.is_pending
    )
    record_id = await database.execute(query)
    query = reference_letter_request_db.select().where(reference_letter_request_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/rl_requests/{rl_request_id}")
async def delete_rl_request(rl_request_id: int):
    query = reference_letter_request_db.delete().where(reference_letter_request_db.c.id == rl_request_id)
    return await database.execute(query)

@app.get("/students")
async def get_students():
    query = student_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.get("/students/{student_id}")
async def get_a_student(student_id: int):
    query = student_db.select().where(student_db.c.id == student_id)
    user = await database.fetch_one(query)
    return {**user}

@app.post("/students")
async def add_student(student: Student):
    query = student_db.insert().values(
        name=student.name,
        school_id=student.school_id,
        email=student.email
    )
    record_id = await database.execute(query)
    query = student_db.select().where(student_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    query = student_db.update().where(student_db.c.id == student_id).values(
        name=student.name,
        school_id=student.school_id,
        email=student.email
    )
    record_id = await database.execute(query)
    query = student_db.select().where(student_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    query = student_db.delete().where(student_db.c.id == student_id)
    return await database.execute(query)

@app.get("/teachers")
async def get_teachers():
    query = teacher_db.select()
    all_get = await database.fetch_all(query)
    return all_get

@app.get("/teachers/{teacher_id}")
async def get_a_teacher(teacher_id: int):
    query = teacher_db.select().where(teacher_db.c.id == teacher_id)
    user = await database.fetch_one(query)
    return {**user}

@app.post("/teachers")
async def add_teacher(teacher: Teacher):
    query = teacher_db.insert().values(
        name=teacher.name,
        email=teacher.email
    )
    record_id = await database.execute(query)
    query = teacher_db.select().where(teacher_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.put("/teachers/{teacher_id}")
async def update_teacher(teacher_id: int, teacher: Teacher):
    query = teacher_db.update().where(teacher_db.c.id == teacher_id).values(
        name=teacher.name,
        email=teacher.email
    )
    record_id = await database.execute(query)
    query = teacher_db.select().where(teacher_db.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}

@app.delete("/teachers/{teacher_id}")
async def delete_teacher(teacher_id: int):
    query = teacher_db.delete().where(teacher_db.c.id == teacher_id)
    return await database.execute(query)

"""
@app.get("/admin")
def admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    return f'Hi premium user{user}'

@app.get("/user/roles")
def user_roles(user: OIDCUser = Depends(idp.get_current_user)):
    return f'{user.roles}'
"""
