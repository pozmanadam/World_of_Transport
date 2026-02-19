import argparse
import json
import math
import urllib.parse
import urllib.request


BASE_URL = "https://mikerhodes.cloudant.com"
DATABASE = "airportdb"
SEARCH_PATH = "_design/view1/_search/geo"

R = 6371.0

def haver_dist(lati1, long1, lati2, long2):
    lati1 = math.radians(lati1)
    long1 = math.radians(long1)
    lati2 = math.radians(lati2)
    long2 = math.radians(long2)
    dlong = long2 - long1
    dlati = lati2 - lati1
    a = (
        math.sin(dlati / 2) ** 2
        + math.cos(lati1) * math.cos(lati2) * math.sin(dlong / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def bounding_box(lat, lon, radius_km):
    lat_delta = radius_km / 111
    lon_delta = radius_km / (111 * math.cos(math.radians(lat)))

    return (
        lat - lat_delta,
        lat + lat_delta,
        lon - lon_delta,
        lon + lon_delta,
    )

def curl_query(min_lat, max_lat, min_lon, max_lon):
    query_string = f"lat:[{min_lat} TO {max_lat}] AND lon:[{min_lon} TO {max_lon}]"

    encoded_query = urllib.parse.urlencode({"query": query_string})

    url = f"{BASE_URL}/{DATABASE}/{SEARCH_PATH}?{encoded_query}"

    with urllib.request.urlopen(url) as response:
        data = response.read()
        return json.loads(data)

def extract_hubs(raw_data, latitude, longitude, distance):    
    hubs = []
    for row in raw_data.get("rows"):

        name, lat, lon = get_row_data(row)

        if name is None or lat is None or lon is None:
            continue

        distance_actual = haver_dist(latitude, longitude, lat, lon)

        if distance_actual <= distance:
            i = 0
            while i < len(hubs): 
                if hubs[i][3] < distance_actual:
                    i = i+1
                else:
                    hubs.insert(i,(name, lat, lon, distance_actual))
                    break
            if i == len(hubs):
                hubs.append((name, lat, lon, distance_actual))
    return hubs

def get_row_data(row):
        fields = row.get("fields")
        name = fields.get("name")
        lat = fields.get("lat")
        lon = fields.get("lon")
        return (
            name,
            lat,
            lon
        )

def main():
    
    parser = argparse.ArgumentParser(
        description="Find transport hubs within a given distance."
    )
    parser.add_argument("latitude", type=float)
    parser.add_argument("longitude", type=float)
    parser.add_argument("distance", type=float, help="Distance in km")

    args = parser.parse_args()
    
    min_lat, max_lat, min_lon, max_lon = bounding_box(
        args.latitude, args.longitude, args.distance
    )

    try:
        raw_data = curl_query(min_lat, max_lat, min_lon, max_lon)
    except Exception as e:
        print(f"Error querying database: {e}")
        return
    
    hubs = extract_hubs(raw_data, args.latitude, args.longitude, args.distance)
    
    if len(hubs) == 0:
        print("No hubs found.")
        return

    for name, lat, lon, dist in hubs:
        print(f"{name} | ({lat}, {lon}) | {dist:.2f} km")

if __name__ == "__main__":
    main()



