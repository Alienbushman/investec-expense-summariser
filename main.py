import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import json

from data_manipulation import save_monthly_transactions, save_all_transactions
from investec_requests import get_transactions, get_account_ids, get_balance


class Credentials(BaseModel):
    client_id: str
    client_password: str
    x_api_key: str


class BetweenDates(BaseModel):
    start_date: str
    end_date: str


class AuthenticationCredentials:
    client_id: str
    client_password: str
    x_api_key: str

    def set_auth(self, client_id, client_password, x_api_key):
        self.client_id = client_id
        self.client_password = client_password
        self.x_api_key = x_api_key


app = FastAPI()


@app.post("/save_credentials")
async def save_credentials(credentials: Credentials):
    authentication_credentials = AuthenticationCredentials()
    authentication_credentials.set_auth(credentials.client_id, credentials.client_password, credentials.x_api_key)
    json_cred = json.dumps(authentication_credentials.__dict__)

    with open('credentials.json', 'w') as f:
        json.dump(json_cred, f)

    return {"Status": "Credentials saved successfully"}


@app.get("/get_credentials")
async def get_credentials():
    with open('credentials.json') as f:
        authentication_credentials = json.loads(json.load(f))

    return {"client_id": authentication_credentials['client_id'], "x_api_key": authentication_credentials['x_api_key']}


@app.get("/get_balances")
async def get_balances():
    account_ids = get_account_ids()
    balances = []
    for account_id in account_ids:
        data = get_balance(account_id)
        balances.append({'account_id': account_id, 'currentBalance': data['currentBalance'],
                         'availableBalance': data['availableBalance'], })

    return json.dumps(balances).replace('\n', '').replace('\"', '\'')


@app.put("/generate_monthly_expenses")
async def generate_monthly_expenses():
    account_ids = get_account_ids()
    for account_id in account_ids:
        data = get_transactions(account_id)
        save_monthly_transactions(data, account_id)


@app.put("/get_all_transactions")
async def get_all_transactions(dates: BetweenDates):
    account_ids = get_account_ids()

    start_date = dates.start_date
    end_date = dates.end_date

    for account_id in account_ids:
        data = get_transactions(account_id, start_date, end_date)
        save_all_transactions(data, account_id, start_date, end_date)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
