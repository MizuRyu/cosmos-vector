from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    COSMOS_ENDPOINT: str = os.getenv('AZURE_COSMOS_ENDPOINT')
    COSMOS_KEY: str = os.getenv('AZURE_COSMOS_KEY')
    COSMOS_CONNECTION_STRING: str = os.getenv('AZURE_COSMOS_CONNECTION_STRING')
    COSMOS_DATABASE_NAME: str = os.getenv('AZURE_COSMOS_DATABASE_NAME')
    COSMOS_CONTAINER_NAME: str = os.getenv('AZURE_COSMOS_CONTAINER_NAME')

config = Config()
print("####Config values:")
print(config.COSMOS_ENDPOINT)
print(config.COSMOS_KEY)
print(config.COSMOS_CONNECTION_STRING)
print(config.COSMOS_DATABASE_NAME)