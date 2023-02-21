import os
from dotenv import load_dotenv
from redis import Redis
import web3
from adapters.smart_contracts.repositories.stats_repository import StatsRepository
from config import Config
from core.use_cases.rebalancer import Rebalancer
from core.use_cases.rebalance_executor import RebalanceExecutor
from adapters.smart_contracts.repositories.user_repository import UserRepository
from adapters.smart_contracts.repositories.vault_repository import VaultRepository 
from adapters.smart_contracts.repositories.position_manager_repository import PositionManagerRepository


def rebalance(event, context):
    env_file = os.getenv("ENV_FILE") 
    env_file = ".env.{}".format(env_file) if env_file else ".env"
    
    load_dotenv(dotenv_path=env_file)

    config = Config()
    w3 = web3.Web3(web3.HTTPProvider(config.rpc_url))
    redis = Redis(host=config.redis_host, port=config.redis_port, password=config.redis_password, ssl=config.redis_ssl, db=0, ssl_cert_reqs=None)
    vault_repository = VaultRepository(w3, config)
    position_manager_repository = PositionManagerRepository(w3)
    user_repository = UserRepository(w3)
    stats_repository = StatsRepository(redis)

    rebalance_executor = RebalanceExecutor(config, w3, user_repository, vault_repository)
    rebalancer = Rebalancer(config, vault_repository, position_manager_repository, rebalance_executor, stats_repository)
    rebalancer.run()
