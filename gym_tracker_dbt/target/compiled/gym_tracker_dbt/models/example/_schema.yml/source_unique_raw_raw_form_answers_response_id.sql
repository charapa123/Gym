
    
    

select
    response_id as unique_field,
    count(*) as n_records

from "gym"."raw"."raw_form_answers"
where response_id is not null
group by response_id
having count(*) > 1


