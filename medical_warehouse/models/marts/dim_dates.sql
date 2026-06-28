
SELECT DISTINCT

    TO_CHAR(
        message_date,
        'YYYYMMDD'
    )::INTEGER AS date_key,

    DATE(message_date) AS full_date,

    TO_CHAR(
        message_date,
        'Day'
    ) AS day_name,

    TO_CHAR(
        message_date,
        'Month'
    ) AS month_name,

    EXTRACT(
        QUARTER
        FROM message_date
    ) AS quarter,

    EXTRACT(
        YEAR
        FROM message_date
    ) AS year,

    CASE
        WHEN EXTRACT(
            DOW
            FROM message_date
        ) IN (0, 6)
        THEN TRUE
        ELSE FALSE
    END AS is_weekend

FROM {{ ref('stg_telegram_messages') }}

