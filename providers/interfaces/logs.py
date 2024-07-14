from abc import ABC, abstractmethod
from enum import Enum

class IServicesEnum(Enum):
    AUTHENTICATION = "authentication"
    PROCESS_FILE = "process_file"
    SYSTEM = "system"

class ICustomUvicornLogger(ABC):
    @abstractmethod
    def get_logger(self, service: IServicesEnum, operation_id: str):
        pass