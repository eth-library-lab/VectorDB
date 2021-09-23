from abc import ABC, abstractmethod

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