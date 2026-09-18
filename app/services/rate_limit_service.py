from app.database.redis import redis_client


def check_rate_limit(
    key: str,
    limit: int,
    window: int,
)->bool:
    try: 
        current = redis_client.incr(key)

        if current == 1:
            redis_client.expire(
                key,
                window,
            )

        return current <= limit
    except RedisError:
        return True