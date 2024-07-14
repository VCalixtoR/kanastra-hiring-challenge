from abc import ABC, abstractmethod

class IEnvironmentHandler(ABC):
    @abstractmethod
    def getenv(self, env_key: str):
        pass