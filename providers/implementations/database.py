import uuid
from enum import Enum as PythonEnum
from sqlalchemy import create_engine, Column, String, Float, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

class SQLAlchemyORM:
    def __init__(self, db_url):
        print(db_url)
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.Base = declarative_base()

        class DebtStatusEnum(PythonEnum):
            started = "started"
            bill_generated = "bill_generated"
            bill_sent = "bill_sent"
            done = "done"
            error = "error"

        class DebtBillsAutomation(self.Base):
            __tablename__ = 'debt_bills_automation'

            debtId = Column(String, primary_key=True, default=str(uuid.uuid4()))
            name = Column(String)
            governmentId = Column(String)
            email = Column(String)
            debtAmount = Column(Float)
            debtDueDate = Column(Date)
            status = Column(Enum(DebtStatusEnum))
            errorMessage = Column(String)

            def __repr__(self):
                return (
                    f"<DebtBillsAutomation(debtID={self.debtID}, "
                    f"name={self.name}, "
                    f"governmentId={self.governmentId}, "
                    f"email={self.email}, "
                    f"debtAmount={self.debtAmount}, "
                    f"debtDueDate={self.debtDueDate}, "
                    f"status={self.status}, "
                    f"errorMessage={self.errorMessage})>"
                )

        self.DebtBillsAutomation = DebtBillsAutomation
        self.__create_tables()
    
    def __create_tables(self) -> None:
        self.Base.metadata.create_all(self.engine)
    
    # SQLAlchemy scoped sessions are thread safe to do db CRUD transactions
    def get_session(self) -> scoped_session:
        return scoped_session(self.Session)