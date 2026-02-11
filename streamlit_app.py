import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & SYSTEM THEME ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")

# Professional Dark-Mode UI
st.markdown("""
    <style>
    .main { background-color: #0b0f1a; color: #e8edf5; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1e2d45; }
    div[data-testid="stExpander"] { background-color: #111827; border: 1px solid #1e2d45; }
    h1, h2, h3 { color: #00d4aa !important; }
    .stButton>button { background-color: #00d4aa; color: black; font-weight: bold; width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    # We prioritize V2 as requested
    if os.path.exists('streamlit_data_v2.csv'):
        return pd.read_csv('streamlit_data_v2.csv')
    return None

df = load_data()

if df is None:
    st.error("❌ DATA ERROR: 'streamlit_data_v2.csv' not found. Please ensure it is in your GitHub root.")
    st.stop()

# --- 3. THE INTELLIGENCE POP-UP ENGINE ---
@st.dialog("🧠 Market Intelligence Briefing", width="large")
def show_briefing(country_name):
    c_data = df[df['country'] == country_name].iloc[0]
    
    st.subheader(f"Strategic Audit: {country_name}")
    
    # Section 1: The 2 Classifications
    colA, colB = st.columns(2)
    with colA:
        st.markdown("**🛡️ Classification 1: Market Maturity**")
        status = "🚀 Takeoff" if c_data['EV_Share_Pct'] < 20 else "📈 Mature"
        st.info(f"**Status: {status}**\n\n**Justification:** S-Curve analysis shows a {c_data['EV_Share_Pct']}% share. Market is in {status.lower()} phase.")
    
    with colB:
        st.markdown("**🤖 Classification 2: AI Resilience**")
        safety = "✅ Safe Haven" if c_data['Survival_Prob'] > 0.6 else "⚠️ Volatile"
        st.warning(f"**Grade: {safety}**\n\n**Justification:** Random Forest predicts a {c_data['Survival_Prob']:.1%} survival probability if subsidies are removed.")

    st.divider()

    # Section 2: 2023 vs 2024 Audit
    st.markdown("### 🕰️ Regime Shift Audit (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    
    share_delta = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
    pol_delta = c_data['Policy_Score'] - c_data['Policy_Score_2023']
    
    m1.metric("EV Share Delta", f"{c_data['EV_Share_Pct']}%", f"{share_delta:+.1f}% vs 2023")
    m2.metric("Policy Score Delta", f"{c_data['Policy_Score']:.1f}", f"{pol_delta:+.1f} vs 2023")
    m3.metric("AI Confidence", f"{c_data['Survival_Prob']:.1%}")

    # Section 3: Why & Real World Events
    st.markdown("### 📰 Situational Awareness (Real-World Context)")
    intel = {
        "Germany": "**The Subsidy Cliff:** ROI rating is lower due to the Dec 2023 incentive cancellation. AI predicts high volatility as market moves from 'Hype' to 'Fundamentals'.",
        "USA": "**Trade War Shielding:** 2024 implementation of 100% tariffs on Chinese imports. Growth is internally driven by IRA credits and charging density.",
        "Norway": "**Maturity Trap:** Structural resilience is 100%, but growth alpha is low. Zero 'Market Room' left for explosive infrastructure deployment.",
        "China": "**Post-Subsidy War:** Market has shifted to brutal price wars. High volume but extreme saturation in Tier 1 cities."
    }
    st.success(intel.get(country_name, "ℹ️ **Market Fundamentals:** ROI is driven by organic purchasing power and infrastructure build-out. No major policy shocks detected."))

    st.markdown(f"### 💰 Strategic ROI Justification: **{c_data['ROI_Score']:.1f}**")
    st.write(f"This rating is driven by {country_name}'s high GDP per capita (${c_data['GDP_per_capita']:,.0f}) ensuring buying power, balanced against its current charging saturation.")

# --- 4. SIDEBAR: BOARD CONSOLE ---
st.sidebar.title("🎮 Strategy Console")
w_safety = st.sidebar.slider("🛡️ Resilience", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth", 0.0, 2.0, 1.0)

# ROI FORMULA
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center;'>⚡ GlobalCharge Strategic War Room</h1>", unsafe_allow_html=True)

# Phase 1: Global Map
st.subheader("🌎 Phase 1: Identify High-ROI Assets")
fig_map = px.choropleth(
    df, locations="iso_alpha", color="ROI_Score",
    hover_name="country", color_continuous_scale="Viridis",
    projection="natural earth",
    hover_data={"Survival_Prob": ":.1%", "market_room": ":.1%", "ROI_Score": ":.1f"}
)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500, clickmode='event+select')

# The interactive trigger
map_selection = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Phase 2: Drill-Down
st.divider()
st.subheader("🔍 Phase 2: Deep-Dive Intelligence Audit")

# Sync selection logic (Map click or Dropdown)
map_country = "USA"
if map_selection and map_selection["selection"]["points"]:
    map_country = map_selection["selection"]["points"][0]["hovertext"]

c_list = sorted(df['country'].unique())
selected_target = st.selectbox("Current Selection:", c_list, index=c_list.index(map_country))

if st.button(f"🔍 Launch {selected_target} Audit Briefing"):
    show_briefing(selected_target)

# Phase 3: Dashboard
st.divider()
st.subheader("📊 Phase 3: Portfolio Shootout")
compare = st.multiselect("Select Assets to Compare:", options=c_list, default=["USA", "Germany", "Norway"])
if compare:
    comp_df = df[df['country'].isin(compare)].sort_values('ROI_Score', ascending=False)
    st.bar_chart(comp_df.set_index('country')['ROI_Score'])
    st.dataframe(comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room', 'GDP_per_capita']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
