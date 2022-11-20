import json
from core.models.position_manager import PositionManager
from adapters.smart_contracts.mappings.position_manager_mapping import to_position_manager_model

position_manager_abi = json.load(open("adapters/smart_contracts/abi/position_manager.json"))

class PositionManagerRepository:
	def __init__(self, w3):
		self.w3 = w3

	def get_position_manager(self, address: str) -> PositionManager:
		position_manager_contract = self.w3.eth.contract(address=address, abi=position_manager_abi)
		print("address is")
		print(address)
		position_manager_dto = position_manager_contract.functions.stats().call()
		return to_position_manager_model(position_manager_dto)	


	def get_position_managers(self, addresses: list[str]) -> list[PositionManager]:
		return list(map(lambda a: self.get_position_manager(a), addresses))
