import numpy as np
from src.config import FaissDBSettings
from src.faissdb import FaissDB

settings = FaissDBSettings()
db = FaissDB(settings)
key = np.array([1.,2.,3.,4.])
# db.put('test', key, 'val2')

print(db.getVec('test', key))
print(db.getVal('test', key))

key = key.reshape((1, 4))
D,I= db.knn_query('test', key, k=1)
print(D)
print(I)