import requests
import pandas as pd


base_url = 'http://localhost:8000/api/v1'
auth_url = f'{base_url}/login/access-token'
incidence_url = f'{base_url}/incidence/'


credentials = {
    'username': 'barba@gmail.com',  
    'password': 'chibolochivazo'   
}

def login_and_get_token():
    response = requests.post(auth_url, data=credentials)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    token = response.json().get('access_token')
    if not token:
        raise Exception("Token no encontrado en la respuesta.")
    return token

def get_data(token, skip=0, limit=100):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(incidence_url, headers=headers, params={'skip': skip, 'limit': limit})
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    data = response.json()
    incidences = data['data']
    df = pd.json_normalize(incidences, sep='_')  # Desanidar columnas
    return df