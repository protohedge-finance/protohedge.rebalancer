from core.models.position_manager import PositionManager
from core.models.allocation import Allocation

class EquationAllocation:
	def __init__(self, position_manager: PositionManager, allocation: Allocation, index: int):
		self.position_manager: PositionManager = position_manager
		self.allocation: Allocation = allocation
		self.index: int = index
