from providers import injector_container, ICustomUvicornLogger, IEnvironmentHandler, IServicesEnum

REQUEST_TIMEOUT_SECONDS = 60

class ProcessFile:

    def __init__(self):
        self.env_handler: IEnvironmentHandler = injector_container.get(IEnvironmentHandler)
        self.custom_uvicorn_logger: ICustomUvicornLogger = injector_container.get(ICustomUvicornLogger)
                
    async def execute(self):

        operation_logger = self.custom_uvicorn_logger.get_logger(IServicesEnum.PROCESS_FILE, "test_id")

        try:
            print("Doing some testes")
            
            print(self.env_handler.getenv("APP"))

            operation_logger.info("Working")

            return {"data": { "ok": True } }

        except Exception as e:
            raise e