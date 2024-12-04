import os
import csv
import requests

from decouple import config
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

def load_courses():
    try:
        with open(config('COURSES_CSV')) as csvfile:
            reader = csv.DictReader(csvfile,delimiter=",")
            return list(reader)
    except IOError as e:
        print(e)

def get_token():
    client = BackendApplicationClient(client_id=config('CLIENT_ID'))
    oauth = OAuth2Session(client=client)
    auth_uri = f'{config("SIGAA_API_AUTH_BASE")}/authz-server/oauth/token'
    return oauth.fetch_token(token_url=auth_uri, client_id=config('CLIENT_ID'), client_secret=config('CLIENT_SECRET'))

def fetch_data(url, params):
    token = get_token()
    authorization_header = f"{token['token_type']}  {token['access_token']}"
    headers = {'Authorization': authorization_header, 'x-api-key': config('X_API_KEY')}
    response = requests.get(config("SIGAA_API_BASE") + url, params=params, headers=headers)
    return response.json() if response else None

def get_user_details(username):
    API_VERSION = config('API_VERSION', default='v0.1')
        
    sigaa_user = fetch_data(f'/usuario/{API_VERSION}/usuarios', {'login': username})
    sigaa_api_data = {
        'username': username,
        'email': sigaa_user[0]['email'],
        'name': sigaa_user[0]['nome-pessoa'],
    }

    student_params = { 'cpf-cnpj': sigaa_user[0]['cpf-cnpj'], 'situacao-discente': [1,8,9,11,12], 'sigla-nivel': 'G' }
    student = fetch_data(f'discente/{API_VERSION}/discentes', student_params) if sigaa_user else None
        
    if student:
        sigaa_api_data['cpf'] = student[0]['cpf-cnpj']
        sigaa_api_data['course_id'] = student[0]['id-curso']
        sigaa_api_data['course_name'] = student[0]['nome-curso']
    else:   
        return {"error" : f'Student returned {student} for user {username}'}
    return sigaa_api_data