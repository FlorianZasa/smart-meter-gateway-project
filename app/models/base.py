from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass