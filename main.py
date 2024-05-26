from src.cosmosdb import CosmosDB
from src.config import Config

def main():
    print("creating cosmosdb container...")
    cosmos_db = CosmosDB(Config())
    cosmos_db.initialize()
    print("cosmosdb container created")

if __name__ == '__main__':
    main()