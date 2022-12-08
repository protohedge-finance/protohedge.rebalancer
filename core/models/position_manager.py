from core.models.allocation import Allocation
from core.models.exposure import Exposure
from core.models.allocation import Allocation

class PositionManager:
	def __init__(self, name: str, address: str, position_worth: int, cost_basis: int, pnl: int, token_exposures: list[Exposure], token_allocation: list[Allocation], price: int, collateral_ratio: int):
		self.name: str = name
		self.address: str = address
		self.position_worth: int = position_worth
		self.cost_basis: int = cost_basis
		self.pnl: int = pnl 
		self.token_exposures: list[Exposure] = token_exposures
		self.token_allocation: list[Allocation] = token_allocation		
		self.price: int = price
		self.collateral_ratio: int = collateral_ratio