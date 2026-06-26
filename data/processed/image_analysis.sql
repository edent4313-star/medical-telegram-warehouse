--Do promotional posts get more views?
SELECT

    image_category,

    ROUND(
        AVG(view_count),
        2
    ) AS avg_views

FROM analytics.fct_image_detections

GROUP BY image_category

ORDER BY avg_views DESC;



--Which channels use more visual content?
SELECT

    c.channel_name,

    COUNT(*) AS image_posts

FROM analytics.fct_image_detections d

JOIN analytics.dim_channels c
ON d.channel_key = c.channel_key

GROUP BY c.channel_name

ORDER BY image_posts DESC;