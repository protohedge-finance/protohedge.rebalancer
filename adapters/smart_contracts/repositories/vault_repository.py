import os
import json
from adapters.smart_contracts.mappings.position_manager_mapping import to_position_manager_model
from core.models.position_manager import PositionManager
from core.models.rebalance_queue_data import RebalanceQueueData
from core.models.vault import Vault
from adapters.smart_contracts.dto.rebalance_dto import RebalanceRequestDto
from config import Config

vault_abi = json.load(open("adapters/smart_contracts/abi/protohedge_vault.json"))

class VaultRepository:
	def __init__(self, w3, config: Config):
		self.w3 = w3
		self.config: Config = config

	def get_vault(self, vault_address: str):
		vault_contract = self.w3.eth.contract(address=vault_address, abi=vault_abi)
		name = vault_contract.functions.vaultName().call()
		worth = vault_contract.functions.vaultWorth().call()
		cost_basis = vault_contract.functions.vaultCostBasis().call()	
		amount_to_rebalance = vault_contract.functions.amountToRebalance().call()
		available_liquidity = vault_contract.functions.getAvailableLiquidity().call()

		return Vault(name, worth, cost_basis, amount_to_rebalance, available_liquidity)

	def get_position_manager_addresses(self, vault_address: str) -> list[str]: 
		vault_contract = self.w3.eth.contract(address=vault_address, abi=vault_abi)
		position_manager_addresses = vault_contract.functions.getPositionManagers().call()
		return position_manager_addresses
	
	def rebalance(self, vault_address: str, request_payload: list[RebalanceQueueData], nonce: int):
		vault_contract = self.w3.eth.contract(address=vault_address, abi=vault_abi)
		tx = vault_contract.functions.rebalance(request_payload).build_transaction({"nonce": nonce})
		signed = self.w3.eth.account.sign_transaction(tx, private_key=self.config.private_key)
		self.w3.eth.send_raw_transaction(signed.rawTransaction)
		return tx

	def should_rebalance(self, vault_address: str, request_payload: list[RebalanceQueueData]) -> tuple[bool, str]:
		vault_contract = self.w3.eth.contract(address=vault_address, abi=vault_abi)
		return vault_contract.functions.shouldRebalance(request_payload).call()


 	

		
			
		
	
	
