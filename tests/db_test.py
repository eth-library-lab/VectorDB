import unittest

import numpy as np

from src.config import FaissDBSettings
from src.faissdb import FaissDB


class TestFaissDB(unittest.TestCase):
    def test_get_put_val(self):
        settings = FaissDBSettings()
        db = FaissDB(settings)
        db.create_partition('test')
        val_input = "val1"
        x = np.array([1., 2., 3., 4.])
        db.put('test', x, "val1")
        val_get = db.getVal('test', x)
        self.assertEqual(val_input, val_get)

if __name__ == '__main__':
    unittest.main()
