with source as (
    select * from `gharchive-pipeline.gharchive.repo_activity`
)

select
    repo_name,
    event_count

from source