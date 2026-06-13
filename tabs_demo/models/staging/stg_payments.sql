select
    "payment_id"        as payment_id,
    "invoice_id"        as invoice_id,
    "customer_id"       as customer_id,
    "amount_paid"       as amount_paid,
    "payment_date"::date as payment_date
from {{ source('raw', 'payments') }}