class UserRepository:
	def __init__(self, w3):
		self.w3 = w3

	def get_transaction_count(self, address: str) -> int:
		return self.w3.eth.get_transaction_count(address)	
		