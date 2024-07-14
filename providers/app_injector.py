from injector import Binder, Injector, Module
from providers.implementations import CustomUvicornLogger, EnvironmentHandler
from providers.interfaces import ICustomUvicornLogger, IEnvironmentHandler

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

injector_container = Injector(AppModule())