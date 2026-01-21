import os
import time
import uuid
import random
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from pinecone import Pinecone, ServerlessSpec
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

# Load env variables
load_dotenv()

class Jarvis:
    def __init__(self):
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_env = os.getenv("PINECONE_ENV", "us-east-1")
        self.index_name = "jarvis" 
        
        if not self.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY not found in .env file")

        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        
        # Ensure index exists (Integrated Inference)
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)
        
        # Initialize LLM (Optimized for speed)
        # temperature=0.7 for more natural conversation
        self.llm = ChatOllama(model="llama3.1", temperature=0.7)
        
        # Initialize Memory
        self.memory = ConversationBufferMemory(
            memory_key="history", 
            return_messages=True
        )
        
        # Prompt Template for fast RAG
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are J.A.R.V.I.S., a sophisticated AI assistant. 
            Answer the user's question using the following context if relevant. 
            If the context is empty or irrelevant, use your general knowledge.
            Keep answers concise and helpful.
            
            Context: {context}
            """),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])

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
                while not self.pc.describe_index(target_name).status.ready:
                    time.sleep(1)
        except Exception as e:
            print(f"Index check/creation warning: {e}")

    def add_document(self, file_path):
        """Ingests a document."""
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT are supported.")
            
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        
        vectors = []
        for i, doc in enumerate(splits):
            record = {
                "id": f"{os.path.basename(file_path)}-{i}-{uuid.uuid4()}",
                "values": [0.1] * 1024, 
                "metadata": {
                    "chunk_text": doc.page_content,
                    "source": file_path
                }
            }
            vectors.append(record)
            
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i+batch_size]
            self.index.upsert(vectors=batch)
            
        return len(vectors)

    def seed_knowledge(self):
        """Seeds knowledge from the 'data' directory."""
        data_dir = os.path.join(os.path.dirname(__file__), "data")
        if not os.path.exists(data_dir):
            return "Data directory not found."
            
        total_chunks = 0
        processed_files = []
        
        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)
            if filename.endswith(".txt") or filename.endswith(".pdf"):
                try:
                    chunks = self.add_document(file_path)
                    total_chunks += chunks
                    processed_files.append(filename)
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    
        return f"Ingested {total_chunks} chunks from: {', '.join(processed_files)}"

    def search_knowledge(self, query):
        """Searches Pinecone for context."""
        try:
            results = self.index.search(q=query, k=3, include_metadata=True)
            context = ""
            for match in results.matches:
                if match.score > 0.6: 
                    text = match.metadata.get("chunk_text", "")
                    context += f"{text}\n\n"
            return context
        except Exception:
            return ""

    def chat(self, query):
        """Processes a user query using fast RAG (No Agent Loop)."""
        # 1. Retrieve Context
        context = self.search_knowledge(query)
        
        # 2. Update Memory
        history = self.memory.load_memory_variables({})["history"]
        
        # 3. Generate Response
        chain = self.prompt | self.llm
        response = chain.invoke({
            "context": context,
            "history": history,
            "question": query
        })
        
        # 4. Save Context
        self.memory.save_context({"input": query}, {"output": response.content})
        
        return response.content
