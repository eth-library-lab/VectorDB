# FaissDB

> An experimental vector storage, built for [AID Project](aid.autoai.org/).


## Installation

* Step 1/2: Install faiss-cpu or faiss-gpu based on your system.

  ```sh
  pip install faiss-cpu
  # or
  pip install faiss-gpu
  ```
* Step 2/2: Install FaissDB
  ```
  pip install faissdb
  ```

It should suffice on Ubuntu/Debian system. 

## Usage


```python
from faissdb.faissdb import FaissDB
from faissdb.config import FaissDBSettings

settings = FaissDBSettings()
db = FaissDB(settings)
# For the first time, create a partition with any name
db.create_partition('voc')

# Create a one-dimensional vector
feature = np.random.random((4096,))
# Put it in database
# here 1.jpg could be any string, that you want to indicate the file
db.put('voc', feature, '1.jpg')
# build the index
db.create_index('voc')

# Now perform KNN Query
# First reshape the feature, such that it becomes (k*d)
# where k is the number of vectors you want to consider
# In our case, we have a single query vector, hence k=1
# d is the dimension of the vectors.
feature = feature.reshape((1, 4096))
D, keys = db.knn_query('voc', feature, k=1)

# Since k=1, we always get the vector itself, hence D should only contains 0.
print(D)
for each in keys:
    value = db.getVal('voc', each)
    # The value should be 1.jpg, or the string you specified above.
    print(value)
```