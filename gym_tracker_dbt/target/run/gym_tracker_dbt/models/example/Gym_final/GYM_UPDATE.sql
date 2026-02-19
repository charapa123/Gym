
      
        
        
        delete from "gym"."pres"."GYM_UPDATE" as DBT_INTERNAL_DEST
        where (response_Id) in (
            select distinct response_Id
            from "GYM_UPDATE__dbt_tmp210437969665" as DBT_INTERNAL_SOURCE
        );

    

    insert into "gym"."pres"."GYM_UPDATE" ("insert_timestamp", "response_id", "create_time", "respondent_email", "Body_Part", "Weight", "Reps", "Exercises")
    (
        select "insert_timestamp", "response_id", "create_time", "respondent_email", "Body_Part", "Weight", "Reps", "Exercises"
        from "GYM_UPDATE__dbt_tmp210437969665"
    )
  