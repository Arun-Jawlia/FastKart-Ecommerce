import redis
from app.core.config import settings

redis_client = redis.Redis.from_url(
    settings.redis_url,
    decode_responses  = True,
    # protocol=2,
    socket_connect_timeout=1,
    socket_timeout=1,
)