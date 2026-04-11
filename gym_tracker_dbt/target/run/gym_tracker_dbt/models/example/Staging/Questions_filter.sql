
  create view "gym"."staging"."Questions_filter__dbt_tmp"
    
    
  as (
    SELECT QUESTIONS,INSERT_TIMESTAMP
FROM (
SELECT *,ROW_NUMBER() OVER ( ORDER BY INSERT_TIMESTAMP DESC) AS RN
FROM "gym"."raw"."raw_form_questions"
)
WHERE RN = 1
  );