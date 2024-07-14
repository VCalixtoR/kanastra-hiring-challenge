from injector import Binder, Injector, Module
from .implementations import CustomUvicornLogger, EnvironmentHandler, SQLAlchemyORM
from .interfaces import ICustomUvicornLogger, IEnvironmentHandler, ISQLAlchemyORM

class AppModule(Module):
    def configure(self, binder: Binder):
        env_handler = EnvironmentHandler()
        binder.bind(IEnvironmentHandler, to=EnvironmentHandler)
        binder.bind(
            ICustomUvicornLogger,
            to=CustomUvicornLogger(
                app=env_handler.getenv("APP"), environment=env_handler.getenv("ENVIRONMENT")
            )
        )
        binder.bind(
            ISQLAlchemyORM,
            to=SQLAlchemyORM(
                db_url=env_handler.getenv("DB_CONN_STRING")
            )
        )

injector_container = Injector(AppModule())