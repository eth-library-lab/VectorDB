import os
import numpy as np
from mlpm_client import Client
import ast

from src.faissdb import FaissDB
from src.config import FaissDBSettings

c = Client('http://127.0.0.1')

BASE_PATH="/home/username/Documents/voc-slim"

settings = FaissDBSettings()
db = FaissDB(settings)
files = os.listdir(BASE_PATH)
# training...
'''


db.create_partition('voc')

for each in files:
    if each.endswith('.jpg'):
        with open(os.path.join(BASE_PATH, each), 'rb') as file:
            r = c.create_requests('aidmodels','image_encoding','encodingSolver', {'file': file})
            result = r.do()
            feature = result.json()["feature"]
            feature = ast.literal_eval(feature)
            feature = np.array(feature)
            db.put('voc', feature, os.path.join(BASE_PATH, each))

db.create_index('voc')
'''

# testing...

file = files[24]

with open(os.path.join(BASE_PATH, file), 'rb') as file:
    r = c.create_requests('aidmodels','image_encoding','encodingSolver', {'file': file})
    result = r.do()
    feature = result.json()["feature"]
    feature = result.json()["feature"]
    feature = ast.literal_eval(feature)
    feature = np.array(feature)
    feature = feature.reshape(1, 4096)
    D, I = db.knn_query('voc', feature, k=10)
    print(D)
    print(I)