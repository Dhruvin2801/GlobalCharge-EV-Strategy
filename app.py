import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np

# --- 1. CONFIG & STYLING ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide")
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Strategic Investment Engine</h1>", unsafe_allow_html=True)

# --- 2. DATA & MODEL LOADING ---
@st.cache_resource
def load_assets():
    df = pd.read_csv('final_merged_ev_dataset_annual.csv')
    model = joblib.load('resilience_model.pkl')
    return df, model

try:
    df, model = load_assets()
    latest_df = df[df['year'] == 2024].copy()
except Exception as e:
    st.error(f"Error loading files: {e}. Ensure CSV and PKL are in the GitHub repo.")
    st.stop()

# --- 3. THE ROLE-PLAY SIDEBAR ---
st.sidebar.image("https://img.icons8.com/color/96/electric-vehicle.png", width=80)
st.sidebar.header("🛠️ Boardroom Controls")
st.sidebar.markdown("---")

# Sliders to simulate different investment philosophies
risk_weight = st.sidebar.slider("Resilience Weight (Safety)", 0.0, 2.0, 1.0)
growth_weight = st.sidebar.slider("Opportunity Weight (Market Room)", 0.0, 2.0, 1.0)
wealth_weight = st.sidebar.slider("Purchasing Power Weight (GDP)", 0.0, 2.0, 1.0)

# --- 4. THE INTELLIGENCE ENGINE (ROI Logic) ---
# Calculate survival probability from loaded PKL
# Features used: log_gdp, Policy_Score, Gas_Price, infra_score
# Note: Ensure the features in 'latest_df' match those the model was trained on.
latest_df['Survival_Prob'] = model.predict_proba(latest_df[['log_gdp', 'Policy_Score', 'Gas_Price_USD', 'infra_score']])[:, 1]

# Custom Strategic ROI Formula
latest_df['ROI_Score'] = (
    (latest_df['Survival_Prob'] ** risk_weight) * (latest_df['market_room'] ** growth_weight) * (latest_df['GDP_per_capita'] ** (wealth_weight/2))
) / (1 + latest_df['infra_saturation'])

top_targets = latest_df.nlargest(10, 'ROI_Score')

# --- 5. INTERACTIVE VISUALS ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Global Strategy Map")
    fig_map = px.scatter_geo(latest_df, locations="iso_alpha", color="ROI_Score",
                             size="ROI_Score", hover_name="country",
                             projection="natural earth", color_continuous_scale="Viridis")
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("💰 $100M Deployment Split")
    # Allocate $100M based on relative ROI Score
    total_score = top_targets['ROI_Score'].sum()
    top_targets['Investment_Millions'] = (top_targets['ROI_Score'] / total_score) * 100
    
    fig_pie = px.pie(top_targets, values='Investment_Millions', names='country',
                     hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 6. THE BOARD'S SUMMARY TABLE ---
st.divider()
st.subheader("📋 Targeted Deployment List")
st.dataframe(
    top_targets[['country', 'Survival_Prob', 'ROI_Score', 'Investment_Millions']]
    .sort_values('ROI_Score', ascending=False)
    .style.format({'Survival_Prob': '{:.2%}', 'Investment_Millions': '${:.1f}M'}),
    use_container_width=True
)
