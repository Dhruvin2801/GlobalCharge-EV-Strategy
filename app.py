import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SETUP ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide")
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Strategic Investment Engine</h1>", unsafe_allow_html=True)

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # We use the pre-processed CSV which already has Survival_Prob calculated
        df = pd.read_csv('streamlit_data.csv')
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Error: 'streamlit_data.csv' not found. Please upload it to your GitHub repository.")
    st.stop()

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.header("🛠️ Strategy Controls")
st.sidebar.markdown("Adjust weights to simulate Board priorities.")

w_safety = st.sidebar.slider("Weight: Resilience (Safety)", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("Weight: Growth Room", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("Weight: Wealth (GDP)", 0.0, 2.0, 1.0)

# --- 4. ROI CALCULATOR ---
# The formula: (Survival * Room * Wealth) / Saturation
# We calculate this LIVE so the sliders actually change the results
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# Select Top 10 based on the NEW score
top_targets = df.nlargest(10, 'ROI_Score')

# --- 5. DASHBOARD LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📍 Global Strategy Map")
    # Use iso_alpha if available, otherwise country names
    loc_mode = "ISO-3" if 'iso_alpha' in df.columns else "country names"
    loc_col = "iso_alpha" if 'iso_alpha' in df.columns else "country"
    
    fig_map = px.scatter_geo(
        df, 
        locations=loc_col, 
        locationmode=loc_mode if loc_mode == "ISO-3" else "country names",
        color="ROI_Score", 
        size="ROI_Score", 
        hover_name="country",
        hover_data={"Survival_Prob": ":.1%", "ROI_Score": ":.1f", "market_room": ":.1%"},
        projection="natural earth", 
        color_continuous_scale="Viridis",
        title="Investment Hotspots (Size = ROI Score)"
    )
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("💰 $100M Deployment")
    # Calculate investment split based on ROI Score
    total_score = top_targets['ROI_Score'].sum()
    top_targets['Investment ($M)'] = (top_targets['ROI_Score'] / total_score) * 100
    
    fig_pie = px.pie(
        top_targets, 
        values='Investment ($M)', 
        names='country', 
        hole=0.4, 
        color_discrete_sequence=px.colors.sequential.Greens_r,
        title="Portfolio Allocation"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 6. DETAILED TABLE ---
st.divider()
st.subheader("📋 Top 10 Investment Targets (Audit Log)")

# Format the table for display
display_cols = ['country', 'Survival_Prob', 'ROI_Score', 'Investment ($M)', 'market_room', 'infra_saturation']
st.dataframe(
    top_targets[display_cols]
    .sort_values('ROI_Score', ascending=False)
    .style.format({
        'Survival_Prob': '{:.1%}', 
        'ROI_Score': '{:.1f}', 
        'Investment ($M)': '${:.1f}M',
        'market_room': '{:.1%}',
        'infra_saturation': '{:.2f}'
    }),
    use_container_width=True
)

st.caption("Data Source: GlobalCharge Intelligence Engine (2024 Snapshot)")
