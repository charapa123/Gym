


SELECT
insert_timestamp,
  answers->>'responseId' AS response_id,
  answers->>'createTime' AS create_time,
  answers->>'respondentEmail' AS respondent_email,
  q.key AS question_id,
  q.value->'textAnswers'->'answers'->0->>'value' AS answer
FROM {{ source('raw', 'raw_form_answers') }},
  jsonb_each(answers->'answers') AS q