from core.models.position_type import PositionType


class Allocation:
	def __init__(self, percent: int, token: str, symbol: str, leverage: int, position_type: PositionType, collateral_ratio: int):
		self.percent: int = percent
		self.token: str = token
		self.symbol: str = symbol
		self.leverage: int = leverage
		self.position_type: PositionType = PositionType(position_type)
		self.collateral_ratio: int = collateral_ratio;