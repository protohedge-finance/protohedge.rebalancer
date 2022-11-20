import sympy
from core.models.position_type import PositionType
from core.models.position_manager import PositionManager
from core.models.equation_allocation import EquationAllocation
from core.models.equation_positions import EquationPositions
from core.use_cases.equation import Equation


class EquationsSolver:
	def __init__(self, position_managers: list[PositionManager]):
		self.position_managers = position_managers

	def calculate_equations(self):
		equation_data = self.create_equation_data()
		self.symbols = sympy.symbols(" ".join(self.names)) 
		self.names = list(map(lambda p: p.name))
		equations: list[sympy.Eq] = []

		for token in self.equation_data:
			if len(self.equation_data[token][PositionType.Long]) == 0 or len(self.equation_data[token][PositionType.Short]) == 0:
				continue
			
			longs = equation_data[token][PositionType.Long]
			shorts = equation_data[token][PositionType.Long]
			long_equation = Equation(longs, self.symbols).create()
			short_equation = Equation(shorts, self.symbols).create()

			equations.append(sympy.Eq(long_equation, short_equation))

		equations.append(self.create_liquidity_equation())
		return self.execute_equations() 

	def create_equation_data(self) -> dict[str, EquationPositions]:
		equation_data = {}

		for (index, position_manager) in enumerate(self.position_managers):
			equation_data = self.process_allocations(position_manager, index, equation_data)

		return equation_data

	def process_allocations(self, position_manager: list[PositionManager], index: int, equation_data) -> dict[str, EquationPositions]:
		for allocation in position_manager.allocations:
			if allocation.symbol not in self.equation_data:
				self.equation_data[allocation.symbol] = EquationPositions()

			equation_allocation = EquationAllocation(position_manager, allocation, index)
			self.equation_data[allocation.symbol].add_position(allocation.position_type, equation_allocation)

		return equation_data


	def create_liquidity_equation(self):
		liquidity_equation = 0
		for (index, position_manager) in enumerate(self.position_managers):
			liquidity_equation += (position_manager.price * self.symbols[index])

		return sympy.Eq(liquidity_equation, 1000)

	def execute_equations(self, equations: list[sympy.Eq]):
		try:
			return list(sympy.linsolve(equations, self.symbols))[0]
		except IndexError:
			print('This equation has no solutions.')	