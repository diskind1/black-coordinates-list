import os
import json
import redis
from schemas import CoordinateData

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

KEY_PREFIX = "coord:"


def _client() -> redis.Redis:
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def save_coordinate(data: CoordinateData) -> None:
    r = _client()
    key = f"{KEY_PREFIX}{data.ip}"
    r.set(key, data.model_dump_json())


def get_all_coordinates() -> list[dict]:
    r = _client()
    keys = list(r.scan_iter(match=f"{KEY_PREFIX}*"))
    if not keys:
        return []
    values = r.mget(keys)
    out = []
    for v in values:
        if not v:
            continue
        try:
            out.append(json.loads(v))
        except json.JSONDecodeError:
            continue
    return out
ס