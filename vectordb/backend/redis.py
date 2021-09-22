import redis
from vectordb.backend.base import Backend

class RedisBackend(Backend):
    def __init__(self, host: str, port: int, db: int=0, ssl:bool=False, ssl_ca_certs:str="") -> None:
        super().__init__()
        self.client = redis.Redis(host, port, db, ssl, ssl_ca_certs)
    
    def get(self, key: str) -> bytes:
        return self.client.get(key)
    
    def set(self, key: str, value: str) -> None:
        self.client.set(key, value)
    
    def delete(self, key: str) -> None:
        self.client.delete(key)
    
    def get_all_values(self):
        values = []
        for key in self.client.scan_iter():
            values.append(self.client.get(key))