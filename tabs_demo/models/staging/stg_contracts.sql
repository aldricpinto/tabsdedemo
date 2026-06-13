select
    "contract_id"       as contract_id,
    "customer_id"       as customer_id,
    "arr"               as arr,
    "billing_frequency" as billing_frequency,
    "start_date"::date  as start_date,
    "end_date"::date    as end_date,
    "status"            as status
from {{ source('raw', 'contracts') }}
where "status" is not null