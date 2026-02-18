
  create view "gym"."pres"."my_second_dbt_model__dbt_tmp"
    
    
  as (
    -- Use the `ref` function to select from other models

select *
from "gym"."pres"."GYM_RESPONSE"
where id = 1
  );