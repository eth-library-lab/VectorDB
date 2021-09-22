from abc import ABC, abstractmethod

class Backend(ABC):
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def get(key):
        raise NotImplementedError
    
    @abstractmethod
    def put(key, value):
        raise NotImplementedError
    
    @abstractmethod
    def list():
        raise NotImplementedError