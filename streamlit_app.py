import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & HIGH-CONTRAST THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence War Room", layout="wide", page_icon="⚡")

# Custom UI Styling: High contrast, professional light theme
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; color: #1c2b33; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #18BC9C !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stButton>button { background-color: #18BC9C; color: white; font-weight: bold; width: 100%; border-radius: 10px; height: 3.5em; border: none; }
    .justification-box { background-color: #f1f3f6; padding: 25px; border-radius: 15px; border-left: 8px solid #18BC9C; margin-top: 20px; color: #1c2b33; line-height: 1.6; }
    .delta-positive { color: #27ae60; font-weight: bold; }
    .delta-negative { color: #e74c3c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    if os.path.exists('war_room_data.csv'):
        return pd.read_csv('war_room_data_v3.csv')
    return None

df = load_data()

if df is None:
    st.error("❌ 'war_room_data_v3.csv' missing. Please ensure the file is in your GitHub root.")
    st.stop()

# --- 3. THE INTELLIGENCE ENGINE (Geopolitical Context) ---
def get_deep_analysis(country):
    analysis = {
        "Germany": {
            "context": "The 2024 'Crisis Year'. In late 2023, a Constitutional Court ruling froze the climate fund, leading to the immediate termination of the €4,500 'Umweltbonus'.",
            "regime_shift": "Shifted from 'Hype-driven' to 'Fundamentals-driven'. 2024 sales plummeted 35% as the market reached a 'Subsidy Cliff'. Growth is now reliant on corporate fleet tax breaks.",
            "roi_reason": "ROI remains at 90.4 only due to massive GDP and existing charging density. The 'Safety' score is penalized by political flip-flopping."
        },
        "USA": {
            "context": "The year of 'Protectionist Transition'. In May 2024, the US implemented 100% tariffs on Chinese EVs to shield domestic manufacturers.",
            "regime_shift": "2023 was consumer curiosity; 2024 is infrastructure reality. The NEVI Formula Program is finally breaking ground, making the US a high-conviction 'Resilient' market.",
            "roi_reason": "High ROI driven by 'Protected Alpha' (tariffs keep Chinese competitors out) and the highest purchasing power in the dataset."
        },
        "China": {
            "context": "The 'Post-Subsidy War'. National subsidies ended in 2023. 2024 is a brutal price war led by BYD and Tesla.",
            "regime_shift": "Transitioned from 'Government-Led' to 'Oversaturated'. While 100% resilient (growth continues without aid), the profit-per-plug is shrinking.",
            "roi_reason": "ROI is capped because infrastructure is near-saturation. New capital deployment faces diminishing returns."
        },
        "Norway": {
            "context": "Mission Accomplished. Near 90% market share.",
            "regime_shift": "2024 introduced new weight-based taxes on heavy EVs to recover road tax revenue. It is no longer a growth market.",
            "roi_reason": "Low ROI justification: With no 'Market Room' left, a $100M investment has no growth runway."
        },
        "Mexico": {
            "context": "The 'Nearshoring Beneficiary'. Mexico is pivoting to satisfy USMCA supply chain requirements.",
            "regime_shift": "Shifted from 'Neglected' to 'Industrial Safe Haven'. Growth is driven by fleet electrification (DHL, Bimbo) rather than consumer whim.",
            "roi_reason": "High ROI due to 98% Market Room and industrial necessity."
        }
    }
    return analysis.get(country, {
        "context": "Standard market dynamics driven by GDP and local charging density.",
        "regime_shift": "Organic growth following the S-Curve. No major 'Black Swan' policy shocks recorded in 2024.",
        "roi_reason": "ROI is a factor of untapped market potential vs infrastructure cost."
    })

# --- 4. THE POP-UP DIALOG ---
@st.dialog("🧠 Strategic Intelligence Briefing", width="large")
def show_briefing(country_name):
    c_data = df[df['country'] == country_name].iloc[0]
    intel = get_deep_analysis(country_name)
    
    st.markdown(f"## 🏛️ {country_name}: Strategic Audit")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Classification 1: Market Stage")
        status = "🚀 TAKE-OFF" if c_data['EV_Share_Pct'] < 20 else "📈 MATURE"
        st.success(f"**Current Status:** {status}")
        st.write(f"**Justification:** {country_name} has a {c_data['EV_Share_Pct']}% share. Markets between 5-20% are the 'Golden Zone' for infrastructure ROI.")
    
    with col2:
        st.markdown("### 🤖 Classification 2: AI Resilience")
        safety = "✅ RESILIENT" if c_data['Survival_Prob'] > 0.65 else "⚠️ VULNERABLE"
        st.warning(f"**AI Confidence:** {safety}")
        st.write(f"**Justification:** Model predicts a {c_data['Survival_Prob']:.1%} survival rate in a zero-subsidy regime (The 2024 Stress Test).")

    st.divider()

    st.markdown("### 🕰️ 2023 ➔ 2024 Regime Shift Audit")
    m1, m2, m3 = st.columns(3)
    s_delta = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
    p_delta = c_data['Policy_Score'] - c_data['Policy_Score_2023']
    m1.metric("Market Share Change", f"{c_data['EV_Share_Pct']}%", f"{s_delta:+.1f}% vs 2023")
    m2.metric("Policy Support Delta", f"{c_data['Policy_Score']:.1f}", f"{p_delta:+.1f} Shift")
    m3.metric("Purchasing Power", f"${c_data['GDP_per_capita']:,.0f}", "GDP/Capita")

    st.markdown(f"""
    <div class='justification-box'>
        <h3>📰 Geopolitical & Policy Intelligence</h3>
        <p><b>Current Situation:</b> {intel['context']}</p>
        <p><b>Regime Shift Analysis:</b> {intel['regime_shift']}</p>
        <hr>
        <h3>💰 Strategic ROI Justification: {c_data['ROI_Score']:.1f}</h3>
        <p>{intel['roi_reason']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN APP INTERFACE ---
st.sidebar.title("🎮 Strategy Mandate")
w_safety = st.sidebar.slider("🛡️ Resilience Weight", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity Weight", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth Weight", 0.0, 2.0, 1.0)

# ROI MATH
df['ROI_Score'] = ((df['Survival_Prob']**w_safety) * (df['market_room']**w_room) * (df['purchasing_power']**w_wealth)) / (1+df['infra_saturation']) * 100

st.markdown("<h1 style='text-align: center;'>⚡ GlobalCharge Strategic Investment War Room</h1>", unsafe_allow_html=True)

# PHASE 1: MAP
st.subheader("🌎 Phase 1: Global Strategic Scan (Click a country to select)")
fig_map = px.choropleth(df, locations="iso_alpha", color="ROI_Score", hover_name="country", color_continuous_scale="Viridis", projection="natural earth")
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500, clickmode='event+select')

map_selection = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# PHASE 2: TRIGGER
st.divider()
st.subheader("🔍 Phase 2: Tactical Intelligence Drill-Down")

map_target = "USA"
if map_selection and map_selection["selection"]["points"]:
    map_target = map_selection["selection"]["points"][0]["hovertext"]

c_list = sorted(df['country'].unique())
selected_country = st.selectbox("Current Selection:", c_list, index=c_list.index(map_target))

if st.button(f"🔎 AUDIT {selected_country}"):
    show_briefing(selected_country)

# PHASE 3: COMPARISON
st.divider()
st.subheader("⚖️ Phase 3: Final Portfolio Shootout")
compare = st.multiselect("Select Targets for Comparison:", options=c_list, default=["USA", "Germany", "Norway"])
if compare:
    comp_df = df[df['country'].isin(compare)].sort_values('ROI_Score', ascending=False)
    st.bar_chart(comp_df.set_index('country')['ROI_Score'])
    st.dataframe(comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room', 'GDP_per_capita']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
