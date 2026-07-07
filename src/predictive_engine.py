# src/predictive_engine.py
import sqlite3
import json
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

# ==========================================
# 📊 SECTION 1: SYSTEM DATA COMPILATION
# ==========================================

def calculate_days_to_depletion(stock, consumption):
    if consumption <= 0: return float('inf')
    return round(stock / consumption, 1)

def run_cross_tier_supply_balancing():
    conn = sqlite3.connect("data/smart_health.db")
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

def log_audit_breach(entered_password):
    """Commits invalid password attempts to the immutable audit database ledger."""
    try:
        conn = sqlite3.connect("data/smart_health.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO system_audit_logs (user_role, node_id, action_type, details)
            VALUES (?, ?, ?, ?)
        """, ('ADMIN_DASHBOARD', 'GLOBAL_GATEWAY', 'SECURITY_BREACH', f'Unauthorised gateway attempt using password: {entered_password}'))
        conn.commit()
        conn.close()
    except Exception as e:
        pass

# ==========================================
# 📈 SECTION 2: CHARTS GRAPHICS CONTROLLER
# ==========================================

def generate_stock_prediction_chart(df):
    fig, ax = plt.subplots(figsize=(7, 3.2))
    df['days_remaining'] = df.apply(lambda r: calculate_days_to_depletion(r['current_stock'], r['daily_avg_consumption']), axis=1)
    df_sorted = df.sort_values(by='days_remaining')
    colors = ['#DC3545' if x <= 5 else '#FFC107' if x <= 15 else '#28A745' for x in df_sorted['days_remaining']]
    bars = ax.barh(df_sorted['node_name'], df_sorted['days_remaining'], color=colors, height=0.5)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.5, color='#E0E0E0')
    ax.set_xlabel('Predicted Days Until Total Stock-Out', fontsize=9, fontweight='bold')
    ax.set_title('AI Asset Exhaustion Timeline & Depletion Grid', fontsize=10, fontweight='bold')
    
    for bar in bars:
        width = bar.get_width()
        label_text = f"{width} days" if width != float('inf') else "Stable"
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2, label_text, ha='left', va='center', fontsize=8, fontweight='bold')
    plt.tight_layout()
    return fig

def generate_epidemic_risk_chart(district_filter="All Districts"):
    conn = sqlite3.connect("data/smart_health.db")
    query = """
        SELECT h.node_name, o.active_epidemic_risk_score, h.district_name
        FROM node_operations o 
        JOIN administrative_hierarchy h ON o.node_id = h.node_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if district_filter != "All Districts":
        df = df[df['district_name'] == district_filter]
        
    fig, ax = plt.subplots(figsize=(7, 3.2))
    bars = ax.bar(df['node_name'], df['active_epidemic_risk_score'], color='#007BFF', alpha=0.85, width=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#E0E0E0')
    ax.set_ylabel('Active Outbreak Risk Multiplier', fontsize=9, fontweight='bold')
    ax.set_title('District Syndromic Anomaly & Infection Index Mapping', fontsize=10, fontweight='bold')
    ax.set_ylim(0, 1.0)
    plt.xticks(rotation=10, ha='right', fontsize=8)
    ax.axhline(y=0.5, color='#DC3545', linestyle=':', linewidth=1.5, label='Critical Breach')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.02, f"{round(height*100)}%", ha='center', va='bottom', fontsize=8, fontweight='bold')
    plt.tight_layout()
    return fig

# ==========================================
# 🤖 SECTION 3: STRUCTURED GEMINI API ENGINE
# ==========================================

class DroneResupplyRoute(BaseModel):
    item: str = Field(description="Name of the medicine or vaccine asset")
    from_center: str = Field(description="Name of originating supplier facility")
    to_node: str = Field(description="Target destination health center node")
    priority_level: str = Field(description="Urgency tier: CRITICAL, HIGH, or ROUTINE")
    reasoning: str = Field(description="Health justification for why this drone route was created")

class StrategicHealthMandate(BaseModel):
    early_warning_bulletin: str = Field(description="Executive emergency summary text report for district administration")
    drone_flight_manifest: List[DroneResupplyRoute] = Field(description="List of required automated UAV redistribution flights")

def generate_district_health_forecast(backend_key, inventory_df, transfer_recommendations):
    try:
        client = genai.Client(api_key=backend_key)
    except Exception as e:
        st.error("Authentication setup failure with Google Vertex.")
        return None

    system_instruction = (
        "You are an expert Public Health Operations Assistant for Andhra Pradesh health systems. "
        "Analyze facility statistics and construct flight deployment logs. "
        "You must return data matching the requested structural schema layout exactly."
    )
    
    inventory_summary = inventory_df[['node_name', 'item_name', 'current_stock', 'min_required_threshold', 'daily_avg_consumption']].to_string()
    
    prompt = f"""
    Analyze our active facility metrics:
    {inventory_summary}
    
    Algorithmic paths suggested:
    {transfer_recommendations}
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=StrategicHealthMandate,
            )
        )
        return json.loads(response.text)
    except Exception as e:
        st.error(f"Error querying Gemini API model: {str(e)}")
        return None
