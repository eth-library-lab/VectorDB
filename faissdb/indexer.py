import faiss
from numpy.typing import ArrayLike


class VectorIndexer(object):
    def __init__(self) -> None:
        super().__init__()

    def build_index(self, matrix: ArrayLike):
        n, d = matrix.shape[0], matrix.shape[1]
        index = faiss.IndexFlatL2(d)
        index.add(matrix)
        return index
