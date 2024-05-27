import uuid
import json

from azure.cosmos import CosmosClient, PartitionKey, exceptions


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

    def create_container(self):
        if not self.database:
            self.create_database()
        try:
            vector_policy = self.create_vector_embedding_policy()
            indexing_policy = self.create_indexing_policy()
            
            self.container = self.database.create_container_if_not_exists(
                id=self.container_name,
                partition_key=PartitionKey(path="/id"),
                indexing_policy=indexing_policy,
                vector_embedding_policy=vector_policy,
                offer_throughput=400  # 専用スループットを設定
            )
        except exceptions.CosmosHttpResponseError as e:
            print(f"Failed to create container: {e}")
            raise

    def create_item(self, content, content_vector):
        item = {
            'id': str(uuid.uuid4()),
            'content': content,
            'contentvector': content_vector
        }
        try:
            self.container.create_item(body=item)
            print("Item created")
        except exceptions.CosmosHttpResponseError as e:
            print(f"Failed to create item: {e}")
            raise

    def vector_search(self, query_vector):
        if not self.container:
            self.create_container()
        query = """
        SELECT c.id, c.content, VectorDistance(c.contentvector, @query_vector) AS SimilarityScore
        FROM c
        """
        parameters = [
            {"name": "@query_vector", "value": query_vector}
        ]

        search_results = self.container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        )
        print("search_results: ", search_results)
        results = [ item for item in search_results]
        return json.dumps(results, indent=True)

    def container_initialize(self):
        self.create_container()
        print("CosmosDB initialized")