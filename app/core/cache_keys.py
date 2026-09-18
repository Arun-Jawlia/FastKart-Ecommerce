
def product_cache_key(product_id: int) -> str:
    return f"product:{product_id}"