select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select answers
from "gym"."raw"."raw_form_answers"
where answers is null



      
    ) dbt_internal_test