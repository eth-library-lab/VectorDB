# FAISSDB

import os
import json

import plyvel
from config import FaissDBSettings
from typing import List, Dict

class FaissDB():

    def __init__(self, settings:FaissDBSettings) -> None:
        self.settings = settings
        self.partitions:List[Dict] = []
        # check if the base_dir exists, and if everything else is there.
        # if not, create it.
        if not os.path.exists(self.settings.base_dir):
            os.mkdir(self.settings.base_dir)
        self.read_partitions()

    def create_partition(self, partition_name: str):
        db = plyvel.DB(os.path.join(self.settings.base_dir, partition_name), create_if_missing=True)
        self.partitions.append({partition_name: db})
        self.write_partitions()

    def write_partitions(self):
        # write the partitions information into partitions.json under base_dir
        with open(os.path.join(self.settings.base_dir, 'partitions.json'), 'w') as f:
            json.dump(self.partitions, f)

    def read_partitions(self):
        if os.path.exists(os.path.join(self.settings.base_dir, 'partitions.json')):
            with open(os.path.join(self.settings.base_dir, 'partitions.json'), 'r') as f:
                self.partitions = json.load(f)
    
    def get_partition_db(self,partition_name:str)-> plyvel.DB:
        if partition_name in self.partitions:
            return self.partitions[partition_name]
        else:
            return None

    def put(self, partition_name: str, key: bytes, value: bytes):
        db = self.get_partition_db(partition_name)
        db.put(key, value)
    
    def get(self, partition_name: str, key: bytes):
        db = self.get_partition_db(partition_name)
        return db.get(key)