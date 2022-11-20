from core.models.position_manager import PositionManager

class RebalanceRequestDto:
	def __init__(self, position_manager: PositionManager, usdcAmount: int):
		self.positionManager: PositionManager = position_manager.address
		self.usdcAmountToHave: int = usdcAmount
		