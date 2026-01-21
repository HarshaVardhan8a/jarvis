import streamlit as st
import os
import tempfile
from langchain_community.callbacks import StreamlitCallbackHandler
from jarvis_core import Jarvis

# Page Config
st.set_page_config(page_title="J.A.R.V.I.S.", page_icon="🕸️", layout="wide")

# Custom CSS for "Jarvis" look
st.markdown("""
<style>
    .stApp {
        background-color: #050510;
        color: #00ffcc;
    }
    .stChatMessage {
        background-color: rgba(0, 255, 204, 0.05);
        border: 1px solid rgba(0, 255, 204, 0.2);
        border-radius: 12px;
        color: #e0e0e0;
    }
    div[data-testid="stChatMessageContent"] p {
        color: #e0e0e0;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background-color: #00ccaa;
        color: #000;
        border: none;
        box-shadow: 0 0 10px #00ccaa;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00ffcc;
        box-shadow: 0 0 20px #00ffcc;
    }
    h1, h2, h3 {
        color: #00ffcc !important;
        text-shadow: 0 0 5px #00ffcc;
        font-family: 'Orbitron', sans-serif;
    }
    .stSpinner > div {
        border-color: #00ffcc;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Jarvis (Singleton-ish via cache)
@st.cache_resource
def get_jarvis():
    try:
        return Jarvis()
    except Exception as e:
        st.error(f"Failed to initialize Jarvis: {e}")
        return None

if "jarvis" not in st.session_state:
    st.session_state.jarvis = get_jarvis()

jarvis = st.session_state.jarvis

# Sidebar for Knowledge Management
with st.sidebar:
    st.title("🧠 Core Systems")
    st.markdown("Wait for the system to come online.")
    
    if st.button("Initialize / Reset Knowledge Base"):
        with st.spinner("Seeding database with built-in knowledge..."):
            try:
                # Run the seeder function directly
                import seed_knowledge
                seed_knowledge.seed_knowledge()
                st.success("Knowledge Base Online! 50+ Data Points Active.")
            except Exception as e:
                st.error(f"Initialization Failed: {e}")
    
    st.markdown("---")
    st.markdown("### System Status")
    st.markdown("🟢 **Neural Interface**: Online")
    st.markdown("🟢 **Pinecone Link**: Active")
    st.markdown("🟢 **Ollama Model**: Llama 3.1")

# Main Chat Interface
st.title("J.A.R.V.I.S.")
st.caption("Integrated Systems Online | Pinecone Neural Link Active")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Jarvis anything..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    if jarvis:
        with st.chat_message("assistant"):
            # Create a container for the agent's thoughts
            st_callback = StreamlitCallbackHandler(st.container())
            try:
                response = jarvis.chat(prompt, callbacks=[st_callback])
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error generating response: {e}")
    else:
        st.error("Jarvis is not initialized. Check your configuration.")
