import requests
from langchain.memory import ConversationBufferMemory
from scraper import fetch_zillow_listings

# ✅ Initialize memory
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
memory = ConversationBufferMemory()


def format_listings_response(listings):
    """Formats real estate listings for chatbot responses with images and links."""
    response = "**🏡 Available Properties in the Bay Area:**\n\n"
    
    for listing in listings:
        address = listing.get("address", "Address not available")
        price = listing.get("price", "Price not listed")
        image_url = listing.get("image", "No image available")
        listing_url = listing.get("url", "#")

        response += f"- **{address}**\n  💰 {price}\n  🔗 [View Listing]({listing_url})\n  ![Image]({image_url})\n\n"

    return response


def real_estate_chat(query):
    try:
        past_context = memory.load_memory_variables({})
        full_prompt = f"Previous Conversations: {past_context}\nUser Query: {query}"

        # ✅ Extract city dynamically from query
        bay_area_cities = ["San Francisco", "Oakland", "San Jose", "Berkeley", "Palo Alto", "Fremont", "Sunnyvale", "Mountain View"]
        city = next((c for c in bay_area_cities if c.lower() in query.lower()), "San Francisco")

        # ✅ Trigger web scraper dynamically for Zillow-related queries
        if "zillow" in query.lower() or "real estate" in query.lower():
            listings = fetch_zillow_listings(city, min_price=500000, max_price=1000000, beds=2)

            if listings:
                return format_listings_response(listings)  # ✅ Display properly formatted listings

        # ✅ Call Ollama API for other queries
        payload = {"model": "llama3.2", "prompt": full_prompt, "stream": False}
        response = requests.post(OLLAMA_URL, json=payload)
        ai_response = response.json().get("response", "AI response error")
        memory.save_context({"input": query}, {"output": ai_response})

        return ai_response
    except Exception as e:
        print(f"Error processing AI response: {e}")
        return "Something went wrong with AI processing."


