
    
    

select
    answers as unique_field,
    count(*) as n_records

from "gym"."raw"."raw_form_answers"
where answers is not null
group by answers
having count(*) > 1


