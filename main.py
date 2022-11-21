from dotenv import load_dotenv
import web3
from config import Config
from core.use_cases.rebalancer import Rebalancer
from core.use_cases.rebalance_executor import RebalanceExecutor
from adapters.smart_contracts.repositories.user_repository import UserRepository
from adapters.smart_contracts.repositories.vault_repository import VaultRepository 
from adapters.smart_contracts.repositories.position_manager_repository import PositionManagerRepository

load_dotenv()

def rebalance():
    w3 = web3.Web3(web3.HTTPProvider("https://arb1.arbitrum.io/rpc"))
    vault_repository = VaultRepository(w3)
    position_manager_repository = PositionManagerRepository(w3)
    user_repository = UserRepository(w3)
    config = Config()

    rebalance_executor = RebalanceExecutor(config, w3, user_repository, vault_repository)
    rebalancer = Rebalancer(config, vault_repository, position_manager_repository, rebalance_executor)
    rebalancer.run()

rebalance()