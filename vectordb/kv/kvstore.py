from ctypes import Array
import json
import time
import faiss
import hashlib
import numpy as np
import msgpack
import msgpack_numpy as msgpack_np
from numpy.typing import ArrayLike
from typing import Dict

from vectordb.backend.base import Backend
from vectordb.utilities.logger import logger
from .indexer import VectorIndexer

class VStore():
    def __init__(self, backend: Backend, digest_size: int = 32) -> None:
        self.backend = backend
        self.digest_size = digest_size
        self.index = None
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
    
    @property
    def np_index(self):
        return faiss.serialize_index(self.index)

    def write_index(self):
        encoded_idx = msgpack.packb(self.np_index, default=msgpack_np.encode)
        current_version = "idx:"+str(int(time.time()))
        self.backend.put(current_version, encoded_idx)
        self.backend.put("idx:latest", current_version.encode())

    def read_index(self, version=None):
        if version is None:
            version = self.backend.get("idx:latest")
            if version is not None:
                version = version.decode()

        index = msgpack.unpackb(self.backend.get(version),object_hook=msgpack_np.decode)
        self.index = faiss.deserialize_index(index)
    
    def knn_search(self, key: ArrayLike, k: int=1):
        if not self.index:
            self.read_index()
            if not self.index:
                self.build_index()
        key = key.astype(np.float32)
        D, I = self.index.search(key, k)
        matx = self.keys()
        key_vectors = matx[I].reshape(k, -1)
        return D, key_vectors