from qdrant_client import QdrantClient
print("Inspecting QdrantClient...")
print(dir(QdrantClient))
try:
    client = QdrantClient(":memory:")
    print("Instance attributes:")
    print([d for d in dir(client) if not d.startswith("_")])
except Exception as e:
    print(f"Error: {e}")
