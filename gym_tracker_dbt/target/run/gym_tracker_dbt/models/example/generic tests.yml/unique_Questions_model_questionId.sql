select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    questionId as unique_field,
    count(*) as n_records

from "gym"."staging"."Questions_model"
where questionId is not null
group by questionId
having count(*) > 1



      
    ) dbt_internal_test