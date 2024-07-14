import logging
import sys
import uvicorn.logging
from providers.interfaces import ICustomUvicornLogger, IServicesEnum
from injector import inject

class CustomUvicornLoggerConfig(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        if extra == None:
            extra = {}
        extra.setdefault('app', self.app)
        extra.setdefault('environment', self.environment)
        extra.setdefault('service', self.service)
        extra.setdefault('operation_id', self.operation_id)
        super()._log(level, msg, args, exc_info, extra, stack_info, **kwargs)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        rv = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        rv.app = self.app
        rv.environment = self.environment
        rv.service = self.service
        rv.operation_id = self.operation_id
        return rv

class CustomUvicornLogger(ICustomUvicornLogger):

    @inject
    def __init__(self, app: str, environment: str):
        self.app = app
        self.environment = environment

    def get_logger(self, service: IServicesEnum = IServicesEnum.SYSTEM, operation_id: str = "BaseLogger") -> CustomUvicornLoggerConfig:
        logger = CustomUvicornLoggerConfig("uvicorn.access")
        logger.app = self.app
        logger.environment = self.environment
        logger.service = service.value
        logger.operation_id = operation_id

        # Check if stdout is a terminal, if it is, use colorized prefix
        if sys.stdout.isatty():
            console_formatter = uvicorn.logging.ColourizedFormatter(
                "{levelprefix} {app} {environment} {service} {operation_id} {message}",
                style="{", use_colors=True)
        else:
            console_formatter = logging.Formatter(
                "{levelname} {app} {environment} {service} {operation_id} {message}",
                style="{"
            )

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(console_formatter)
        logger.addHandler(stream_handler)

        return logger