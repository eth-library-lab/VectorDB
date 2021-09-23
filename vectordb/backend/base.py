from abc import ABC, abstractmethod
from enum import Enum
class KeyType(str, Enum):
    KEY = "key"
    VAL = "val"
    IDX = "idx"

class Backend(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def get(key: str):
        raise NotImplementedError
    
    @abstractmethod
    def put(key: str, value: bytes):
        raise NotImplementedError
    
    @abstractmethod
    def get_all_keys():
        raise NotImplementedError
    
    @abstractmethod
    def delete(key: str):
        raise NotImplementedError
    
    @abstractmethod
    def clear(type: str):
        raise NotImplementedError