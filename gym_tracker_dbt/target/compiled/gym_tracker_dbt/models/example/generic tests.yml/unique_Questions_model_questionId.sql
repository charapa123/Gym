
    
    

select
    questionId as unique_field,
    count(*) as n_records

from "gym"."staging"."Questions_model"
where questionId is not null
group by questionId
having count(*) > 1


