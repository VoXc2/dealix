{{ config(materialized='table') }}

-- Tenant-level KPI mart. Used by founder-only NPS / health dashboard.

select
    t.id as tenant_id,
    t.name,
    t.plan,
    t.status,
    t.currency,
    t.created_at,
    coalesce(u.users_active, 0) as users_active,
    coalesce(l.leads_total, 0) as leads_total,
    coalesce(d.deals_open, 0) as deals_open,
    coalesce(d.deals_won, 0) as deals_won
from {{ source('public', 'tenants') }} t
left join (
    select tenant_id, count(*) as users_active
    from {{ source('public', 'users') }}
    where is_active is true and deleted_at is null
    group by 1
) u on u.tenant_id = t.id
left join (
    select tenant_id, count(*) as leads_total
    from {{ source('public', 'leads') }}
    where deleted_at is null
    group by 1
) l on l.tenant_id = t.id
left join (
    select
        tenant_id,
        sum(case when status not in ('won','lost','abandoned') then 1 else 0 end) as deals_open,
        sum(case when status = 'won' then 1 else 0 end) as deals_won
    from {{ source('public', 'deals') }}
    group by 1
) d on d.tenant_id = t.id
