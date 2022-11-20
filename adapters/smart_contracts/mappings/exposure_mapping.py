from core.models.exposure import Exposure 

def to_exposure_model(exposure_dto) -> Exposure:
	(amount, token, symbol) = exposure_dto
	return Exposure(amount, token, symbol)

def to_exposure_models(exposure_dtos) -> list[Exposure]:
	return list(map(lambda d: to_exposure_model(d)))