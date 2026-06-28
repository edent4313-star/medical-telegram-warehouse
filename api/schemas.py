from pydantic import BaseModel


class TopProduct(BaseModel):
    product: str
    mentions: int


class ChannelActivity(BaseModel):
    channel_name: str
    total_posts: int
    avg_views: float


class MessageSearch(BaseModel):
    message_id: int
    channel_name: str
    message_text: str


class VisualContentStats(BaseModel):
    channel_name: str
    total_posts: int
    image_posts: int
    image_percentage: float