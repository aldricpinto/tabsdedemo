import snowflake.connector
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import os

load_dotenv()

user=os.getenv('SNOWFLAKE_USER')
password=os.getenv('SNOWFLAKE_PASSWORD')
account=os.getenv('SNOWFLAKE_ACCOUNT')
warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
database=os.getenv('SNOWFLAKE_DATABASE')
schema=os.getenv('SNOWFLAKE_SCHEMA')

fake = Faker()

def generate_customers(n=50):
    return pd.DataFrame([{
        'customer_id': f'CUST_{i:04d}',
        'company_name': fake.company(),
        'industry': random.choice(['SaaS', 'Fintech', 'Healthcare', 'E-commerce']),
        'created_at': fake.date_between('-2y', 'today')
    } for i in range(n)])

def generate_contracts(customers):
    contracts = []
    for _, c in customers.iterrows():
        for _ in range(random.randint(1, 3)):
            start = fake.date_between('-1y', 'today')
            contracts.append({
                'contract_id': f'CON_{len(contracts):04d}',
                'customer_id': c['customer_id'],
                'arr': random.choice([12000, 24000, 36000, 60000, 120000]),
                'billing_frequency': random.choice(['monthly', 'quarterly', 'annual']),
                'start_date': start,
                'end_date': start + timedelta(days=365),
                'status': random.choice(['active', 'active', 'active', 'churned'])
            })
    return pd.DataFrame(contracts)

def generate_invoices(contracts):
    invoices = []
    for _, c in contracts.iterrows():
        months = 12 if c['billing_frequency'] == 'monthly' else (4 if c['billing_frequency'] == 'quarterly' else 1)
        amount = c['arr'] / months
        for m in range(months):
            invoices.append({
                'invoice_id': f'INV_{len(invoices):04d}',
                'contract_id': c['contract_id'],
                'customer_id': c['customer_id'],
                'amount': round(amount, 2),
                'issued_date': c['start_date'] + timedelta(days=30 * m),
                'due_date': c['start_date'] + timedelta(days=30 * m + 30),
                'status': random.choice(['paid', 'paid', 'paid', 'overdue', 'pending'])
            })
    return pd.DataFrame(invoices)

def generate_payments(invoices):
    payments = []
    for _, inv in invoices[invoices['status'] == 'paid'].iterrows():
        payments.append({
            'payment_id': f'PAY_{len(payments):04d}',
            'invoice_id': inv['invoice_id'],
            'customer_id': inv['customer_id'],
            'amount_paid': inv['amount'],
            'payment_date': inv['due_date'] + timedelta(days=random.randint(-5, 15)),
        })
    return pd.DataFrame(payments)

# Load to Snowflake
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

customers = generate_customers()
contracts = generate_contracts(customers)
invoices = generate_invoices(contracts)
payments = generate_payments(invoices)



for df, table in [(customers, 'CUSTOMERS'), (contracts, 'CONTRACTS'),
                  (invoices, 'INVOICES'), (payments, 'PAYMENTS')]:
    write_pandas(conn, df, table, auto_create_table=True, overwrite=True)
    print(f'Loaded {len(df)} rows into {table}')

conn.close()