import os
from dotenv import load_dotenv
import ynab
import pandas as pd
from datetime import datetime

# Load .env variables
load_dotenv()
ACCESS_TOKEN = os.getenv("YNAB_TOKEN")

def get_client():
    config = ynab.Configuration(access_token=ACCESS_TOKEN)
    return ynab.ApiClient(config)

def get_budget_id():
    with get_client() as client:
        budgets_api = ynab.BudgetsApi(client)
        return budgets_api.get_budgets().data.budgets[0].id

def load_budget_summary(selected_month):
    with get_client() as client:
        budget_id = get_budget_id()

        months_api = ynab.MonthsApi(client)
        month_data = months_api.get_budget_month(budget_id, selected_month).data.month
        to_be_budgeted = month_data.to_be_budgeted / 1000

        tx_api = ynab.TransactionsApi(client)
        transactions = tx_api.get_transactions(budget_id).data.transactions

        inflow = 0
        outflow = 0

        for t in transactions:
            tx_data = t.to_dict()
            tx_date = tx_data['date']

            if isinstance(tx_date, str):
                tx_date = datetime.strptime(tx_date, "%Y-%m-%d").date()

            if tx_date.strftime("%m/%y") == selected_month.strftime("%m/%y"):
                if tx_data['amount'] > 0:
                    inflow += tx_data['amount']
                else:
                    outflow += tx_data['amount']

        return {
            "to_be_budgeted": to_be_budgeted,
            "inflow": inflow / 1000,
            "outflow": abs(outflow) / 1000,
        }

def load_transactions(selected_month):
    with get_client() as client:
        budget_id = get_budget_id()
        tx_api = ynab.TransactionsApi(client)
        transactions = tx_api.get_transactions(budget_id).data.transactions

        data = []

        for t in transactions:
            tx_data = t.to_dict()
            tx_date = tx_data['date']

            if isinstance(tx_date, str):
                tx_date = datetime.strptime(tx_date, "%Y-%m-%d").date()

            if tx_date.strftime("%m/%y") == selected_month.strftime("%m/%y"):
                # Improved category logic
                if t.subtransactions:
                    category_name = t.subtransactions[0].category_name
                else:
                    category_name = t.category_name if t.category_name else "Uncategorized"

                data.append({
                    "date": tx_date,
                    "amount": t.amount / 1000,
                    "payee_name": t.payee_name,
                    "memo": t.memo,
                    "category_name": category_name
                })

        df = pd.DataFrame(data)

        # 🐞 Debugging info
        if df.empty:
            print("⚠️ No transaction data matched the selected month.")
        else:
            print("✅ Loaded transactions columns:", df.columns.tolist())

        if 'category_name' in df.columns:
            df['category_name'].fillna("Uncategorized", inplace=True)

        return df

    with get_client() as client:
        budget_id = get_budget_id()
        tx_api = ynab.TransactionsApi(client)
        transactions = tx_api.get_transactions(budget_id).data.transactions

        data = []

        for t in transactions:
            tx_data = t.to_dict()
            tx_date = tx_data['date']

            if isinstance(tx_date, str):
                tx_date = datetime.strptime(tx_date, "%Y-%m-%d").date()

            if tx_date.strftime("%m/%y") == selected_month.strftime("%m/%y"):
                # Improved category logic
                if t.subtransactions:
                    category_name = t.subtransactions[0].category_name
                else:
                    category_name = t.category_name if t.category_name else "Uncategorized"

                data.append({
                    "date": tx_date,
                    "amount": t.amount / 1000,
                    "payee_name": t.payee_name,
                    "memo": t.memo,
                    "category_name": category_name
                })

        df = pd.DataFrame(data)
        df['category_name'].fillna("Uncategorized", inplace=True)
        return df

def export_transactions_to_csv(df, filename="transactions_export.csv"):
    df.to_csv(filename, index=False)
    return filename

def get_available_months():
    with get_client() as client:
        budget_id = get_budget_id()
        months_api = ynab.MonthsApi(client)
        months = months_api.get_budget_months(budget_id).data.months
        return sorted([m.month for m in months], reverse=True)
