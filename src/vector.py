import openai


class AzureOpenAIClient:
    def __init__(self,config):
        self.endpoint = config.AZURE_OPENAI_ENDPOINT
        self.api_key = config.AZURE_OPENAI_API_KEY
        self.model_name = config.AZURE_OPENAI_MODEL_NAME
        self.api_version = config.AZURE_OPENAI_API_VERSION

        openai.api_type = "azure"
        openai.azure_endpoint = self.endpoint
        openai.api_key = self.api_key
        openai.api_version = self.api_version
    
    def get_openai_client(self):
        return openai.AzureOpenAI(
            azure_endpoint=self.endpoint, 
            api_key=self.api_key, 
            api_version=self.api_version
            )
    
    def generate_embeddings(self, text):
        embeddings = self.get_openai_client().embeddings.create(
            input=[text], 
            model=self.model_name
            ).data[0].embedding
        
        return embeddings