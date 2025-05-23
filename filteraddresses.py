import math
import json

def haversine(lat1, lon1, lat2, lon2):
    # Radius of Earth in miles. Use 6371 for kilometers
    R = 3958.8
    
    # Convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

# # Example usage:
# lat1, lon1 = 33.4081, -111.8086
# lat2, lon2 = 33.4195, -111.8223

# distance = haversine(lat1, lon1, lat2, lon2)
# print(f"Distance: {distance:.2f} miles")

with open('addresses', 'r') as f:
  data = f.readlines()

# "geometry": {"type": "Point", "coordinates": [-111.7746896, 33.3397748]}

origin = [-111.7443136, 33.3398274]

filtered_addresses = []
for d in data:
  d = json.loads(d)
  geolocation = d["geometry"]["coordinates"]
  distance = haversine(origin[1], origin[0], geolocation[1], geolocation[0])

  if distance < 0.5 and distance > 0:
    filtered_addresses.append({
      "address": d["properties"]["number"] + " " + d["properties"]["street"],
      "distance": distance
    })
  

filtered_addresses.sort(key=lambda x: x["distance"])

with open('filtered_addresses', 'w') as f:
  f.write(json.dumps(filtered_addresses, indent=4))