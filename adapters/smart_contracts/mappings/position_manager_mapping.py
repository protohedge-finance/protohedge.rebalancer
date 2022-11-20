from core.models.position_manager import PositionManager 
from adapters.smart_contracts.mappings.allocation_mapping import to_allocation_models
from adapters.smart_contracts.mappings.exposure_mapping import to_exposure_models 

def to_position_manager_model(position_manager_dto) -> PositionManager:
	(name, address, position_worth, cost_basis, pnl, token_exposures, token_allocation, price) = position_manager_dto

	allocations = to_allocation_models(token_allocation)
	exposures = to_exposure_models(token_exposures)

	return PositionManager(name, address, position_worth, cost_basis, pnl, allocations, exposures, price)


	