from core.models.position_manager import PositionManager 
from adapters.smart_contracts.mappings.allocation_mapping import to_allocation_models
from adapters.smart_contracts.mappings.exposure_mapping import to_exposure_models 

def to_position_manager_model(name: str, address: str, position_worth: int, cost_basis: int, pnl: int, exposures: list, allocation: list, price: int, collateral_ratio: int) -> PositionManager:
	exposures = to_exposure_models(exposures)
	allocations = to_allocation_models(allocation)

	return PositionManager(name, address, position_worth, cost_basis, pnl, exposures, allocations, price, collateral_ratio)


	