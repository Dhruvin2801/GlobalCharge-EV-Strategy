import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .main { background-color: #0b0f1a; color: #e8edf5; }
    .stMetric { background-color: #111827; padding: 15px; border-radius: 12px; border: 1px solid #1e2d45; }
    h1, h2, h3 { color: #00d4aa !important; }
    .stButton>button { background-color: #00d4aa; color: black; font-weight: bold; width: 100%; border-radius: 25px; }
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
    st.error("❌ 'war_room_data_v3.csv' missing. Upload it to GitHub.")
    st.stop()

# --- 3. THE POP-UP DIALOG ENGINE ---
@st.dialog("🧠 Market Intelligence Briefing", width="large")
def show_intelligence(country_name):
    row = df[df['country'] == country_name].iloc[0]
    
    st.subheader(f"Strategic Audit: {country_name}")
    
    # 1. TWO CLASSIFICATIONS & JUSTIFICATION
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🛡️ Classification 1: Market Maturity**")
        status = "🚀 Takeoff" if row['EV_Share_Pct'] < 20 else "📈 Mature"
        st.info(f"**Status: {status}**\n\n**Justification:** Based on S-Curve theory. {country_name} currently has a {row['EV_Share_Pct']}% share, placing it in the {status.lower()} phase.")
    with c2:
        st.markdown("**🤖 Classification 2: AI Resilience**")
        safety = "✅ Safe Haven" if row['Survival_Prob'] > 0.6 else "⚠️ High Risk"
        st.warning(f"**Grade: {safety}**\n\n**Justification:** Random Forest model predicts a {row['Survival_Prob']:.1%} survival probability in a zero-subsidy regime.")

    st.divider()
    
    # 2. 2023 VS 2024 DIFFERENCE
    st.markdown("### 🕰️ Regime Shift Analysis (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    
    s_diff = row['EV_Share_Pct'] - row['EV_Share_Pct_2023']
    p_diff = row['Policy_Score'] - row['Policy_Score_2023']
    
    m1.metric("Market Share", f"{row['EV_Share_Pct']}%", f"{s_diff:+.1f}% vs 2023")
    m2.metric("Gov Support", f"{row['Policy_Score']:.1f}", f"{p_diff:+.1f} vs 2023")
    m3.metric("AI Confidence", f"{row['Survival_Prob']:.1%}", "Resilience")

    # 3. WHY & REAL WORLD EVENTS
    st.markdown("### 📰 Why is this happening?")
    briefings = {
        "Germany": "**⚠️ The Subsidy Crash:** ROI rating reflects the Dec 2023 'Umweltbonus' cancellation. The AI correctly predicted the 35% sales drop in early 2024. The market is now struggling to transition to organic growth.",
        "USA": "**🛡️ Trade War Shielding:** 100% tariffs on Chinese imports implemented in May 2024 protects domestic margins. ROI is driven by infrastructure build-out and federal IRA tax credits.",
        "Norway": "**✅ Market Saturation:** Structural resilience is 100%, but ROI is capped. With 90% share, there is zero 'Market Room' left for high-alpha deployment. This is now a low-yield maintenance zone.",
        "China": "**🏭 Post-Subsidy Consolidation:** Market has shifted from government aid to extreme price wars. High volume exists, but over-saturation in charging stations reduces the ROI for new capital.",
        "Mexico": "**📈 Nearshoring Alpha:** Growth is driven by commercial fleet electrification to comply with USMCA supply chain rules. This is immune to consumer subsidy shocks."
    }
    st.success(briefings.get(country_name, "ℹ️ **Market Fundamentals:** Trajectory is governed by local purchasing power and charging density expansion. No major policy black-swan events recorded in the 2024 audit window."))

    # 4. ROI JUSTIFICATION
    st.markdown(f"### 💰 Final ROI Justification: **{row['ROI_Score']:.1f}**")
    st.write(f"The score for {country_name} is derived from its high GDP per capita (${row['GDP_per_capita']:,.0f}) which ensures sustainable buying power, balanced against its current charging plug density.")

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center;'>⚡ GlobalCharge Strategic Investment Engine</h1>", unsafe_allow_html=True)

# SIDEBAR CONTROLS
st.sidebar.title("💎 Strategy Console")
w_safety = st.sidebar.slider("🛡️ Resilience", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth", 0.0, 2.0, 1.0)

# LIVE ROI MATH
df['ROI_Score'] = ((df['Survival_Prob']**w_safety) * (df['market_room']**w_room) * (df['purchasing_power']**w_wealth)) / (1+df['infra_saturation']) * 100

# PHASE 1: MAP
st.subheader("Phase 1: Global Scan (Click a country to select)")
fig_map = px.choropleth(df, locations="iso_alpha", color="ROI_Score", hover_name="country", color_continuous_scale="Viridis", projection="natural earth")
fig_map.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0}, clickmode='event+select')

# The Interactive Trigger
selected_map = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Sync selection logic
map_target = "USA"
if selected_map and selected_map["selection"]["points"]:
    map_target = selected_map["selection"]["points"][0]["hovertext"]

st.divider()

# PHASE 2: DRILL DOWN
st.subheader("Phase 2: Tactical Intelligence Briefing")
col_l, col_r = st.columns([1, 2])
with col_l:
    c_list = sorted(df['country'].unique())
    selected_country = st.selectbox("Current Selection:", c_list, index=c_list.index(map_target))
    if st.button(f"🔍 Audit {selected_country}"):
        show_intelligence(selected_country)
with col_r:
    st.info("💡 **INTERACTIVE:** Click a country on the map above, then click the **'Audit'** button here to launch the full Strategic Briefing Pop-up.")

# PHASE 3: COMPARISON
st.divider()
st.subheader("Phase 3: Portfolio Asset Comparison")
compare = st.multiselect("Select Markets to Compare:", options=c_list, default=["USA", "Germany", "Norway"])
if compare:
    comp_df = df[df['country'].isin(compare)].sort_values('ROI_Score', ascending=False)
    st.bar_chart(comp_df.set_index('country')['ROI_Score'])
    st.dataframe(comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room', 'GDP_per_capita']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
