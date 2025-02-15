import requests

API_KEY = "hoewgoehwaog"  # Replace with your actual API key
LAT, LNG = 17.3850, 78.4867  # Hyderabad coordinates
RADIUS = 5000  # Search within 5km
TYPE = "restaurant"

url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={LAT},{LNG}&radius={RADIUS}&type={TYPE}&key={API_KEY}"

response = requests.get(url)
data = response.json()

if data["status"] == "OK":
    for place in data["results"][:10]:  # Get top 10 restaurants
        name = place["name"]
        address = place.get("vicinity", "No address available")
        rating = place.get("rating", "No rating")
        print(f"🍽 {name} - ⭐ {rating} - 📍 {address}")
else:
    print(f"Error: {data.get('error_message', 'Unknown error')}")
