import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px # Ensure plotly is in requirements.txt

# 1. ASSET LOADING
@st.cache_data
def load_data():
    df = pd.read_csv('war_room_audit_2025.csv')
    # Add coordinates for the map (Streamlit needs 'lat' and 'lon')
    # If your CSV doesn't have them, st.map won't work, so we use Plotly Choropleth
    return df

df_audit = load_data()

# 2. UI HEADER (No Chef Icon)
st.set_page_config(page_title="GlobalCharge Audit", layout="wide")
st.title("🛡️ GlobalCharge: Regime-Aware Strategic Audit")

# 3. THE WORLD MAP (Restored)
st.subheader("Global Risk Map (New Model Intelligence)")
# Using Plotly for a professional financial map
fig = px.choropleth(df_audit, 
                    locations="Country", 
                    locationmode='country names',
                    color="New_Prob_Pct", 
                    hover_name="Country",
                    color_continuous_scale="RdYlGn",
                    title="AI Confidence Scores (78% Threshold Applied)")
st.plotly_chart(fig, use_container_width=True)

# 4. DYNAMIC FILTERING (The 78% Logic)
st.sidebar.title("Audit Controls")
margin = st.sidebar.slider("Margin of Safety (%)", 50, 95, 78)

# Re-calculate action based on sidebar live
df_audit['Current_Action'] = df_audit['New_Prob_Pct'].apply(lambda x: "🟢 DEPLOY" if x >= margin else "🔴 VETO")

# 5. TABLES & DEEP DIVE
tab1, tab2 = st.tabs(["Investment Tiers", "Market Deep-Dive"])

with tab1:
    st.dataframe(df_audit[['Country', 'Current_Action', 'ROI_Score', 'New_Prob_Pct']].sort_values('ROI_Score', ascending=False), use_container_width=True)

with tab2:
    target = st.selectbox("Select Country:", df_audit['Country'].unique())
    row = df_audit[df_audit['Country'] == target].iloc[0]
    
    col1, col2 = st.columns(2)
    col1.metric("AI Confidence", f"{row['New_Prob_Pct']}%")
    col2.metric("Decision", row['Current_Action']) # Fixed the KeyError here
    
    if target == "Germany":
        st.error("Political Shock Alert: Human Veto recommended due to 2024 subsidy cuts.")
    elif target == "India":
        st.info(f"Value Opportunity: Large Opportunity Gap detected ({row['Opportunity_Gap']:.2f}).")
