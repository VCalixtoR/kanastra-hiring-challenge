"""
    Module responsible for checking and formatting environment variables into a dictionary used by the application
    Avoids code repetition for handling environment variables
    Implements the environments.py interface
"""
import logging
import os
from dotenv import load_dotenv
from providers.interfaces import IEnvironmentHandler
from injector import inject
from typing import Any, Dict, List, Optional

class EnvironmentHandler(IEnvironmentHandler):
    
    ENV_VARS = [
        {
            "key": "APP",
            "type": str,
            "required": False,
            "default": "FileProcessingApp"
        },
        {
            "key": "API_KEY",
            "type": str,
            "required": True
        },
        {
            "key": "DOCS_USERNAME",
            "type": str,
            "required": False,
            "default": "docsuser"
        },
        {
            "key": "DOCS_PASSWORD",
            "type": str,
            "required": False,
            "default": "docspass"
        },
        {
            "key": "ENVIRONMENT",
            "type": str,
            "required": False,
            "default": "local"
        }
    ]

    @inject
    def __init__(self):
        self.env_dict = self.__load_environment()

    def __get_missing_environment(self) -> List[str]:
        """ Returns a list of required environment variables that are missing """
        return [var["key"] for var in self.ENV_VARS if var["required"] and os.getenv(var["key"]) == None]

    def __load_environment(self) -> Dict[str, Optional[str]]:
        """ Loads environment variables, if any are missing, terminates the application """
        
        logging.basicConfig()
        logger = logging.getLogger(__name__)

        load_dotenv()
        missing_env = self.__get_missing_environment()
        if missing_env:
            logger.error(f"Missing {str(missing_env)} environment variable{'s' if len(missing_env) > 1 else ''}")
            exit(1)

        env_dict = {}
        for var in self.ENV_VARS:
            env_key = var["key"]
            env_type = var["type"]
            env_default = var.get("default")

            if env_default != None:
                env_value = os.getenv(env_key, env_default)
            else:
                env_value = os.getenv(env_key)
            
            if env_value == None:
                logger.error(f"Missing environment variable {env_key} default value")
                exit(1)
            
            try:
                env_dict[env_key] = env_type(env_value)
            except ValueError as e:
                logger.error(f"Error converting {env_key} to {env_type}: {str(e)}")
                exit(1)
            
        return env_dict
    
    def getenv(self, env_key: str) -> Optional[Any]:
        """ Returns a formatted environment variable """
        return self.env_dict.get(env_key)