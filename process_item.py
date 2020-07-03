import json
import os
import requests
import psycopg2
import psycopg2.extras
import traceback

from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.postgres_operator import PostgresOperator

load_dotenv()

TODAY = datetime.today().strftime('%Y-%m-%d')
#TODAY = "2020-06-20" # DEBUG
#YESTERDAY = (date.today() - timedelta(days=10)).strftime('%Y-%m-%d')

TABLE = os.getenv("TABLE")
CLIENT_ID = os.getenv("CLIENT_ID")
SECRET = os.getenv("DEVELOPMENT_SECRET")
URL = os.getenv("API_HOST") + os.getenv("ENDPOINT")

# Database params
PG_HOST = os.getenv("PG_HOST")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")

dag_params = {
    "dag_id": "transaction_dag",
    "start_date": datetime(2020, 6, 1),
    "schedule_interval": None
}


def process_single_transaction(transaction):
    """
    Takes single Plaid Transaction object and returns a tuple of values that can be exported directly to Postgres.

    :param transaction: JSON object of transaction
    :return: dictionary of required fields for direct export to Postgres
    """

    transaction_id = transaction["transaction_id"]
    account_id = transaction["account_id"]
    name = transaction["name"]
    amount = transaction["amount"]
    category_id = transaction["category_id"]
    category = transaction["category"]
    date = transaction["date"]
    iso_currency_code = transaction["iso_currency_code"]
    location = json.dumps(transaction["location"])
    payment_channel = transaction["payment_channel"]
    transaction_type = transaction["transaction_type"]
    pending = transaction["pending"]
    payment_reference = transaction["payment_meta"]["reference_number"]
    merchant = transaction["merchant_name"]

    return (transaction_id,
            account_id,
            name,
            amount,
            category_id,
            category,
            date,
            iso_currency_code,
            location,
            payment_channel,
            transaction_type,
            pending,
            payment_reference,
            merchant
            )


def process_transactions(plaid_transaction):
    """
    Takes the raw JSON output from the Plaid Transaction API and outputs a list of tuple of the fields being exported to the Postgres database.

    :param plaid_transaction: JSON object of the raw JSON output from the Transaction API
    """

    # TODO: do something about Accounts and Items

    collected_transactions = []    
    for transaction in plaid_transaction["transactions"]:
        collected_transactions.append(process_single_transaction(transaction))

    return collected_transactions


def get_transactions(client_id, secret, access_token, start_date, end_date):

    request_body = {
        "client_id": client_id,
        "secret": secret,
        "access_token": access_token,
        "start_date": start_date,
        "end_date": end_date
    }

    r = requests.post(URL,
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(request_body))

    return r.json()


def insert_transactions(rows):

    conn = psycopg2.connect(dbname=PG_DATABASE,
                            user=PG_USER,
                            password=PG_PASSWORD,
                            host=PG_HOST,
                            port=PG_PORT
                            )

    try:
        insert_query = "INSERT INTO {} VALUES %s ON CONFLICT DO NOTHING".format(TABLE)
        template = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        psycopg2.extras.execute_values(conn.cursor(), insert_query, rows, template=template)
        conn.commit()

    except Exception as ex:
        traceback.print_exc()

    finally:
        conn.close()


def process_discover_transactions(**context):

    discover_access_token = os.getenv("DISCOVER_ACCESS_TOKEN", None)

    # Fail early if the env variable is not present
    assert discover_access_token is not None

    start_date = context["execution_date"].strftime('%Y-%m-%d')
    end_date = context["execution_date"].strftime('%Y-%m-%d')

    data = get_transactions(CLIENT_ID, SECRET, discover_access_token, start_date, end_date)
    rows = process_transactions(data)
    insert_transactions(rows)


def process_amex_transactions(**context):

    amex_access_token = os.getenv("AMEX_ACCESS_TOKEN", None)

    # Fail early if the env variable is not present
    assert amex_access_token is not None

    start_date = context["execution_date"].strftime('%Y-%m-%d')
    end_date = context["execution_date"].strftime('%Y-%m-%d')

    data = get_transactions(CLIENT_ID, SECRET, amex_access_token, start_date, end_date)
    rows = process_transactions(data)
    insert_transactions(rows)


def process_citi_transactions(**context):

    citi_access_token = os.getenv("CITI_ACCESS_TOKEN", None)

    # Fail early if the env variable is not present
    assert citi_access_token is not None

    start_date = context["execution_date"].strftime('%Y-%m-%d')
    end_date = context["execution_date"].strftime('%Y-%m-%d')

    data = get_transactions(CLIENT_ID, SECRET, citi_access_token, start_date, end_date)
    rows = process_transactions(data)
    insert_transactions(rows)


def process_chase_transactions(**context):

    chase_access_token = os.getenv("CHASE_ACCESS_TOKEN", None)

    # Fail early if the env variable is not present
    assert chase_access_token is not None

    start_date = context["execution_date"].strftime('%Y-%m-%d')
    end_date = context["execution_date"].strftime('%Y-%m-%d')

    data = get_transactions(CLIENT_ID, SECRET, chase_access_token, start_date, end_date)
    rows = process_transactions(data)
    insert_transactions(rows)


with DAG(**dag_params) as dag:

    # Task: Discover
    discover_task = PythonOperator(task_id="discover_task",
                                   python_callable=process_discover_transactions,
                                   provide_context=True
                                   )

    # Task: Amex
    amex_task = PythonOperator(task_id="amex_task",
                               python_callable=process_amex_transactions,
                               provide_context=True
                               )

    # Task: Citi
    citi_task = PythonOperator(task_id="citi_task",
                               python_callable=process_citi_transactions,
                               provide_context=True
                               )

    # Task: Chase
    chase_task = PythonOperator(task_id="chase_task",
                                python_callable=process_chase_transactions,
                                provide_context=True
                                )
