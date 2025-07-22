import requests
from bs4 import BeautifulSoup

def fetch_zillow_listings(city, min_price=None, max_price=None, beds=None):
    url = f"https://www.zillow.com/homes/for_sale/{city}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Failed to fetch listings (Status Code: {response.status_code})"}

    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all("div", class_="StyledPropertyCardDataWrapper")

    results = []
    for listing in listings:
        try:
            price = listing.find("span", class_="PropertyCardPrice").text.strip()
            address = listing.find("address", class_="PropertyCard-address").text.strip()
            image_url = listing.find("img")["src"] if listing.find("img") else "No image available"
            listing_url = listing.find("a", class_="StyledPropertyCardAnchor")["href"] if listing.find("a", class_="StyledPropertyCardAnchor") else "#"
            
            # ✅ Apply user-defined filters dynamically
            price_value = int(price.replace("$", "").replace(",", "").split("+")[0]) if price else None
            if (min_price and price_value < min_price) or (max_price and price_value > max_price):
                continue
            if beds and f"{beds} bds" not in listing.text:
                continue

            results.append({
                "title": address,
                "price": price,
                "location": city.replace("-", " ").title(),
                "image": image_url,
                "link": f"https://www.zillow.com{listing_url}"
            })
        except AttributeError:
            continue  # ✅ Prevents crashes if any elements are missing

    return results if results else {"error": "No listings found for the given criteria."}
