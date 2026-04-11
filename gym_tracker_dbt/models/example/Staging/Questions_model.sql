SELECT
    -- raw_form_questions.id AS raw_id,
    item.value->>'itemId' AS itemId,
    CASE WHEN item.value->>'title' LIKE '%Exercises%' THEN 'Exercises' ELSE item.value->>'title' END AS TITLE,
    item.value->'questionItem'->'question'->>'questionId' AS questionId,
    item.value->'questionItem'->'question'->'choiceQuestion'->>'type' AS choiceQuestionType,
    option.value->>'key' AS option_key,
    option.value->>'value' AS option_value
FROM
    {{ref ('Questions_filter')}},
    jsonb_array_elements(questions->'items') AS item
LEFT JOIN
    jsonb_array_elements(item.value->'questionItem'->'question'->'choiceQuestion'->'options') AS option
    ON TRUE