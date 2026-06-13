-- {{ config(materialized='table') }}
with revenue as (
    select * from {{ ref('fct_revenue') }}
),

contracts as (
    select * from {{ ref('stg_contracts') }}
)

select
    -- Total vs active customers
    count(distinct c.customer_id) as total_customers,
    count(distinct case when c.status = 'active'
        then c.customer_id end) as active_customers,

    -- ARR and MRR
    sum(case when c.status = 'active'
        then c.arr else 0 end) as total_arr,
    sum(case when c.status = 'active'
        then c.arr else 0 end) / 12 as mrr,

    -- Collection rate (%)
    round(
        sum(case when r.payment_status != 'unpaid'
            then r.amount_paid else 0 end) /
        nullif(sum(r.invoiced_amount), 0) * 100, 1) as collections_rate_pct,

    -- Avg days to collect
    round(avg(case when r.days_to_collect is not null
        then r.days_to_collect end), 1) as avg_days_to_collect

from contracts c
left join revenue r on c.contract_id = r.contract_id