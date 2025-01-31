import json

def load_hamburg_geojson():
    with open("geojson/hamburg_map.geojson", "r") as f:
        return json.load(f)
