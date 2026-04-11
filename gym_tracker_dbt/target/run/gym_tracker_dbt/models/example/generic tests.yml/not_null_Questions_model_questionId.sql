select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select questionId
from "gym"."staging"."Questions_model"
where questionId is null



      
    ) dbt_internal_test