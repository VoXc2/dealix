{{ config(materialized='table') }}

-- Deals by status per tenant per day. Stage transitions + win rate
-- feed the internal sales-ops Metabase dashboards.

select
    date_trunc('day', updated_at) as day,
    tenant_id,
    status,
    count(*) as deals_count,
    sum(case when status = 'won' then 1 else 0 end) as won_count,
    sum(case when status = 'lost' then 1 else 0 end) as lost_count
from {{ source('public', 'deals') }}
group by 1, 2, 3
