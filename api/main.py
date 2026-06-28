from fastapi import FastAPI
from fastapi import Query
from fastapi import HTTPException

from sqlalchemy import text

from api.database import engine

app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="Analytical API for Telegram medical channels",
    version="1.0"
)

@app.get(
    "/api/reports/top-products",
    tags=["Reports"]
)
def top_products(limit: int = 10):

    query = text("""
        SELECT
            LOWER(word) AS product,
            COUNT(*) AS mentions
        FROM (
            SELECT
                regexp_split_to_table(
                    message_text,
                    '\s+'
                ) AS word
            FROM analytics.fct_messages
        ) t
        WHERE LENGTH(word) > 4
        GROUP BY word
        ORDER BY mentions DESC
        LIMIT :limit
    """)

    with engine.connect() as conn:
        result = conn.execute(
            query,
            {"limit": limit}
        )

        return [
            dict(row._mapping)
            for row in result
        ]
    
@app.get(
    "/api/channels/{channel_key}/activity",
    tags=["Channels"]
)
def channel_activity(channel_key: str):

    query = text("""
        SELECT
            channel_key,
            COUNT(*) AS total_posts,
            AVG(views) AS avg_views
        FROM analytics.fct_messages
        WHERE channel_key = :channel_key
        GROUP BY channel_key
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {"channel_key": channel_key}
        ).fetchone()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Channel not found"
        )

    return dict(result._mapping)

@app.get(
    "/api/search/messages",
    tags=["Search"]
)
def search_messages(
    query: str,
    limit: int = 20
):

    sql = text("""
        SELECT
            message_id,
            channel_key,
            message_text
        FROM analytics.fct_messages
        WHERE
            LOWER(message_text)
            LIKE LOWER(:keyword)
        LIMIT :limit
    """)

    with engine.connect() as conn:

        result = conn.execute(
            sql,
            {
                "keyword": f"%{query}%",
                "limit": limit
            }
        )

        return [
            dict(row._mapping)
            for row in result
        ]

@app.get(
    "/api/reports/visual-content",
    tags=["Reports"]
)
def visual_content():

    query = text("""
        SELECT
            channel_key,
            COUNT(*) AS total_posts,

            SUM(
                CASE
                    WHEN has_image = TRUE
                    THEN 1
                    ELSE 0
                END
            ) AS image_posts,

            ROUND(
                100.0 *
                SUM(
                    CASE
                        WHEN has_image = TRUE
                        THEN 1
                        ELSE 0
                    END
                )
                /
                COUNT(*),
                2
            ) AS image_percentage

        FROM analytics.fct_messages

        GROUP BY channel_key
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            dict(row._mapping)
            for row in result
        ]   
    

    ##http://127.0.0.1:8000/docs