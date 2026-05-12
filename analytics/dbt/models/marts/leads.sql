{{ config(materialized='table') }}

-- Daily mart: leads created per tenant per sector with fit/urgency
-- distributions. Powers the customer-facing benchmarks page (T3c).

select
    date_trunc('day', created_at) as day,
    tenant_id,
    coalesce(sector, 'unknown') as sector,
    count(*) as leads_count,
    avg(fit_score) as avg_fit,
    avg(urgency_score) as avg_urgency,
    percentile_cont(0.5) within group (order by fit_score) as p50_fit,
    percentile_cont(0.75) within group (order by fit_score) as p75_fit,
    percentile_cont(0.9) within group (order by fit_score) as p90_fit
from {{ source('public', 'leads') }}
where deleted_at is null
group by 1, 2, 3
