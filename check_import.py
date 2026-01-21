try:
    import langchain
    from langchain.memory import ConversationBufferMemory
    print("LangChain import successful")
except ImportError as e:
    print(f"Import failed: {e}")
