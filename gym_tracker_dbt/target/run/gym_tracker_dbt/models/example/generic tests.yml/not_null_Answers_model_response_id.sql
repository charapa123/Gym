select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select response_id
from "gym"."staging"."Answers_model"
where response_id is null



      
    ) dbt_internal_test