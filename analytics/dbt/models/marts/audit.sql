{{ config(materialized='table') }}

-- Daily audit volume by action — feeds the SOC2 evidence pack and the
-- ops/quality dashboards.

select
    date_trunc('day', created_at) as day,
    tenant_id,
    action,
    status,
    count(*) as event_count
from {{ source('public', 'audit_logs') }}
group by 1, 2, 3, 4
