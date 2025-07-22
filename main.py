from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os
from datetime import datetime
from langchain_community.llms import Ollama

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI model
llm = Ollama(model="llama3.2")  # Runs Llama3 N2 locally

CACHE_FILE = "market_cache.json"

def scrape_and_cache_market_data():
    # Scrape Google News for real estate news
    url = "https://news.google.com/search?q=real%20estate%20bay%20area&hl=en-US&gl=US&ceid=US:en"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    articles = []
    for item in soup.select("article"):
        headline = item.find("h3")
        if not headline:
            continue
        title = headline.text
        link = "https://news.google.com" + headline.find("a")["href"][1:]
        blurb = item.find("span")
        summary = blurb.text if blurb else ""
        articles.append({"title": title, "url": link, "blurb": summary})
        if len(articles) >= 5:
            break
    
    cache = {
        "news": articles,
        "last_updated": datetime.utcnow().isoformat()
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

# Schedule the job to run weekly
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_and_cache_market_data, "interval", weeks=1)
scheduler.start()

# Run once at startup to ensure cache exists
if not os.path.exists(CACHE_FILE):
    scrape_and_cache_market_data()

@app.get("/market/news")
def get_market_news():
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
    return {"news": cache.get("news", []), "last_updated": cache.get("last_updated")}

@app.get("/market/listings")
def get_sf_links():
    return {
        "links": [
            {"name": "Redfin Hot Homes - San Francisco", "url": "https://www.redfin.com/city/17151/CA/San-Francisco/hot-homes"},
            {"name": "Zillow San Francisco Homes", "url": "https://www.zillow.com/san-francisco-ca/houses/"},
            {"name": "Realtor.com San Francisco", "url": "https://www.realtor.com/realestateandhomes-search/San-Francisco_CA"},
            {"name": "Trulia San Francisco", "url": "https://www.trulia.com/CA/San_Francisco/"},
        ]
    }

@app.get("/market/mortgage")
def get_mortgage_rate():
    return {"rate": "6.75%"}

@app.get("/market/appreciation")
def get_appreciation():
    return {"appreciation": "+4.2% YoY"}

@app.get("/market/newbuilds")
def get_new_builds():
    return {"new_builds": "12 new homes this month"}

@app.get("/ask")
def chat(query: str):
    try:
        # Use the actual AI model to generate a response
        ai_response = llm.invoke(query)
        return {"response": ai_response}
    except Exception as e:
        print(f"Error in /ask endpoint: {e}")
        return {"response": "An error occurred while processing your request."} 