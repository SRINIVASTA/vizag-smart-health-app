import pandas as pd

def map_cross_tier_drone_grid(transfers_list):
    coords = []
    for t in transfers_list:
        coords.append({"lat": t["from_lat"], "lon": t["from_lon"]})
        coords.append({"lat": t["to_lat"], "lon": t["to_lon"]})
    return pd.DataFrame(coords)
