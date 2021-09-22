import hashlib
from numpy.typing import ArrayLike
from backend.base import Backend
from typing import Dict

class VStore():
    
    def __init__(self, backend: Backend, digest_size: int = 32) -> None:
        self.backend = backend
    
    def _hash_vector(self, vector: ArrayLike) -> bytes:
        hash = hashlib.blake2b(vector.tobytes(), digest_size=self.digest_size)
        return hash.digest()
    
    def put(self, vector: ArrayLike, value: Dict) -> bytes:
        pass