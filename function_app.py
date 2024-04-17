import os
import json
import requests
import logging
import azure.functions as func

def exchange_token(access_token, client_id, client_secret, tenant_id):
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': access_token,
        'requested_token_use': 'on_behalf_of'
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        logging.info("Token exchange failed.")
        print("Token exchange failed.")
        return None

def get_user_profile(graph_token):
    headers = {
        'Authorization': f'Bearer {graph_token["access_token"]}',
        'Content-Type': 'application/json'
    }
    profile_url = 'https://graph.microsoft.com/v1.0/me'
    response = requests.get(profile_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.info("Failed to fetch user profile.")
        print("Failed to fetch user profile.")
        return None

def get_access_token(req):
    authorization_header = req.headers.get('Authorization')

    if authorization_header:
        # Authorizationヘッダーがある場合、Bearerトークンを取得
        parts = authorization_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            access_token = parts[1]
            return access_token
        else:
            print("Invalid Authorization header")
            return None
    else:
        print("Authorization header not found")
        return None

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger_vsc")
def http_trigger_vsc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    print('Python HTTP trigger function processed a request.')
    
    access_token = get_access_token(req)
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    tenant_id = os.getenv("TENANT_ID")

    graph_token = exchange_token(access_token, client_id, client_secret, tenant_id)
    print(graph_token)

    user_profile = get_user_profile(graph_token)
    print(user_profile)

    return func.HttpResponse(
        json.dumps(user_profile),
        status_code=200
    )

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )