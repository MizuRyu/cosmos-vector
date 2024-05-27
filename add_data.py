from src.cosmosdb import CosmosDB
from src.config import config
from src.vector import AzureOpenAIClient

def add_data():
    cosmos_db = CosmosDB(config)
    cosmos_db.initialize()

    with open('./data/text.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    oai_client = AzureOpenAIClient(config)
    embedding_result = oai_client.generate_embeddings(text=text)

    # データ作成
    cosmos_db.create_item(content=text, content_vector=embedding_result)

if __name__ == '__main__':
    add_data()