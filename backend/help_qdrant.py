from qdrant_client import QdrantClient
client = QdrantClient(":memory:")
print(help(client.query_points))
