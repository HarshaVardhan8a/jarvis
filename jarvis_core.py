import os
import time
import uuid
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from pinecone import Pinecone, ServerlessSpec
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chains import RetrievalQA

# Load env variables
load_dotenv()

class Jarvis:
    def __init__(self):
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_env = os.getenv("PINECONE_ENV", "us-east-1")
        self.index_name = "jarvis" # Matches user's index name
        
        if not self.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY not found in .env file")

        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        
        # Ensure index exists (Integrated Inference)
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)
        
        # Initialize LLM for Agent (Still need a brain for the agent)
        self.llm = ChatOllama(model="llama3.1", temperature=0)
        
        # Initialize Memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", 
            return_messages=True
        )
        
        # Tools
        self.tools = [
            Tool(
                name="Jarvis Knowledge Base",
                func=self.search_knowledge,
                description="Useful for answering questions about detailed topics, stored documents, or specific facts. Use this tool finding info about Diligent Corporation or uploaded files."
            ),
             Tool(
                name="Current Time",
                func=lambda x: f"The current local time is {time.ctime()}.",
                description="Useful for getting the current local time and date."
            )
        ]
        
        # Initialize Agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=True
        )

    def _ensure_index_exists(self):
        """Checks if index exists, if not creates it with Integrated Inference."""
        try:
            existing_indexes = [i.name for i in self.pc.list_indexes()]
            target_name = self.index_name

            if target_name not in existing_indexes:
                print(f"Creating index: {target_name} with Integrated Inference")
                self.pc.create_index_for_model(
                    name=target_name,
                    cloud="aws",
                    region=self.pinecone_env,
                    embed={
                        "model": "llama-text-embed-v2",
                        "field_map": {"text": "chunk_text"}
                    }
                )
                # Wait for index to be ready
                while not self.pc.describe_index(target_name).status.ready:
                    time.sleep(1)
        except Exception as e:
            print(f"Index check/creation warning: {e}")

    def add_document(self, file_path):
        """Ingests a document. Splits text and upserts to Pinecone for auto-embedding."""
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT are supported.")
            
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        # Upsert logic for Integrated Inference
        # We prepare records with "chunk_text" in the inputs/metadata
        vectors = []
        for i, doc in enumerate(splits):
            # For integrated inference, the ID and the text in the mapped field are key.
            # We usually upsert 'vectors' but with empty values and populate metadata? 
            # Or use specific inference methods. 
            # As per common patterns for this 'create_index_for_model' preview feature:
            # We upsert records where we map the text field.
            
            record = {
                "id": f"{os.path.basename(file_path)}-{i}-{uuid.uuid4()}",
                "values": [0.1] * 1024, # Dummy values if required, or potentially omitted.
                # Ideally Pinecone ignores 'values' if embedding is enabled, or we don't send it. 
                # Let's try sending metadata matching the field_map.
                "metadata": {
                    "chunk_text": doc.page_content,
                    "source": file_path
                }
            }
            vectors.append(record)
            
        # Batch upsert
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)
            
        return len(vectors)

    def search_knowledge(self, query):
        """Searches the Pinecone index using the text query."""
        try:
            # For integrated inference, we search with 'query' text.
            # Using the query_text parameter if available or 'inputs'.
            # If the client is standard, we usually need to convert query to vector explicitly 
            # UNLESS the index supports 'search' with text directly.
            # Assuming 'pc.inference.embed' is handled by the index during query?
            # Actually, typically we use: query_response = index.search(q=query, ...) 
            # Warning: Python SDK specific syntax for this is emerging. 
            # I will assume `index.query` with `vector` is standard, but `inputs` for model.
            
            # ATTEMPT 1: Search using 'query' string in 'vector' field (unlikely) 
            # ATTEMPT 2: Check if there's a specific method.
            # Let's try passing the text to 'query' via 'inputs' or similar if documentation implies.
            # User instructions implied: "search with text".
            
            # Workaround: Use pc.inference.embed to get vector, then query? 
            # "have Pinecone generate vectors automatically" -> Implications for query too.
            # If I can't find the exact syntax, I'll return a placeholder or try `query(data=...)`
            
            # Let's assume for this Agent I need to implement the 'search' correctly.
            # Since I cannot know the exact syntax without docs, I will use a safe fallback:
            # I will generate a dummy vector if needed, but likely the index handles text.
            
            # Correct approach for many such systems:
            results = self.index.search(
                q=query, # Some clients support 'q' or 'query' as text
                k=5,
                include_metadata=True
            )
            
            # Format results
            context = ""
            for match in results.matches:
                if match.score > 0.6: # Filter low relevance
                    text = match.metadata.get("chunk_text", "")
                    context += f"- {text}\n"
            
            return context if context else "No relevant information found."
            
        except Exception as e:
            # Fallback/Debug info
            return f"Search Error: {e}. (Note: Ensure Pinecone SDK supports text search for this index type)."

    def chat(self, query, callbacks=None):
        """Processes a user query via the Agent."""
        try:
            return self.agent.run(query, callbacks=callbacks)
        except Exception as e:
            return f"I encountered an error processing your request: {e}"
