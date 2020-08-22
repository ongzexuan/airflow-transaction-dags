# Airflow DAG for Extracting Credit Transactions from Plaid API to PostgreSQL

This small repo demonstrates an example of a DAG that pulls credit card transaction data from Plaid, transforms the data, and puts it in a Postgres database. The schema of this table can be found in `database.md`, and can be created with `create_table_transactions.sql`.

I wrote it for my personal use, so there's a task for Chase, AMEX, Citi, and Discover. There are no differences between the tasks except for which token they use. You should customize it to your needs when you get your own tokens from Plaid.

### Environment

Create an environment file with the following:

```
ENVIRONMENT=local
CLIENT_ID=<FROM PLAID>
SECRET=<FROM PLAID>

API_HOST=https://development.plaid.com
ENDPOINT=/transactions/get

PG_DATABASE=
PG_HOST=
PG_PORT=
PG_USER=
PG_PASSWORD=
TABLE=transactions (Your database table)

# Account related access tokens from Plaid
DISCOVER_ACCESS_TOKEN=<FROM PLAID>
AMEX_ACCESS_TOKEN=<FROM PLAID>
CITI_ACCESS_TOKEN=<FROM PLAID>
CHASE_ACCESS_TOKEN=<FROM PLAID>

```

### Deployment

Git clone this folder in the DAGs folder of your Airflow instance, and the Airflow scheduler should pick it up in good time. If impatient, restart the Airflow scheduler.

### Minor notes

- Database inserts are idempotent, so it's ok to rerun the task.
- Script ignores pending transactions. Therefore you will have to wait for the pending transaction to become a real transaction before this script pulls it. There's more information about it on [Plaid](https://support.plaid.com/hc/en-us/articles/360008271814-Pending-transaction-overview).