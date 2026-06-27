
SELECT

    ROW_NUMBER() OVER (
        ORDER BY channel_name
    ) AS channel_key,

    channel_name,

    'Medical Channel' AS channel_type,

    MIN(message_date) AS first_post_date,

    MAX(message_date) AS last_post_date,

    COUNT(*) AS total_posts,

    ROUND(
        AVG(views),
        2
    ) AS avg_views

FROM {{ ref('stg_telegram_messages') }}

GROUP BY channel_name

