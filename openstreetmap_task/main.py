import requests
import pandas as pd

city_name = "Ahmedabad"
overpass_url = "http://overpass-api.de/api/interpreter"

query = f"""
[out:json][timeout:25];
area["name"="{city_name}"]->.searchArea;
(
  node["tourism"~"attraction|museum|artwork|gallery|zoo|theme_park|viewpoint|park"](area.searchArea);
  way["tourism"~"attraction|museum|artwork|gallery|zoo|theme_park|viewpoint|park"](area.searchArea);
  relation["tourism"~"attraction|museum|artwork|gallery|zoo|theme_park|viewpoint|park"](area.searchArea);
);
out center;
"""

response = requests.get(overpass_url, params={'data': query})
data = response.json()

results = []
for element in data["elements"]:
    lat = element.get("lat") or element.get("center", {}).get("lat")
    lon = element.get("lon") or element.get("center", {}).get("lon")
    name = element.get("tags", {}).get("name", "N/A")
    tourism_type = element.get("tags", {}).get("tourism", "N/A")

    if lat and lon:
        results.append({
            "Name": name,
            "Type": tourism_type,
            "Latitude": lat,
            "Longitude": lon
        })

# Save to CSV
df = pd.DataFrame(results)
df.to_csv(f"scraped_data.csv", index=False)
print(f"Saved {len(df)} tourist attractions in {city_name}.")
