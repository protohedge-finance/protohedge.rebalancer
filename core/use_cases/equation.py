from core.models.equation_allocation import EquationAllocation

class Equation:
	def create(self, equation_allocations: list[EquationAllocation], symbols):
		equation = 0
		
		for alloc in equation_allocations:
			equation += alloc.position_manager.price * symbols[alloc.index] * alloc.allocation.leverage * alloc.allocation.percent

		return equation