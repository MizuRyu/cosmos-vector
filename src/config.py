from dataclasses import dataclass
import os
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

@dataclass
class Config:
    COSMOS_ENDPOINT: str = os.getenv('AZURE_COSMOS_ENDPOINT')
    COSMOS_KEY: str = os.getenv('AZURE_COSMOS_KEY')
    COSMOS_CONNECTION_STRING: str = os.getenv('AZURE_COSMOS_CONNECTION_STRING')
    COSMOS_DATABASE_NAME: str = os.getenv('AZURE_COSMOS_DATABASE_NAME')
    COSMOS_CONTAINER_NAME: str = os.getenv('AZURE_COSMOS_CONTAINER_NAME')
    AZURE_OPENAI_ENDPOINT: str = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY: str = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_API_VERSION: str = os.getenv('AZURE_OPENAI_API_VERSION')
    AZURE_OPENAI_MODEL_NAME: str = os.getenv('AZURE_OPENAI_MODEL_NAME')

config = Config()