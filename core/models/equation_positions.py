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

	def has_no_positions_for_type(self, position_type: PositionType):
		positions = self.long if position_type == PositionType.Long else self.short
		return len(positions) == 0

	def get_positions(self, position_type: PositionType):
		return self.long if position_type == PositionType.Long else self.short
	
