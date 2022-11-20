import os
import json
from adapters.smart_contracts.mappings.position_manager_mapping import to_position_manager_model
from core.models.position_manager import PositionManager
from adapters.smart_contracts.dto.rebalance_dto import RebalanceRequestDto

vault_abi = json.load(open("adapters/smart_contracts/abi/protohedge_vault.json"))

class VaultRepository:
	def __init__(self, w3):
		self.w3 = w3

	def get_position_manager_addresses(self, vaultAddress: str) -> list[str]: 
		vault_contract = self.w3.eth.contract(address=vaultAddress, abi=vault_abi)
		position_manager_addresses = vault_contract.functions.getPositionManagers().call()
		return position_manager_addresses
	
	def rebalance(self, vaultAddress: str, request_payload: list[RebalanceRequestDto], nonce: int):
		vault_contract = self.w3.eth.contract(address=vaultAddress, abi=vault_abi)
		tx = vault_contract.functions.rebalance(json.dumps(request_payload)).build_transaction({"nonce": nonce})
		signed = self.w3.eth.account.sign_transaction(tx, private_key=os.getenv("PERSONAL_PRIVATE_KEY"))
		self.w3.eth.send_raw_transaction(signed.rawTransaction)
		return tx

 	

		
			
		
	
	