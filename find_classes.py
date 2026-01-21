import importlib

def check_import(path, class_name):
    try:
        module = importlib.import_module(path)
        if hasattr(module, class_name):
            print(f"[SUCCESS] Found {class_name} in {path}")
        else:
            print(f"[FAIL] {class_name} not in {path}")
    except ImportError as e:
        print(f"[FAIL] Could not import {path}: {e}")

print("Searching for ConversationBufferMemory...")
check_import("langchain.memory", "ConversationBufferMemory")
check_import("langchain_community.memory", "ConversationBufferMemory")
check_import("langchain.memory.buffer", "ConversationBufferMemory")

print("\nSearching for RetrievalQA...")
check_import("langchain.chains", "RetrievalQA")
check_import("langchain.chains.retrieval_qa.base", "RetrievalQA")
check_import("langchain_community.chains", "RetrievalQA")
