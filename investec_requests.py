import base64
import json
import requests

domain = 'https://openapi.investec.com'


def encode_base64(unencoded):
    return str(base64.b64encode(unencoded.encode('ascii')), encoding='ascii')


def get_token():
    with open('credentials.json') as f:
        authentication_credentials = json.loads(json.load(f))

    client_id = str(authentication_credentials['client_id'])
    password = str(authentication_credentials['client_password'])
    api_key = str(authentication_credentials['x_api_key'])

    url = domain + "/identity/v2/oauth2/token"
    encoded_auth = encode_base64(f'{client_id}:{password}')
    payload = 'grant_type=client_credentials'
    headers = {
        'x-api-key': f'{api_key}==',
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_auth}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_object = response.json()
    return response_object['access_token']


def get_account_ids():
    token = get_token()
    url = domain + "/za/pb/v1/accounts"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response_object = response.json()
    ids = []
    for account in response_object['data']['accounts']:
        ids.append(account['accountId'])
    return ids


def get_balance(account_id):
    token = get_token()
    url = domain + f"/za/pb/v1/accounts/{account_id}/balance"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    response_object = response.json()
    return response_object['data']


def get_transactions(account_id, start_date=None, end_date=None):
    token = get_token()
    url = domain + f"/za/pb/v1/accounts/{account_id}/transactions"
    if start_date is not None and end_date is not None:
        url = domain + f"/za/pb/v1/accounts/{account_id}/transactions?fromDate={start_date}&toDate={end_date}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response_object = response.json()
    return response_object['data']['transactions']
