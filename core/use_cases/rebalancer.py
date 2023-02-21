from adapters.smart_contracts.repositories.stats_repository import StatsRepository
from config import Config
from adapters.smart_contracts.repositories.vault_repository import VaultRepository
from adapters.smart_contracts.repositories.position_manager_repository import PositionManagerRepository
from core.models.rebalance_queue_data import RebalanceQueueData
from core.models.vault import Vault 
from core.use_cases.equations_solver import EquationsSolver
from core.use_cases.rebalance_executor import RebalanceExecutor

class Rebalancer:
	def __init__(self, config: Config, vault_repository: VaultRepository, position_manager_repository: PositionManagerRepository, rebalance_executor: RebalanceExecutor, stats_repository: StatsRepository):
		self.config: Config = config
		self.vault_repository: VaultRepository = vault_repository
		self.position_manager_repository: PositionManagerRepository = position_manager_repository
		self.stats_repository: StatsRepository = stats_repository
		self.rebalance_executor: RebalanceExecutor = rebalance_executor
	def run(self):
		vault = self.vault_repository.get_vault(self.config.vault_address)
		position_manager_addresses = self.vault_repository.get_position_manager_addresses(self.config.vault_address)
		position_managers = self.position_manager_repository.get_position_managers(position_manager_addresses)
		
		equation_solver = EquationsSolver(vault, position_managers)
		equation_result = equation_solver.calculate_equations()
		rebalance_data = self.rebalance_executor.generate_request_payload(position_managers, equation_result)
		print("Rebalance Data")
		print(rebalance_data)
		should_rebalance, error_message = self.rebalance_executor.should_execute(rebalance_data)

		print("should I rebalance?")
		print(should_rebalance)

		if not should_rebalance:
			print("Error message: {}".format(error_message));
			outcome = "Rebalance did not happen. Error message: {}".format(error_message)
			self.stats_repository.add_rebalance_history(self.config.vault_address, outcome)			
			return

		print("Equation result was {}".format(equation_result))
		tx = self.rebalance_executor.execute_rebalance(rebalance_data)
		outcome = "Successfully rebalanced!"
		self.stats_repository.add_rebalance_history(self.config.vault_address, outcome)
		print("tx: {}".format(tx))

