import os
import numpy as np
from vectordb.kv import VStore
from vectordb.backend.redis import RedisBackend

redis_backend = RedisBackend(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    username=os.environ.get('REDIS_USER'),
    password=os.environ.get('REDIS_PASSWORD')
)

vstore = VStore(backend=redis_backend)

feature = np.random.random((4096,))
val_data = {
    "filename":"2.jpg"
}

# vstore.put(feature, val_data)
# vstore.build_index()
# vstore.write_index()
keys = vstore.keys()
query_key = feature
query_key = query_key.reshape((1, 4096))
# vstore.read_index()
D, keys = vstore.knn_search(query_key, k=10)
for each in keys:
    value = vstore.get(each)
    print(value)