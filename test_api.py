import requests

domain = 'http://localhost:8080'


def set_credentials(json_credentials):
    url = domain + '/save_credentials'
    response = requests.post(url, data=json_credentials)
    return response


def get_credentials():
    url = domain + '/get_credentials'
    response = requests.get(url=url)
    json_response = response.json()
    return json_response


def generate_monthly():
    url = domain + '/generate_monthly_expenses'
    requests.put(url=url)


def generate_all_transactions(data):
    url = domain + '/get_all_transactions'

    requests.put(url=url, data=data)


def get_balances():
    url = domain + '/get_balances'
    response = requests.get(url=url)
    json_response = response.json()
    return json_response


if __name__ == "__main__":
    # enter your credentials here to test out the service
    data ="{\"client_id\": \"1\", \"client_password\": \"2\", \"x_api_key\": \"3\"}"

    set_credentials(data)
    print(get_credentials())
    print(get_balances())
    generate_monthly()
    data = '{"start_date": "2014-01-20", "end_date": "2022-12-20"}'
    generate_all_transactions(data)
