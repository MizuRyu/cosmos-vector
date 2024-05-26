from azure.cosmos import CosmosClient, PartitionKey, exceptions
from src.config import config


class CosmosDB:
    def __init__(self, config):
        self.client = CosmosClient(config.COSMOS_ENDPOINT, config.COSMOS_KEY)
        self.database_name = config.COSMOS_DATABASE_NAME
        self.container_name = config.COSMOS_CONTAINER_NAME
        self.database = self.client.get_database_client(self.database_name)
        self.container = None

    def create_database(self):
        self.database = self.client.create_database_if_not_exists(id=self.database_name)

    def create_vector_embedding_policy(self):
        vector_embedding_policy = {
            "vectorEmbeddings": [
                {
                    "path": "/contentvector",
                    "dataType": "float32",
                    "distanceFunction": "cosine",
                    "dimensions": 1536
                }
            ]
        }
        return vector_embedding_policy
    
    def create_indexing_policy(self):
        indexing_policy = {
            "includedPaths": [
                {
                    "path": "/*"
                }
            ],
            "excludedPaths": [
                {
                    "path": "/\"_etag\"/?"
                }
            ],
            "vectorIndexes": [
                {
                    "path": "/contentvector",
                    "type": "quantizedFlat"
                }
            ]
        }
        return indexing_policy

    try:
        def create_container(self):
            if not self.database:
                self.create_database()
            vector_policy = self.create_vector_embedding_policy()
            indexing_policy = self.create_indexing_policy()
            
            self.container = self.database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=PartitionKey(path="/id"),
                indexing_policy=indexing_policy,
                vector_embedding_policy=vector_policy,
                offer_throughput=400  # 専用スループットを設定

            )
    except exceptions.CosmosHttpResponseError:
        raise

    def initialize(self):
        self.create_container()
        print("CosmosDB initialized")

if __name__ == '__main__':
    cosmos = CosmosDB(config)
    cosmos.initialize()