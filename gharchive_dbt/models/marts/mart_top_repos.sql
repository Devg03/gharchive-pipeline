with repo_activity as (
    select * from {{ ref('stg_repo_activity') }}
)

select
    repo_name,
    event_count

from repo_activity
where event_count < 50000
order by event_count desc
limit 100