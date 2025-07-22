from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ✅ Setup AI Model + Vector Database
llm = ChatOpenAI(openai_api_key="your-api-key")  
emb_model = SentenceTransformer("all-MiniLM-L6-v2") 

# ✅ Create & Populate Vector Store with Real Estate Listings
listings = 
[
    "2-bedroom condo in SF for $750K",
    "Luxury apartment in Palo Alto near Stanford for $1.2M",
    "Townhouse in San Jose with backyard for $850K"
]

embeddings = emb_model.encode(listings)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

def retrieve_listing(query):
    query_embedding = emb_model.encode([query])
    _, idx = index.search(np.array(query_embedding), k=3)  # ✅ Retrieve top 3 matches
    return [listings[i] for i in idx[0]]

# ✅ Define AI Agent Actions
tools = [
    Tool(name="RealEstateSearch", func=retrieve_listing, description="Finds real estate listings.")
]

# ✅ Create Agent That Retrieves + Generates Responses
agent = initialize_agent(tools, llm, verbose=True)

def process_query(query):
    return agent.run(query)

