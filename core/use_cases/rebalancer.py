from config import Config
from adapters.smart_contracts.repositories.vault_repository import VaultRepository
from adapters.smart_contracts.repositories.position_manager_repository import PositionManagerRepository 
from core.use_cases.equations_solver import EquationsSolver
from core.use_cases.rebalance_executor import RebalanceExecutor

class Rebalancer:
	def __init__(self, config: Config, vault_repository: VaultRepository, position_manager_repository: PositionManagerRepository, rebalance_executor: RebalanceExecutor):
		self.config: Config = config
		self.vault_repository: VaultRepository = vault_repository
		self.position_manager_repository: PositionManagerRepository = position_manager_repository
		self.rebalance_executor: RebalanceExecutor = rebalance_executor
	def run(self):
		vault = self.vault_repository.get_vault(self.config.vault_address)
		position_manager_addresses = self.vault_repository.get_position_manager_addresses(self.config.vault_address)
		position_managers = self.position_manager_repository.get_position_managers(position_manager_addresses)

		equation_solver = EquationsSolver(vault, position_managers)
		equation_result = equation_solver.calculate_equations()
		print("Equation result was {}".format(equation_result))
		tx = self.rebalance_executor.execute_rebalance(equation_result, position_managers)
		print("Successfully rebalanced!")
		print("tx: {}".format(tx))
		
		
