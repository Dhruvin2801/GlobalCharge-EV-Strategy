import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")

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

# --- 3. THE POP-UP ENGINE ---
@st.dialog("🧠 Market Intelligence Pop-up", width="large")
def show_briefing(target):
    data = df[df['country'] == target].iloc[0]
    
    st.subheader(f"Strategic Audit: {target}")
    
    # 2 Classifications
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**1. Market Lifecycle**")
        status = "🚀 Takeoff" if data['EV_Share_Pct'] < 20 else "📈 Mature"
        st.info(f"**{status}**\n\nJustification: Based on S-Curve analysis. Current share is {data['EV_Share_Pct']}%.")
    with c2:
        st.markdown("**2. AI Resilience Grade**")
        safety = "✅ Safe" if data['Survival_Prob'] > 0.6 else "⚠️ Volatile"
        st.warning(f"**{safety}**\n\nJustification: Random Forest predicts {data['Survival_Prob']:.1%} survival in subsidy-free environments.")

    st.divider()
    
    # 2023 vs 2024 Change
    st.markdown("### 🕰️ 2023 ➔ 2024 Regime Shift")
    m1, m2 = st.columns(2)
    share_diff = data['EV_Share_Pct'] - data['EV_Share_Pct_2023']
    pol_diff = data['Policy_Score'] - data['Policy_Score_2023']
    
    m1.metric("Market Share Delta", f"{data['EV_Share_Pct']}%", f"{share_diff:+.1f}% shift")
    m2.metric("Policy Support Delta", f"{data['Policy_Score']:.1f}", f"{pol_diff:+.1f} points")

    # Why & Real World Events
    st.markdown("### 📰 Why is this happening?")
    events = {
        "Germany": "Abrupt cancellation of EV subsidies in late 2023 caused a 35% sales crash. High GDP but low resilience score due to political flip-flops.",
        "USA": "100% tariffs on Chinese imports implemented in 2024 protects domestic margins. ROI is driven by infrastructure build-out and IRA credits.",
        "Norway": "Market saturation reached. Zero 'Market Room' for new explosive growth, but 100% resilient. A low-ROI 'Maintenance' zone.",
        "China": "Intense price wars and charging over-saturation. Massive volumes but thinning profit margins per charging plug."
    }
    st.info(events.get(target, "Trajectory is driven by organic purchasing power and charging density. No major black-swan events detected."))

    # ROI Justification
    st.markdown(f"### 💰 ROI Justification: **{data['ROI_Score']:.1f}**")
    st.write(f"Rating reflects high purchasing power (${data['GDP_per_capita']:,.0f}) vs infrastructure cost.")

# --- 4. MAIN INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Strategic Intelligence Engine</h1>", unsafe_allow_html=True)

# SIDEBAR PARAMETERS
st.sidebar.title("💎 Strategy Console")
w_safety = st.sidebar.slider("🛡️ Resilience", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth", 0.0, 2.0, 1.0)

# LIVE MATH
df['ROI_Score'] = ((df['Survival_Prob']**w_safety) * (df['market_room']**w_room) * (df['purchasing_power']**w_wealth)) / (1+df['infra_saturation']) * 100

# TAB 1: THE MAP & DRILL-DOWN
st.subheader("Phase 1: Global Scan")
fig_map = px.choropleth(df, locations="iso_alpha", color="ROI_Score", hover_name="country", color_continuous_scale="Viridis", projection="natural earth")
fig_map.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})

# Capture selection
selected_map = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

st.divider()

# TAB 2: TRIGGER
st.subheader("Phase 2: Deep-Dive Audit")
# Logic to sync map click
map_country = "USA"
if selected_map and selected_map["selection"]["points"]:
    map_country = selected_map["selection"]["points"][0]["hovertext"]

c_list = sorted(df['country'].unique())
selected_country = st.selectbox("Current Selection:", c_list, index=c_list.index(map_country))

if st.button(f"🔎 Launch {selected_country} Intelligence Pop-up"):
    show_briefing(selected_country)

# TAB 3: DASHBOARD
st.divider()
st.subheader("Phase 3: Multi-Market Comparison")
compare = st.multiselect("Select Assets:", c_list, default=["USA", "Germany", "Norway"])
if compare:
    comp_df = df[df['country'].isin(compare)]
    st.bar_chart(comp_df.set_index('country')['ROI_Score'])
    st.dataframe(comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
