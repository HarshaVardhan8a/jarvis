import os
import time
from jarvis_core import Jarvis

def verify_logic():
    print("Initializing Jarvis...")
    jarvis = Jarvis()
    
    # Create a dummy file
    dummy_file = "test_knowledge.txt"
    with open(dummy_file, "w") as f:
        f.write("The secret code for the mission is 'BlueSky'. The target is located in Sector 7.")
    
    try:
        print(f"Adding document: {dummy_file}")
        num_chunks = jarvis.add_document(dummy_file)
        print(f"Document added. chunks: {num_chunks}")
        
        # Give Pinecone a moment to index
        print("Waiting for indexing...")
        time.sleep(10) 
        
        print("Querying Jarvis...")
        query = "What is the secret code and where is the target?"
        response = jarvis.chat(query)
        
        print(f"Query: {query}")
        print(f"Response: {response}")
        
        if "BlueSky" in response and "Sector 7" in response:
            print("Verification PASSED: Answer contains expected details.")
        else:
            print("Verification WARN: Answer might be incomplete, check output.")
            
    except Exception as e:
        print(f"Verification FAILED: {e}")
    finally:
        if os.path.exists(dummy_file):
            os.remove(dummy_file)

if __name__ == "__main__":
    verify_logic()
