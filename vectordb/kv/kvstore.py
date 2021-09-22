import json
import hashlib
import numpy as np
from typing import Dict
from numpy.typing import ArrayLike
import faiss
from vectordb.backend.base import Backend
from vectordb.utilities.logger import logger
from .indexer import VectorIndexer
import time
class VStore():
    
    def __init__(self, backend: Backend, digest_size: int = 32) -> None:
        self.backend = backend
        self.digest_size = digest_size
    
    def _hash_vector(self, vector: ArrayLike) -> bytes:
        hash = hashlib.blake2b(vector.tobytes(), digest_size=self.digest_size)
        return str(hash.digest())
    
    def put(self, vector: ArrayLike, value: Dict) -> bytes:
        self.backend.put("key:"+self._hash_vector(vector), vector.tobytes())
        self.backend.put("val:"+self._hash_vector(vector), json.dumps(value))
    
    def get(self, vector: ArrayLike) -> Dict:
        value = self.backend.get("val:" + self._hash_vector(vector))
        return json.loads(value)
    
    def keys(self):
        return self.backend.get_all_keys()
    
    def build_index(self):
        logger.info("Building index...")
        matx = self.keys().astype(np.float32)
        indexer = VectorIndexer()
        self.index = indexer.build_index(matx)
        if self.index.is_trained:
            logger.info("Index is trained. Saving to disk...")
            self.write_index()
    
    def write_index(self):
        chunk = faiss.serialize_index(self.index)
        chunk_bytes = chunk.tobytes()
        current_version = "idx:"+str(int(time.time()))
        self.backend.put(current_version, chunk_bytes)
        self.backend.put("idx:latest", current_version.encode())

    def read_index(self, version=None):
        pass