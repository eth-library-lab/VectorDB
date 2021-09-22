import redis
from .base import Backend
import numpy as np
class RedisBackend(Backend):
    def __init__(self, host: str, port: int, db: int=0, ssl:bool=False, ssl_ca_certs:str="", password=None, username=None) -> None:
        super().__init__()
        self.client = redis.Redis(host=host, port=port, db=db, password=password, ssl=ssl, ssl_ca_certs=ssl_ca_certs, username=username)

    def get(self, key: str) -> bytes:
        return self.client.get(key)
    
    def put(self, key: str, value: bytes) -> None:
        self.client.set(key, value)
    
    def delete(self, key: str) -> None:
        self.client.delete(key)
    
    def get_all_keys(self):
        values = []
        for key in self.client.scan_iter():
            if key.startswith(b"key:"):
                values.append(np.frombuffer(self.client.get(key)))
        return np.array(values)