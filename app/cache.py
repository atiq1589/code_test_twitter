import json
import aioredis.sentinel
from app.settings import settings

addresses = []
for port in settings.CACHE_PORTS:
    addresses.append((settings.CACHE_CONNECTION, port))

sentinel = aioredis.sentinel.Sentinel(addresses)

async def set_cache(key, value, **kwargs):
    redis = sentinel.master_for("mymaster")
    return await redis.set(key, json.dumps(value, default=str), **kwargs)

async def get_cache(key):
    redis = sentinel.slave_for("mymaster")
    value = await redis.get(key)
    if value:
        return json.loads(value)
    return None

