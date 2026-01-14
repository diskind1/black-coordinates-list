import json
import os
import redis
from schemas import CoordinateData

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

REDIS_KEY = "coordinates_list"

def save_coordinate(data: CoordinateData):
    data_json = data.model_dump_json()
    r.rpush(REDIS_KEY, data_json)
    return True

def get_all_coordinates():
    items = r.lrange(REDIS_KEY, 0, -1)
    return [json.loads(item) for item in items]

# get_data = get_all_coordinates()
# print(get_data)
