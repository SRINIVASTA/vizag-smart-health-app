import sqlite3
import pandas as pd

def calculate_days_to_depletion(stock, consumption):
    if consumption <= 0: return float('inf')
    return round(stock / consumption, 1)

def run_cross_tier_supply_balancing():
    conn = sqlite3.connect("smart_health.db")
    df = pd.read_sql_query("""
        SELECT i.*, h.node_name, h.latitude, h.longitude, h.district_name
        FROM inventory i 
        JOIN administrative_hierarchy h ON i.node_id = h.node_id
    """, conn)
    conn.close()
    
    transfers = []
    deficits = df[df['current_stock'] <= df['min_required_threshold']]
    surpluses = df[df['current_stock'] > (df['min_required_threshold'] * 2)]
    
    for _, def_row in deficits.iterrows():
        match = surpluses[surpluses['item_name'] == def_row['item_name']]
        if not match.empty:
            best_source = match.iloc[0]
            transfers.append({
                "item": def_row['item_name'],
                "from_center": best_source['node_name'], "from_lat": best_source['latitude'], "from_lon": best_source['longitude'],
                "to_node": def_row['node_name'], "to_lat": def_row['latitude'], "to_lon": def_row['longitude'],
                "quantity": int(def_row['min_required_threshold'] * 1.5)
            })
    return df, transfers
