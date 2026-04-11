select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select response_id
from "gym"."raw"."raw_form_answers"
where response_id is null



      
    ) dbt_internal_test