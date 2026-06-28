SELECT *
FROM {{ ref('fct_messages') }}
WHERE date_key >
TO_CHAR(CURRENT_DATE,'YYYYMMDD')::INTEGER