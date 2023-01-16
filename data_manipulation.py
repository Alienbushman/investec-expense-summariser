import pandas as pd
import os


def save_monthly_transactions(data, account_id):
    df = pd.DataFrame.from_dict(data)

    df['transactionDate'] = pd.to_datetime(df['transactionDate'])
    df = df.fillna(value="None")

    grouped_df = df.groupby(
        [df['transactionDate'].dt.year.rename('y'), df['transactionDate'].dt.month.rename('m'), 'transactionType'],
        dropna=False)[
        'amount'].sum()

    saved_name = f'monthly_summary_{account_id}.csv'
    path = os.path.join('reports', saved_name)
    grouped_df.to_csv(path)


def save_all_transactions(data, account_id, start_date, end_date):
    df = pd.DataFrame.from_dict(data)
    saved_name = f'all_transactions_from_{start_date}_to_{end_date}_{account_id}.csv'
    path = os.path.join('reports', saved_name)
    df.to_csv(path)
