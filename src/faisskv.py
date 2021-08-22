import hashlib
import os

import numpy as np
import plyvel
from faiss.swigfaiss import read_index, write_index
from numpy.typing import ArrayLike

from .indexer import VectorIndexer
from .utility import logger
'''
FaissKV manages two DBs, for a single vector->value pair
hash(vector) -> vector (vecKV)
hash(vector) -> value  (valKV)
'''


class FaissKV():
    def __init__(self, db_path: str, digest_size: int = 32):
        self.db_path = db_path
        self.digest_size = digest_size
        self.index = None

        self.vecKV = plyvel.DB(os.path.join(self.db_path, 'vecKV'),
                               create_if_missing=True)
        self.valKV = plyvel.DB(os.path.join(self.db_path, 'valKV'),
                               create_if_missing=True)
        self.read_index()

    def _hash_vector(self, vector: ArrayLike) -> bytes:
        hash = hashlib.blake2b(vector.tobytes(), digest_size=self.digest_size)
        return hash.digest()

    def put(self, vector: ArrayLike, value: str):
        self.vecKV.put(self._hash_vector(vector), vector.tobytes())
        self.valKV.put(self._hash_vector(vector), str.encode(value))

    def getVector(self, key: ArrayLike):
        buffer = self.vecKV.get(self._hash_vector(key))
        return np.frombuffer(buffer)

    def getValue(self, key: bytes):
        return self.valKV.get(self._hash_vector(key))

    def get_all_vectors(self) -> ArrayLike:
        # TODO: allocate memory before iterating
        # that would require statsitic information, at least the length of the database
        matrix = []
        with self.vecKV.iterator() as iter:
            for k, v in iter:
                matrix.append(np.frombuffer(v))
        return np.array(matrix)

    def yield_all(self):
        with self.vecKV.iterator() as iter:
            for k, v in iter:
                yield (k)
                
    def build_index(self):
        logger.info("Building index...")
        matx = self.get_all_vectors().astype(np.float32)
        indexer = VectorIndexer()
        self.index = indexer.build_index(matx)
        if self.index.is_trained:
            logger.info("Index is trained. Saving to disk...")
            self.write_index()

    def write_index(self):
        if self.index:
            if self.index.is_trained:
                write_index(self.index, os.path.join(self.db_path, 'db.index'))

    def read_index(self):
        index_file = os.path.join(self.db_path, 'db.index')
        if os.path.exists(index_file):
            logger.info("Reading index...")
            self.index = read_index(index_file)

    def knn_query(self, key: ArrayLike, k: int = 1):
        if not self.index:
            self.build_index()
        key = key.astype(np.float32)
        D, I = self.index.search(key, k)
        matx = self.get_all_vectors()
        key_vectors = matx[I].reshape(k, -1)
        return D, key_vectors