import json
from redis import Redis 
from datetime import datetime

class StatsRepository:
	def __init__(self, redis: Redis):
		self.redis: Redis = redis	
	
	def add_rebalance_note(self, address: str, note: str):
		timestamp = int(datetime.utcnow().timestamp()*1e3)
		record = "{}:{}:{}" .format((address.lower()), timestamp, note)
		self.redis.zadd("vault_notes", { record: 0 })
		
