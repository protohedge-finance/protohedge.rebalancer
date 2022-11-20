from core.models.position_type import PositionType
from core.models.equation_allocation import EquationAllocation

class EquationPositions:
	def __init__(self):
		self.long: list[EquationAllocation] = []
		self.short: list[EquationAllocation] = []

	def add_position(self, position_type: PositionType, equation_allocation: EquationAllocation):
		if (position_type == PositionType.Long):
			self.long.append(equation_allocation)
		else:
			self.short.append(equation_allocation)
	
