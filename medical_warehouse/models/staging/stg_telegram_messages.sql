WITH source AS (

    SELECT *
    FROM raw.telegram_messages

)

SELECT

    message_id,
    channel_name,

    CAST(message_date AS timestamp)
        AS message_date,

    message_text,

    COALESCE(views,0) AS views,

    COALESCE(forwards,0) AS forwards,

    has_media,

    image_path,

    LENGTH(
        COALESCE(message_text,'')
    ) AS message_length,

    CASE
        WHEN image_path IS NOT NULL
        THEN TRUE
        ELSE FALSE
    END AS has_image

FROM source