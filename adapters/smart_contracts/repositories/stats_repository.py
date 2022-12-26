from redis import Redis 

class StatsRepository:
	def __init__(self, redis: Redis):
		self.redis: Redis = redis	
	
	def add_rebalance_outcome(self, outcome: str):
		self.redis.lpush("rebalance_outcomes", outcome)
		
