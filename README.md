# J.A.R.V.I.S.

**J.A.R.V.I.S.** (Just A Rather Very Intelligent System) is a personal AI assistant built with Python, Streamlit, LangChain, and Pinecone.

## Features
- **Agentic Search**: Intelligently decides when to search its knowledge base or answer directly.
- **RAG (Retrieval Augmented Generation)**: Powered by Pinecone Integrated Inference (`llama-text-embed-v2`) and Llama 3.1.
- **Cyberpunk UI**: A custom themed interface for that "Jarvis" feel.
- **Auto-Seeding**: Built-in knowledge base initialization.

## Setup

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/HarshaVardhan8a/jarvis.git
    cd jarvis
    ```

2.  **Install Dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file:
    ```
    PINECONE_API_KEY=your_key_here
    PINECONE_ENV=us-east-1
    ```

4.  **Run**:
    ```bash
    ollama serve  # Ensure Llama 3.1 is pulled
    streamlit run app.py
    ```
