# config/settings.py

import os
from dotenv import load_dotenv

from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
DB_PATH = os.getenv('DB_PATH')

# Initialize the LLM and other components
llm = ChatGoogleGenerativeAI(model="gemini-pro")
embedding_model = OllamaEmbeddings(model="mxbai-embed-large:latest")

# Initialize ChromaDB for RAG Tool
vector_db = Chroma(
    persist_directory=r'C:\Users\ezequ\anyoneai\final_project\vector_db\chroma_db',
    embedding_function=embedding_model
)

# Initialize shared memory with memory management for main conversation
shared_memory = ConversationBufferWindowMemory(
    memory_key="history",
    return_messages=True,
    k=10  # Increased window size for more context
)

# Initialize separate memory for classification to prevent pollution of main conversation
classification_memory = ConversationBufferMemory(
    memory_key="classification_history",
    return_messages=False  # Do not return messages to prevent UI pollution
)
