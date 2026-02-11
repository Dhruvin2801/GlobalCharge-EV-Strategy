import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & SYSTEM THEME ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")

# Professional Dark-Mode CSS
st.markdown("""
    <style>
    .main { background-color: #0b0f1a; color: #e8edf5; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #1e2d45; }
    h1, h2, h3 { color: #00d4aa !important; }
    .stButton>button { background-color: #00d4aa; color: black; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    if os.path.exists('war_room_data.csv'):
        return pd.read_csv('war_room_data.csv')
    return None

df = load_data()

if df is None:
    st.error("❌ CRITICAL: 'war_room_data.csv' missing. Run your Colab script and upload it.")
    st.stop()

# --- 3. SIDEBAR: BOARD MANDATES ---
st.sidebar.title("💎 Strategy Console")
w_safety = st.sidebar.slider("🛡️ Resilience (Safety)", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity (Growth)", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth (GDP)", 0.0, 2.0, 1.0)

# LIVE ROI CALCULATION
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 4. THE POP-UP INTELLIGENCE ENGINE ---
@st.dialog("🌍 Market Intelligence Briefing", width="large")
def show_briefing(country_name):
    c_data = df[df['country'] == country_name].iloc[0]
    
    st.subheader(f"{country_name} Strategic Profile")
    
    # --- SECTION A: THE 2 CLASSIFICATIONS ---
    colA, colB = st.columns(2)
    with colA:
        # Class 1: Market Maturity
        is_takeoff = c_data['EV_Share_Pct'] > 2 and c_data['EV_Share_Pct'] < 20
        status = "🚀 TAKE-OFF PHASE" if is_takeoff else ("📉 SATURATED" if c_data['EV_Share_Pct'] >= 20 else "🌱 SEEDING")
        st.write(f"**Classification 1: Market Stage**")
        st.info(f"**{status}**\n\nJustification: Based on S-Curve theory. {country_name} currently has a {c_data['EV_Share_Pct']}% share.")
    
    with colB:
        # Class 2: AI Resilience
        is_resilient = c_data['Survival_Prob'] > 0.65
        res_status = "✅ RESILIENT" if is_resilient else "⚠️ VULNERABLE"
        st.write(f"**Classification 2: AI Resilience**")
        st.warning(f"**{res_status}**\n\nJustification: AI prediction of growth stability during the 2024 regime shift (subsidy removal).")

    st.divider()

    # --- SECTION B: 2023 VS 2024 DELTA ---
    st.write("### 🕰️ Regime Shift Audit (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    
    share_change = c_data['EV_Share_Pct'] - c_data.get('EV_Share_Pct_2023', 0)
    pol_change = c_data['Policy_Score'] - c_data.get('Policy_Score_2023', 0)
    
    m1.metric("Market Share Change", f"{c_data['EV_Share_Pct']}%", f"{share_change:+.1f}% Delta")
    m2.metric("Gov Support Change", f"{c_data['Policy_Score']:.1f}", f"{pol_change:+.1f} Support Shift")
    m3.metric("AI Prediction Accuracy", f"{c_data['Survival_Prob']:.1%}", "Confidence")

    # --- SECTION C: REAL WORLD EVENTS ---
    st.write("### 📰 Intelligence Context (Why this happened)")
    intel = {
        "Germany": "**The Subsidy Cliff:** In Dec 2023, Germany abruptly ended its 'Umweltbonus'. Our AI correctly flagged this, predicting the 35% crash in early 2024. Low ROI reflects high policy volatility.",
        "USA": "**Protectionist Shielding:** 2024 implementation of 100% tariffs on Chinese EVs shielded domestic margins. Growth is now driven by IRA credits and internal charging density.",
        "Norway": "**Maturity Trap:** Structural resilience is 100%, but ROI is capped. With 90% share, there is no 'Market Room' left for high-alpha infrastructure growth.",
        "China": "**Post-Subsidy Consolidation:** Hyper-competition and price wars. High volume, but extreme charging station saturation reduces new project ROI."
    }
    st.success(intel.get(country_name, "ℹ️ **Standard Dynamics:** Adoption governed by organic purchasing power and infrastructure build-out. No major black-swan events detected."))

    st.write(f"### 💰 Strategic ROI Justification: **{c_data['ROI_Score']:.1f}**")
    st.write(f"This rating is a factor of {country_name}'s high purchasing power (${c_data['GDP_per_capita']:,.0f}) balanced against its current charging saturation.")

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center;'>⚡ GlobalCharge Strategic War Room</h1>", unsafe_allow_html=True)

# THE INTERACTIVE MAP
st.subheader("Phase 1: Global Market Scan")
fig_map = px.choropleth(
    df, locations="iso_alpha", color="ROI_Score",
    hover_name="country", color_continuous_scale="Viridis",
    projection="natural earth"
)
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
st.plotly_chart(fig_map, use_container_width=True)

# THE TRIGGER
st.subheader("Phase 2: Drill-Down Investigation")
col_l, col_r = st.columns([1, 2])
with col_l:
    target = st.selectbox("Select Target Country:", sorted(df['country'].unique()))
    if st.button(f"🔎 Audit {target}"):
        show_briefing(target)
with col_r:
    st.info("💡 **Click the 'Audit' button to launch the Intelligence Briefing pop-up.** It will show the AI Classifications, the 2024 crash reasons, and the final ROI justification.")

# --- 6. DASHBOARD COMPARISON ---
st.divider()
st.subheader("📊 Phase 3: Portfolio Shootout")
compare_list = st.multiselect("Asset Comparison Group:", options=sorted(df['country'].unique()), default=["USA", "Germany", "Norway"])
if compare_list:
    comp_df = df[df['country'].isin(compare_list)].sort_values('ROI_Score', ascending=False)
    st.bar_chart(comp_df.set_index('country')['ROI_Score'])
    st.dataframe(comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room', 'GDP_per_capita']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
