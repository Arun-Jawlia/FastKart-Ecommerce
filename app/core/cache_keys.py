
def product_cache_key(product_id: int) -> str:
    return f"product:{product_id}"

def rate_limit_cache_key(client_ip: str) -> str:
    return f"rate_limit:login:{client_ip}"