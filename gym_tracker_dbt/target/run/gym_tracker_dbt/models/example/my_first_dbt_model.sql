
  
    

  create  table "gym"."pres"."GYM_RESPONSE__dbt_tmp"
  
  
    as
  
  (
    /*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/



-- SET SEARCH_PATH TO RAW;

WITH ANSWERS AS (

SELECT
insert_timestamp,
  answers->>'responseId' AS response_id,
  answers->>'createTime' AS create_time,
  answers->>'respondentEmail' AS respondent_email,
  q.key AS question_id,
  q.value->'textAnswers'->'answers'->0->>'value' AS answer
FROM "gym"."raw"."raw_form_answers",
  jsonb_each(answers->'answers') AS q
)
,

QUESTIONS AS (
SELECT
    -- raw_form_questions.id AS raw_id,
    item.value->>'itemId' AS itemId,
    CASE WHEN item.value->>'title' LIKE '%Exercises%' THEN 'Exercises' ELSE item.value->>'title' END AS TITLE,
    item.value->'questionItem'->'question'->>'questionId' AS questionId,
    item.value->'questionItem'->'question'->'choiceQuestion'->>'type' AS choiceQuestionType,
    option.value->>'key' AS option_key,
    option.value->>'value' AS option_value
FROM
    "gym"."raw"."raw_form_questions",
    jsonb_array_elements(questions->'items') AS item
LEFT JOIN
    jsonb_array_elements(item.value->'questionItem'->'question'->'choiceQuestion'->'options') AS option
    ON TRUE
)


SELECT
    A.insert_timestamp,
    A.response_id,
    A.create_time,
    A.respondent_email,
    MAX(A.answer) FILTER (WHERE Q.title = 'Which body part did you work out?') AS "Body_Part",
    MAX(A.answer) FILTER (WHERE Q.title = 'How heavy was the weight?') AS "Weight",
    MAX(A.answer) FILTER (WHERE Q.title = 'How many reps?') AS "Reps",
	MAX(A.answer) FILTER (WHERE Q.title = 'Exercises') AS "Exercises"
	
FROM
    answers A
INNER JOIN
    questions Q ON A.question_id = Q.questionid
GROUP BY
    A.insert_timestamp,
    A.response_id,
    A.create_time,
    A.respondent_email

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
  );
  