import redis
import json

def publish_result_message(data):
    conn = redis.StrictRedis()
    json_msg = json.dumps(data)
    conn.publish('_broadcast_:temujin_results', json_msg)

