from qdrant_client import QdrantClient
client = QdrantClient(":memory:")
methods = [m for m in dir(client) if "search" in m or "query" in m]
print(f"Methods with 'search' or 'query': {methods}")
