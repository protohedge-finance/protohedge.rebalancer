from core.models.allocation import Allocation

def to_allocation_model(allocation_dto) -> Allocation:
	(percent, token, symbol, leverage, position_type, collateral_ratio) = allocation_dto
	return Allocation(percent, token, symbol, leverage, position_type, collateral_ratio)

def to_allocation_models(allocation_dtos) -> list[Allocation]:
	return list(map(lambda d: to_allocation_model(d), allocation_dtos))

