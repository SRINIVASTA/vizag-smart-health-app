import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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

def generate_stock_prediction_chart(df):
    fig, ax = plt.subplots(figsize=(7, 3.5))
    df['days_remaining'] = df.apply(lambda r: calculate_days_to_depletion(r['current_stock'], r['daily_avg_consumption']), axis=1)
    df_sorted = df.sort_values(by='days_remaining')
    colors = ['#DC3545' if x <= 5 else '#FFC107' if x <= 15 else '#28A745' for x in df_sorted['days_remaining']]
    bars = ax.barh(df_sorted['node_name'], df_sorted['days_remaining'], color=colors, height=0.6)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5, color='#E0E0E0')
    ax.set_xlabel('Predicted Days Until Total Stock-Out', fontsize=10, fontweight='bold')
    ax.set_title('AI Asset Exhaustion Timeline & Depletion Grid', fontsize=11, fontweight='bold')
    
    for bar in bars:
        width = bar.get_width()
        label_text = f"{width} days" if width != float('inf') else "Stable"
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, label_text, ha='left', va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    return fig

def generate_epidemic_risk_chart():
    conn = sqlite3.connect("smart_health.db")
    df = pd.read_sql_query("SELECT h.node_name, o.active_epidemic_risk_score FROM node_operations o JOIN administrative_hierarchy h ON o.node_id = h.node_id", conn)
    conn.close()
    
    fig, ax = plt.subplots(figsize=(7, 3.5))
    bars = ax.bar(df['node_name'], df['active_epidemic_risk_score'], color='#007BFF', alpha=0.85, width=0.4)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#E0E0E0')
    ax.set_ylabel('Active Outbreak Risk Multiplier', fontsize=10, fontweight='bold')
    ax.set_title('District Syndromic Anomaly & Infection Index Mapping', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.0)
    plt.xticks(rotation=15, ha='right', fontsize=9)
    ax.axhline(y=0.5, color='#DC3545', linestyle=':', linewidth=1.5, label='Critical Breach Threshold')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02, f"{round(height*100)}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
    plt.tight_layout()
    return fig
