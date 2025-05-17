import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL of gyms in Ahmedabad on Magicpin
url = "https://magicpin.in/india/Ahmedabad/All/Gym/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Send HTTP request
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

gym_data_script = None
for tag in soup.find_all("script", type="application/ld+json"):
    try:
        data = json.loads(tag.string.strip())
        if isinstance(data, dict) and data.get("@type") == "ItemList":
            gym_data_script = data
            break
    except Exception:
        continue

gyms = []

# Extract data from the JSON structure
if gym_data_script:
    for gym in gym_data_script.get("itemListElement", []):
        item = gym.get("item", {})
        geo = item.get("geo", {})
        gyms.append({
            "GYM Name": item.get("name", "N/A"),
            "Address": item.get("address", "N/A"),
            "Area": item.get("areaServed", "N/A"),
            "City": "Ahmedabad",
            "State": "Gujarat",
            "Phone Number": item.get("telephone", "N/A"),
            "Timings": "N/A",
            "Map Link": item.get("hasMap", f"https://www.google.com/maps/search/?api=1&query={geo.get('latitude')},{geo.get('longitude')}")
        })

    # Save to CSV
    df = pd.DataFrame(gyms)
    df.to_csv("scraped_data.csv", index=False)
    print(f"Saved {len(df)} gyms to 'scraped_data.csv'")

else:
    print("Data not found")
