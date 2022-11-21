import json
from core.models.position_manager import PositionManager

class RebalanceRequestDto(object):
	def __init__(self, position_manager: PositionManager, usdcAmount: int):
		self.positionManager: str = position_manager.address
		self.usdcAmountToHave: int = usdcAmount
		