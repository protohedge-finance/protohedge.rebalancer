from core.models.allocation import Allocation

def to_allocation_model(allocation_dto) -> Allocation:
	(percent, token, symbol, leverage, position_type) = allocation_dto
	return Allocation(percent, token, symbol, leverage, position_type)

def to_allocation_models(allocation_dtos) -> list[Allocation]:
	return list(map(lambda d: to_allocation_model(allocation_dtos)))

