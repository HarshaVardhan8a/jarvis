import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load env variables
load_dotenv()

def verify_pinecone():
    api_key = os.getenv("PINECONE_API_KEY")
    env = os.getenv("PINECONE_ENV", "us-east-1")
    index_name = "jarvis-memory"

    print(f"Checking Pinecone connection with key: {api_key[:5]}...{api_key[-5:]}")
    
    try:
        pc = Pinecone(api_key=api_key)
        indexes = pc.list_indexes()
        index_names = [i.name for i in indexes]
        print(f"Existing indexes: {index_names}")

        if index_name not in index_names:
            print(f"Creating index: {index_name}")
            pc.create_index(
                name=index_name,
                dimension=4096, # Llama 3.1
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=env
                )
            )
            while not pc.describe_index(index_name).status.ready:
                time.sleep(1)
            print(f"Index {index_name} created successfully.")
        else:
            print(f"Index {index_name} already exists.")
            
        print("Pinecone verification passed!")
        return True
    except Exception as e:
        print(f"Pinecone verification failed: {e}")
        return False

if __name__ == "__main__":
    verify_pinecone()
