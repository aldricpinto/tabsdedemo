select
    "invoice_id"        as invoice_id,
    "contract_id"       as contract_id,
    "customer_id"       as customer_id,
    "amount"            as invoiced_amount,
    "issued_date"::date as issued_date,
    "due_date"::date    as due_date,
    "status"            as status
from {{ source('raw', 'invoices') }}