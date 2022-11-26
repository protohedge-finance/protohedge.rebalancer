import json
import jsonpickle
from adapters.smart_contracts.dto.rebalance_dto import RebalanceRequestDto
from adapters.smart_contracts.repositories.user_repository import UserRepository
from adapters.smart_contracts.repositories.vault_repository import VaultRepository
from core.models.position_manager import PositionManager
from config import Config

class RebalanceExecutor():
	def __init__(self, config: Config, w3, user_repository: UserRepository, vault_repository: VaultRepository):
		self.config: Config = config
		self.w3 = w3
		self.user_repository: UserRepository = user_repository
		self.vault_repository: VaultRepository = vault_repository

	def execute_rebalance(self, equation_result, position_managers: list[PositionManager]):
		print(equation_result)
		request_payload = []

		for (index, position_manager) in enumerate(position_managers):
			usdc_amount = self.calculate_usdc_amount(equation_result, position_manager, index)
			request_payload.append({"positionManager": position_manager.address, "usdcAmountToHave": usdc_amount})	

		nonce = self.user_repository.get_transaction_count(self.config.user_address)
		tx = self.vault_repository.rebalance(self.config.vault_address, request_payload, nonce)
		print(tx)

	def calculate_usdc_amount(self, equation_result, position_manager: PositionManager, index: int) -> int:
		return int(equation_result[index]) * position_manager.price
	