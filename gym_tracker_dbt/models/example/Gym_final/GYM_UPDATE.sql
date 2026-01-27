{{ config(
    materialized = 'table',
    alias = 'GYM_test'
) }}



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
    {{ref ('Answers_model')}} A
INNER JOIN
    {{ref ('Questions_model')}} Q ON A.question_id = Q.questionid
GROUP BY
    A.insert_timestamp,
    A.response_id,
    A.create_time,
    A.respondent_email