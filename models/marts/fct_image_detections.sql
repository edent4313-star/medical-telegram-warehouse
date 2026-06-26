SELECT

    f.message_id,

    f.channel_key,

    f.date_key,

    f.views,

    f.forwards,

    d.detected_objects,

    d.confidence_score,

    d.image_category

FROM {{ ref('fct_messages') }} f

INNER JOIN raw.image_detections d
    ON f.message_id = d.message_id