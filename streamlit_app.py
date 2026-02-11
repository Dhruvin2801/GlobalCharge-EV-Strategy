import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & SYSTEM THEME ---
st.set_page_config(page_title="GlobalCharge Strategic War Room", layout="wide", page_icon="⚡")

# Custom UI Styling (No dark blocks, high-contrast text)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; color: #212529; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #dee2e6; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #18BC9C !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stButton>button { background-color: #18BC9C; color: white; font-weight: bold; width: 100%; border-radius: 8px; border: none; height: 3em; }
    .info-card { background-color: #e9ecef; padding: 20px; border-radius: 12px; border-left: 5px solid #18BC9C; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    if os.path.exists('war_room_data_v3.csv'):
        return pd.read_csv('war_room_data_v3.csv')
    return None

df = load_data()

if df is None:
    st.error("❌ DATA ERROR: 'war_room_data_v3.csv' not found. Please upload it to your GitHub root.")
    st.stop()

# --- 3. SIDEBAR: BOARD OF DIRECTORS CONSOLE ---
st.sidebar.title("🎮 Strategy Mandate")
st.sidebar.markdown("Adjust Board priorities to re-calculate global ROI.")

w_safety = st.sidebar.slider("🛡️ Resilience (Safety)", 0.0, 2.0, 1.0, help="Weights the AI prediction of growth stability if government subsidies are removed.")
w_room = st.sidebar.slider("📈 Opportunity (Market Room)", 0.0, 2.0, 1.0, help="Weights the untapped population potential (ICE vehicles yet to convert).")
w_wealth = st.sidebar.slider("💰 Wealth (GDP per Capita)", 0.0, 2.0, 1.0, help="Weights the organic ability of consumers to afford EVs without state aid.")

# LIVE ROI RE-CALCULATION
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 4. THE INTELLIGENCE POP-UP ENGINE ---
@st.dialog("🧠 Strategic Intelligence Briefing", width="large")
def show_briefing(country_name):
    c_data = df[df['country'] == country_name].iloc[0]
    
    st.markdown(f"## 🏛️ {country_name} Audit Report")
    
    # 1. THE TWO CLASSIFICATIONS
    colA, colB = st.columns(2)
    with colA:
        st.markdown("### 📊 Classification 1: Market Maturity")
        status = "🚀 Takeoff Phase" if c_data['EV_Share_Pct'] < 20 else "📈 Mature Market"
        st.success(f"**Current Status:** {status}")
        st.write(f"**Justification:** Based on S-Curve diffusion. {country_name} has a {c_data['EV_Share_Pct']}% market share. Markets under 20% offer the highest 'Alpha' for new infrastructure growth.")
    
    with colB:
        st.markdown("### 🤖 Classification 2: AI Resilience")
        safety = "✅ Resilient" if c_data['Survival_Prob'] > 0.65 else "⚠️ Policy Dependent"
        st.warning(f"**Resilience Grade:** {safety}")
        st.write(f"**Justification:** Our Random Forest model predicts a {c_data['Survival_Prob']:.1%} chance of sustained growth without state aid, based on historical 2024 regime-shift data.")

    st.divider()

    # 2. 2023 VS 2024 REGIME SHIFT
    st.markdown("### 🕰️ Regime Shift Audit: What changed in 2024?")
    m1, m2, m3 = st.columns(3)
    
    share_change = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
    pol_change = c_data['Policy_Score'] - c_data['Policy_Score_2023']
    
    m1.metric("Market Share Delta", f"{c_data['EV_Share_Pct']}%", f"{share_change:+.1f}% vs 2023")
    m2.metric("Policy Score Delta", f"{c_data['Policy_Score']:.1f}", f"{pol_change:+.1f} Support Shift")
    m3.metric("AI Prediction Accuracy", f"{c_data['Survival_Prob']:.1%}", "Confidence")

    # 3. THE "WHY" - GEOPOLITICS & POLICY
    st.markdown("### 📰 Geopolitical & Policy Context")
    intel_briefings = {
        "Germany": "**⚠️ The Subsidy Cliff:** In late 2023, the 'Umweltbonus' was abruptly terminated due to a constitutional court budget ruling. This caused a massive 2024 sales crash. Our AI ROI rating is suppressed here due to extreme political volatility.",
        "USA": "**🛡️ Trade Protectionism:** The 2024 implementation of 100% tariffs on Chinese EVs (Section 301) has shielded domestic price margins. ROI is driven by long-term IRA tax credits and a national push for charging density.",
        "Norway": "**✅ The Saturation Trap:** Norway is the most resilient market globally, but ROI is low because it has already 'completed the mission.' Growth has plateaued; our $100M finds more 'Alpha' elsewhere.",
        "China": "**🏭 Post-Subsidy Consolidation:** China removed national subsidies in 2023. The 2024 market is now a brutal price war. High volume exists, but charging station over-saturation limits our ROI per plug.",
        "Mexico": "**📈 USMCA Nearshoring:** Growth is driven by commercial fleet mandates and manufacturing nearshoring. Mexico is becoming a 'Safe Haven' because its growth is industrial, not dependent on fickle consumer subsidies."
    }
    st.markdown(f"<div class='info-card'>{intel_briefings.get(country_name, 'ℹ️ **Fundamental Growth:** This market is currently driven by organic purchasing power and infrastructure build-out. No major black-swan policy shocks were recorded in the 2024 audit window.')}</div>", unsafe_allow_html=True)

    # 4. ROI JUSTIFICATION
    st.markdown(f"### 💰 Strategic ROI Justification: **{c_data['ROI_Score']:.1f}**")
    st.write(f"This rating is a product of {country_name}'s high Purchasing Power (${c_data['GDP_per_capita']:,.0f}) which ensures sustainable transition, balanced against the risk of policy withdrawal and current infra saturation.")

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center;'>⚡ GlobalCharge Strategic Investment Engine</h1>", unsafe_allow_html=True)

# Phase 1: Global Scan
st.subheader("🌎 Phase 1: Identify High-ROI Strategic Assets")
fig_map = px.choropleth(
    df, locations="iso_alpha", color="ROI_Score",
    hover_name="country", color_continuous_scale="Viridis",
    projection="natural earth",
    hover_data={"Survival_Prob": ":.1%", "market_room": ":.1%", "ROI_Score": ":.1f"}
)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500, clickmode='event+select')
map_selection = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Phase 2: The Drill-Down
st.divider()
st.subheader("🔍 Phase 2: Tactical Intelligence Audit")

# Sync selection logic
current_target = "USA"
if map_selection and map_selection["selection"]["points"]:
    current_target = map_selection["selection"]["points"][0]["hovertext"]

c_list = sorted(df['country'].unique())
selected_country = st.selectbox("Current Selection:", c_list, index=c_list.index(current_target))

if st.button(f"🔍 Launch {selected_country} Deep-Dive Audit"):
    show_briefing(selected_country)

# Phase 3: Shootout
st.divider()
st.subheader("⚖️ Phase 3: Final Portfolio Asset Comparison")
compare = st.multiselect("Select Markets to Compare Side-by-Side:", options=c_list, default=["USA", "Germany", "Norway", "Mexico"])
if compare:
    comp_df = df[df['country'].isin(compare)].sort_values('ROI_Score', ascending=False)
    st.bar_chart(comp_df.set_index('country')['ROI_Score'])
    st.dataframe(comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room', 'GDP_per_capita']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}', 'ROI_Score': '{:.1f}'}), use_container_width=True)

st.caption("Intelligence powered by GlobalCharge Proprietary Random Forest Model · Audit Cycle: 2023-2024")
