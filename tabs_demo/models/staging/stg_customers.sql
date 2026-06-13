select
    "customer_id"       as customer_id,
    "company_name"      as company_name,
    "industry"          as industry,
    "created_at"::date  as created_date
from {{ source('raw', 'customers') }}