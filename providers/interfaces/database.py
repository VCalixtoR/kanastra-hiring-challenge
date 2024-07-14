from abc import ABC, abstractmethod

class ISQLAlchemyORM:
    @abstractmethod
    def get_session(self):
        pass