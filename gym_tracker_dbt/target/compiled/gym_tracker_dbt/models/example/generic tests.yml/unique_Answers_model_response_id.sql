
    
    

select
    response_id as unique_field,
    count(*) as n_records

from "gym"."staging"."Answers_model"
where response_id is not null
group by response_id
having count(*) > 1


