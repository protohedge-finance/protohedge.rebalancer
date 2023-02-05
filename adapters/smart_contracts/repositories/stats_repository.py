import json
from redis import Redis 
from datetime import datetime

class StatsRepository:
	def __init__(self, redis: Redis):
		self.redis: Redis = redis	
	
	def add_rebalance_history(self, address: str, note: str):
		timestamp = int(datetime.utcnow().timestamp()*1e3)
		record = "{}:{}:{}" .format((address.lower()), timestamp, note)
		self.redis.zadd("rebalance_history", { record: 0 })
		
