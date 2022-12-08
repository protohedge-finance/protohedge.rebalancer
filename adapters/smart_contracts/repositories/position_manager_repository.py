import json
from core.models.position_manager import PositionManager
from adapters.smart_contracts.mappings.position_manager_mapping import to_position_manager_model

position_manager_abi = json.load(open("adapters/smart_contracts/abi/position_manager.json"))

class PositionManagerRepository:
	def __init__(self, w3):
		self.w3 = w3

	def get_position_manager(self, address: str) -> PositionManager:
		print("address is", address)
		position_manager_contract = self.w3.eth.contract(address=address, abi=position_manager_abi)
		name = position_manager_contract.functions.name().call()
		position_worth = position_manager_contract.functions.positionWorth().call()
		cost_basis = position_manager_contract.functions.costBasis().call()
		pnl = position_manager_contract.functions.pnl().call()
		exposures = position_manager_contract.functions.exposures().call()
		allocations = position_manager_contract.functions.allocations().call()
		collateralRatio = position_manager_contract.functions.collateralRatio().call()
		price = position_manager_contract.functions.price().call()

		return to_position_manager_model(name, address, position_worth, cost_basis, pnl, exposures, allocations, price, collateralRatio)	


	def get_position_managers(self, addresses: list[str]) -> list[PositionManager]:
		return list(map(lambda a: self.get_position_manager(a), addresses))
