with source as (
    select * from `gharchive-pipeline.gharchive.events_by_type`
)

select
    type,
    events_by_type

from source