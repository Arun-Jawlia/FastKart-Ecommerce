import json
from app.database.redis import redis_client

def set_cache(
    key: str,
    value,
    expire: int = 300
)->None:
    try:
        redis_client.set(
            key,
            json.dumps(value),
            ex=expire
        )
    except:
        pass


def get_cache(key: str):
    try: 
        value = redis_client.get(key)

        if value is None:
            return None

        return json.loads(value)
    except:
        pass



def delete_cache(key: str)->None:
    try:
        redis_client.delete(key)
    except:
        pass
