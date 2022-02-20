import json
import aioredis.sentinel

addresses = []
for i in range(5):
    addresses.append(("redis-node-sentinel", 26379+i))

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

