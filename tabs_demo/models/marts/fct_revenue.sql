with invoices as (
    select * from {{ ref('stg_invoices') }}
),

payments as (
    select * from {{ ref('stg_payments') }}
)

select
    i.invoice_id,
    i.customer_id,
    i.contract_id,
    i.invoiced_amount,
    p.amount_paid,
    i.issued_date,
    i.due_date,
    p.payment_date,
    datediff('day', i.due_date, p.payment_date) as days_to_collect,
    case
        when p.payment_id is null then 'unpaid'
        when p.payment_date <= i.due_date then 'paid_on_time'
        else 'paid_late'
    end as payment_status
from invoices i
left join payments p on i.invoice_id = p.invoice_id