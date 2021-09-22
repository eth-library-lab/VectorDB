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

vstore.put(feature, val_data)

print(vstore.get(feature))

keys = vstore.keys()

print(keys.shape)