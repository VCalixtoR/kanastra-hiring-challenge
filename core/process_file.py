import csv
from datetime import datetime
from fastapi import File, HTTPException
from fastapi.responses import JSONResponse
from io import StringIO
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from providers import injector_container, ICustomUvicornLogger, IEnvironmentHandler, IServicesEnum, ISQLAlchemyORM
from utils.util import generate_operation_id

REQUIRED_COLUMNS = ["debtId", "name", "governmentId", "email", "debtAmount", "debtDueDate"]
REQUEST_TIMEOUT_SECONDS = 60

class ProcessFile:

    def __init__(self):
        # dependency injection
        self.env_handler: IEnvironmentHandler = injector_container.get(IEnvironmentHandler)
        self.custom_uvicorn_logger: ICustomUvicornLogger = injector_container.get(ICustomUvicornLogger)
        self.database_orm: ISQLAlchemyORM = injector_container.get(ISQLAlchemyORM)

        # Create the log handler with a unique identifier to the request
        self.operation_logger_id = generate_operation_id("process-file")
        self.operation_logger = self.custom_uvicorn_logger.get_logger(IServicesEnum.PROCESS_FILE, self.operation_logger_id)

    def __check_csv_columns(self, reader: csv.DictReader):
        header = reader.fieldnames
        missing_columns = [col for col in REQUIRED_COLUMNS if col not in header]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing columns: {', '.join(missing_columns)}")
    
    async def check_file_fields_get_reader(self, file: File) -> csv.DictReader:
        self.operation_logger.info(f"starting a new file processing operation for {file.filename}")

        if file.content_type != 'text/csv':
            error_message = "Invalid file format. Make sure the file is a csv."
            operation_logger.error(error_message)
            raise HTTPException(status_code=400, detail=error_message)
        
        contents = await file.read()
        csv_data = StringIO(contents.decode('utf-8'))
        reader = csv.DictReader(csv_data)

        self.__check_csv_columns(reader)

        return reader

    async def get_parsed_field_records(self, reader: csv.DictReader) -> dict:
        self.operation_logger.info(f"Parsing the file while checking its fields...")

        # Parses each item before doing the operation to avoid errors
        records = []
        errors = []
        for row in reader:
            try:
                record = {
                    "debtId": str(row["debtId"]),
                    "name": str(row["name"]),
                    "governmentId": int(row["governmentId"]),
                    "email": str(row["email"]),
                    "debtAmount": float(row["debtAmount"]),
                    "debtDueDate": datetime.strptime(str(row["debtDueDate"]), '%Y-%m-%d')
                }
                records.append(record)
            except Exception as e:
                errors.append(f"Error processing row {row}: {str(e)}")
        
        if len(errors) > 0:
            raise HTTPException(status_code=400, detail=f"There are errors in your input, solve the errors before sending to this API: {errors}")
        
        return records

    async def do_records_processing_get_errors(self, records: dict) -> JSONResponse:
        self.operation_logger.info(f"Saving the files with the initial started status")
        
        # Try to start all of the operations
        session = self.database_orm.get_session()
        errors = []
        for record in records:
            try:

                existing_record = session.execute(
                    select(self.database_orm.DebtBillsAutomation).filter_by(debtId=record['debtId'])
                ).scalar_one_or_none()
            
                if existing_record:
                    self.operation_logger.info(f"Record with debtId {record['debtId']} already exists")
                    continue

                new_debt = self.database_orm.DebtBillsAutomation(
                    debtId=record['debtId'],
                    name=record['name'],
                    governmentId=record['governmentId'],
                    email=record['email'],
                    debtAmount=record['debtAmount'],
                    debtDueDate=record['debtDueDate'],
                    status='started',
                    errorMessage=None
                )
                session.add(new_debt)
            except SQLAlchemyError as e:
                session.rollback()
                errors.append(f"Error saving record {record}: {str(e)}")
            except Exception as e:
                raise HTTPException(f"Unexpected error for record {record}: {str(e)}")

        if errors:
            return JSONResponse(status_code=500, content={"errors": errors})

        session.commit()
        session.close()

        return await self.execute()
                
    async def execute(self) -> JSONResponse:
        self.operation_logger.info(f"Doing the file processing ...")

        try:
            
            # Eu iria usar asyncio tasks para paralelizar as execuções de 1000 em 1000 (env configuravel no .env e cloudbuild)
            # FastAPI usa o asyncio para paralelizar as requests dos usuários e para fazer locks e sincronização neste cenário é melhor que threads.
            # Execuções com erro poderiam ser retomadas ao retrigar a rota verificando, caso houver, o status salvo na base DebtBillsAutomation.
            #   Além do enum DebtStatusEnum salvo em DebtBillsAutomation.status (started, bill_generated, bill_sent, done, error)
            #       indicar a etapa em que o erro foi a mensagem de erro seria logada e salvada em DebtBillsAutomation.errorMessage

            # Não acho que este seja o melhor fluxo pra essa solução envolvendo a emissão destes relatórios, uma melhor seria usar
            #   lambdas, sqs e S3 na AWS ou usar cloud functions, pub sub e cloud storage na GCP
            #   se fosse eu criando essa solução para produção, iria criar um CI CD que usa terraform ou serverless para subir a 
            #   infraestrutura automaticamente para a cloud quando houverem commits para dev ou prod, ilustrei uma arquitetura no 
            #   readme deste repo. Posso apresentar algumas soluções envolvendo infraestrutura como codigo que fiz em uma reunião
            
            return JSONResponse(status_code=201, content={"message": f"The process is still incomplete but was done without errors"})

        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Error {e.__class__} {e}"})