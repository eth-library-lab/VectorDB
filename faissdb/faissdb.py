# FAISSDB

import json
import os
from typing import Dict

from faiss.swigfaiss import read_index, write_index
from numpy.typing import ArrayLike

from .config import FaissDBSettings
from .faisskv import FaissKV
from .utility import create_folder_if_not_exists, logger


class FaissDB():
    def __init__(self, settings: FaissDBSettings) -> None:
        self.settings = settings
        self.partitions: Dict = {}
        self.dbs: Dict = {}
        # check if the base_dir exists, and if everything else is there.
        # if not, create it.
        create_folder_if_not_exists(self.settings.base_dir, 'data')
        self.read_partitions()

    def create_partition(self, partition_name: str):
        dbpath = os.path.join(self.settings.base_dir, 'data', partition_name)
        if not partition_name in self.partitions:
            create_folder_if_not_exists(dbpath)
            faisskv = FaissKV(dbpath)
            self.partitions[partition_name] = {
                'dbpath': dbpath,
            }
            self.write_partitions()

    def write_partitions(self):
        # write the partitions information into partitions.json under base_dir
        with open(os.path.join(self.settings.base_dir, 'partitions.json'),
                  'w') as f:
            json.dump(self.partitions, f)

    def read_partitions(self):
        if os.path.exists(
                os.path.join(self.settings.base_dir, 'partitions.json')):
            with open(os.path.join(self.settings.base_dir, 'partitions.json'),
                      'r') as f:
                self.partitions = json.load(f)
                for dbname in self.partitions:
                    dbpath = self.partitions[dbname]['dbpath']
                    self.dbs[dbname] = FaissKV(dbpath)
            logger.info("Successfully read partition.json")
        else:
            logger.info("partition.json does not exist")

    def get_partition_db(self, partition_name: str) -> FaissKV:
        if partition_name in self.dbs:
            return self.dbs[partition_name]
        if partition_name in self.partitions:
            dbpath = self.partitions[partition_name]['dbpath']
            return FaissKV(dbpath)
        else:
            logger.error("Partition {} does not exist".format(partition_name))
            raise ValueError(
                "Partition {} does not exist".format(partition_name))

    def put(self, partition_name: str, key: ArrayLike, value: bytes):
        db = self.get_partition_db(partition_name)
        db.put(key, value)

    def getVec(self, partition_name: str, key: bytes):
        db = self.get_partition_db(partition_name)
        return db.getVector(key)

    def getVal(self, partition_name: str, key: bytes):
        db = self.get_partition_db(partition_name)
        return db.getValue(key).decode("utf-8")

    def create_index(self, partition_name: str):
        db = self.get_partition_db(partition_name)
        db.build_index()

    def knn_query(self, partition_name: str, key: ArrayLike, k: int):
        db = self.get_partition_db(partition_name)
        return db.knn_query(key, k)
