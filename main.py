from src.cosmosdb import CosmosDB
from src.config import config
from src.vector import AzureOpenAIClient

def main():
    # CosmosDBのセットアップ
    cosmos_db = CosmosDB(config)
    cosmos_db.container_initialize()

    #Azure OpenAIクライアント作成
    oai_client = AzureOpenAIClient(config)
    
    # 検索クエリ
    query_text = "勤務規定について知りたい"
    embedding_result = oai_client.generate_embeddings(text=query_text)
    print(embedding_result)

    # vector検索
    search_result = cosmos_db.vector_search(embedding_result)
    print(search_result)

if __name__ == '__main__':
    main()