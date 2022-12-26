from adapters.smart_contracts.dto.rebalance_dto import RebalanceRequestDto
from adapters.smart_contracts.repositories.user_repository import UserRepository
from adapters.smart_contracts.repositories.vault_repository import VaultRepository
from core.models.position_manager import PositionManager
from config import Config
from core.constants import USDC_MULTIPLIER
from core.models.rebalance_queue_data import RebalanceQueueData

class RebalanceExecutor():
	def __init__(self, config: Config, w3, user_repository: UserRepository, vault_repository: VaultRepository):
		self.config: Config = config
		self.w3 = w3
		self.user_repository: UserRepository = user_repository
		self.vault_repository: VaultRepository = vault_repository

	def execute_rebalance(self, request_payload: list[RebalanceQueueData]) -> list[RebalanceQueueData]:
		nonce = self.user_repository.get_transaction_count(self.config.user_address)
		tx = self.vault_repository.rebalance(self.config.vault_address, request_payload, nonce)
		print(tx)

		return request_payload

	def calculate_usdc_amount(self, equation_result, position_manager: PositionManager, index: int) -> int:
		print(equation_result[index] * position_manager.price / USDC_MULTIPLIER)
		return int(equation_result[index] * position_manager.price / USDC_MULTIPLIER)

	def generate_request_payload(self, position_managers: list[PositionManager], equation_result) -> list[RebalanceQueueData]:
		request_payload = []

		for (index, position_manager) in enumerate(position_managers):
			usdc_amount = self.calculate_usdc_amount(equation_result, position_manager, index)
			request_payload.append({"positionManager": position_manager.address, "usdcAmountToHave": usdc_amount})	

		return request_payload
		

	def should_execute(self, request_payload: list[RebalanceQueueData]) -> tuple[bool, str]:
		return self.vault_repository.should_rebalance(self.config.vault_address, request_payload)
		
	
