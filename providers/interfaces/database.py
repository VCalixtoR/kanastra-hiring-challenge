from abc import ABC, abstractmethod
from sqlalchemy.orm import scoped_session

class ISQLAlchemyORM:
    @abstractmethod
    def get_session(self) -> scoped_session:
        pass