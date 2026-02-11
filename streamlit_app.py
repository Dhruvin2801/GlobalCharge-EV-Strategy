import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")

# Custom CSS for a cleaner, professional look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #18BC9C !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>⚡ GlobalCharge Strategic Investment Engine</h1>", unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    # Priority: war_room_data.csv (has comparison) > streamlit_data.csv (fallback)
    files = ['war_room_data.csv', 'streamlit_data.csv']
    for f in files:
        if os.path.exists(f):
            data = pd.read_csv(f)
            if not data.empty: return data
    return None

df = load_data()

if df is None:
    st.error("❌ CRITICAL: Data file missing or empty. Please run the 'War Room Data Script' in Colab and upload the resulting CSV.")
    st.stop()

# --- 3. SIDEBAR: BOARD MANDATES (The Parameters) ---
st.sidebar.title("💎 Strategy Mandate")
st.sidebar.markdown("Adjust weights to simulate Board priorities.")

with st.sidebar.expander("❓ What do these mean?"):
    st.write("**Resilience:** AI prediction of market survival if subsidies vanish tomorrow.")
    st.write("**Market Room:** Growth potential. High room = many petrol cars left to convert.")
    st.write("**Wealth:** Local purchasing power. Can people buy EVs without government help?")

w_safety = st.sidebar.slider("🛡️ Resilience (Safety)", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity (Growth Room)", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth (Purchasing Power)", 0.0, 2.0, 1.0)

# LIVE ROI CALCULATION
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 4. PHASE 1: GLOBAL SCAN (The Map) ---
st.subheader("🌍 Phase 1: Global ROI Heatmap")
st.markdown("Click on a country to initiate a deep-dive investigation below.")

fig_map = px.choropleth(
    df, locations="iso_alpha", color="ROI_Score",
    hover_name="country", color_continuous_scale="Viridis",
    projection="natural earth",
    hover_data={"Survival_Prob": ":.1%", "market_room": ":.1%", "ROI_Score": ":.1f"}
)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500, clickmode='event+select')

# Capture map click
selected_points = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Logic to sync map click with selection
selected_country = "USA" # Default
if selected_points and selected_points["selection"]["points"]:
    selected_country = selected_points["selection"]["points"][0]["hovertext"]

# --- 5. PHASE 2: INTELLIGENCE DEEP-DIVE ---
st.divider()
st.subheader(f"🔍 Phase 2: {selected_country} Market Intelligence")

# Ensure the country is in our list
c_list = sorted(df['country'].unique())
selected_country = st.selectbox("Current Selection (Syncs with map):", c_list, index=c_list.index(selected_country))
c_data = df[df['country'] == selected_country].iloc[0]

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Risk-Adjusted ROI", f"{c_data['ROI_Score']:.1f}")
    res_status = "✅ High Resilience" if c_data['Survival_Prob'] > 0.6 else "⚠️ Policy Dependent"
    st.metric("AI Resilience Grade", res_status, f"{c_data['Survival_Prob']:.1%}")
    st.metric("Market Room", f"{c_data['market_room']:.1%}", "Untapped Market")

with col2:
    st.markdown(f"### 🕰️ 2023 vs 2024 Audit: What Changed?")
    
    # Calculation of why ROI is what it is
    if 'EV_Share_Pct_2023' in df.columns:
        m1, m2 = st.columns(2)
        share_diff = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
        pol_diff = c_data['Policy_Score'] - c_data['Policy_Score_2023']
        
        m1.metric("Market Share Shift", f"{c_data['EV_Share_Pct']}%", f"{share_diff:+.1f}% vs 2023")
        m2.metric("Policy Support Shift", f"{c_data['Policy_Score']:.1f}", f"{pol_diff:+.1f} vs 2023")
    else:
        st.warning("Comparison data (2023) not found. Displaying current snapshot only.")

    st.markdown("### 📰 Intelligence Briefing")
    intel = {
        "Germany": "**The Subsidy Crash:** ROI rating is lower due to the Dec 2023 incentive cancellation. AI predicts high volatility as market moves from 'Hype' to 'Fundamentals'.",
        "USA": "**Trade Shielding:** ROI remains high despite 2024 tariffs on China. Internal demand is resilient due to high GDP and charging density expansion.",
        "Norway": "**Peak Saturation:** Near 90% share. While 100% resilient, the ROI is capped because the growth phase is effectively over.",
        "China": "**Price War Hub:** Extreme volumes but high competition. ROI reflects a transition from government support to private-sector dominance."
    }
    st.info(intel.get(selected_country, "ℹ️ **Market Fundamentals:** ROI is driven by organic purchasing power and infrastructure build-out. No 'Black Swan' policy events detected for this region."))

# --- 6. PHASE 3: PORTFOLIO SHOOTOUT ---
st.divider()
st.subheader("📊 Phase 3: Portfolio Shootout")
st.markdown("Compare your top prospects side-by-side to finalize the $100M deployment.")

compare_list = st.multiselect("Select Markets to Compare:", options=c_list, default=[selected_country, "USA", "Norway", "Germany"])

if compare_list:
    comp_df = df[df['country'].isin(compare_list)].sort_values('ROI_Score', ascending=False)
    
    col_c1, col_c2 = st.columns([2, 1])
    
    with col_c1:
        fig_bar = px.bar(comp_df, x='country', y='ROI_Score', color='ROI_Score', 
                         title="ROI Efficiency Battle", color_continuous_scale="Viridis")
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_c2:
        st.dataframe(
            comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room']]
            .style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}', 'ROI_Score': '{:.1f}'}),
            use_container_width=True
        )

st.caption("Data Source: GlobalCharge Proprietary ML Model (Random Forest Architecture)")
