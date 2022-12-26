import os

class Config:
    def __init__(self):
        self.vault_address: str = os.getenv("VAULT_ADDRESS")
        self.private_key: str = os.getenv("PRIVATE_KEY")
        self.user_address: str = os.getenv("USER_ADDRESS")
        self.rpc_url: str = os.getenv("RPC_URL")
        self.redis_host: str = os.getenv("REDIS_HOST")
        self.redis_port: int = int(os.getenv("REDIS_PORT"))
        self.redis_password: str = os.getenv("REDIS_PASSWORD")
        self.redis_ssl: bool = bool(os.getenv("REDIS_SSL"))
