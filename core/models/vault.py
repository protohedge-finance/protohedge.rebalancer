class Vault:
	def __init__(self, name: str, worth: int, cost_basis: int, amount_to_rebalance: int, available_liquidity: int):
		self.name = name
		self.worth = worth
		self.cost_basis = cost_basis
		self.amount_to_rebalance = amount_to_rebalance
		self.available_liquidity = available_liquidity
		