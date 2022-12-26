from core.models.equation_allocation import EquationAllocation
from core.constants import BASIS_POINTS_DIVISOR

class Equation:
	def create(self, equation_allocations: list[EquationAllocation], symbols):
		equation = 0
		print("Equation is: ")	
		for alloc in equation_allocations:
			print("{} * {} * {} * {}".format(alloc.position_manager.price, symbols[alloc.index], alloc.allocation.leverage, alloc.allocation.percent))
			equation += alloc.position_manager.price * symbols[alloc.index] * alloc.allocation.leverage * alloc.allocation.percent

		return equation
