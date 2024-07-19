"""
Route: 
    - POST /process-file (APIKey authentication)
Description: 
    - Performs file processing
"""
from fastapi import Depends, APIRouter, UploadFile, File
from core import ProcessFile
from handlers import auth_with_api_key

router = APIRouter()

@router.post("/process-file", dependencies=[Depends(auth_with_api_key)])
async def post_process_file(file: UploadFile = File(...)):

    process_file_handler = ProcessFile()
    reader = await process_file_handler.check_file_fields_get_reader(file)
    records = await process_file_handler.get_parsed_field_records(reader)
    json_response = await process_file_handler.do_records_processing_get_errors(records)

    return json_response