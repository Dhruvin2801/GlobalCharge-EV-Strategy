import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SETUP ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Strategic Intelligence Engine</h1>", unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv('streamlit_data_v2.csv')
    except: return None

df = load_data()
if df is None:
    st.error("⚠️ Error: Please upload 'streamlit_data_v2.csv' to GitHub.")
    st.stop()

# --- 3. SIDEBAR: BOARD MANDATES (PARAMETERS) ---
st.sidebar.title("💎 Strategy Mandate")
w_safety = st.sidebar.slider("🛡️ Resilience (Safety)", 0.0, 2.0, 1.0)
st.sidebar.info("**Resilience:** AI's prediction of market survival during 2024-style policy crashes.")

w_room = st.sidebar.slider("📈 Opportunity (Growth Room)", 0.0, 2.0, 1.0)
st.sidebar.info("**Market Room:** Untapped potential. High weight avoids saturated markets like Norway.")

w_wealth = st.sidebar.slider("💰 Wealth (Purchasing Power)", 0.0, 2.0, 1.0)
st.sidebar.info("**Wealth:** Measures if the local economy can buy EVs without government subsidies.")

# LIVE ROI MATH
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 4. TABS ---
tab_map, tab_compare = st.tabs(["🌍 Strategic Map & Deep Dive", "📊 Portfolio Comparison"])

with tab_map:
    # Tableau-style Choropleth
    st.subheader("Global ROI Heatmap (Click a country to select)")
    fig_map = px.choropleth(
        df, locations="iso_alpha", color="ROI_Score",
        hover_name="country", color_continuous_scale="Viridis",
        projection="natural earth", labels={'ROI_Score': 'Strategic Rating'}
    )
    fig_map.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    
    # Selection logic: Click map or use dropdown fallback
    selected_points = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")
    
    selected_country = "USA" # Default
    if selected_points and selected_points["selection"]["points"]:
        selected_country = selected_points["selection"]["points"][0]["hovertext"]
    
    c_list = sorted(df['country'].unique())
    selected_country = st.selectbox("Current Selection:", c_list, index=c_list.index(selected_country))
    
    # 5. COUNTRY DEEP DIVE
    st.divider()
    c_data = df[df['country'] == selected_country].iloc[0]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"Profile: {selected_country}")
        st.metric("Final Strategic ROI", f"{c_data['ROI_Score']:.1f}")
        st.metric("AI Resilience Grade", "Resilient ✅" if c_data['Survival_Prob'] > 0.6 else "Vulnerable ⚠️", f"{c_data['Survival_Prob']:.1%}")
        st.metric("Market Stage", "Early Takeoff 🚀" if c_data['EV_Share_Pct'] < 15 else "Mature Phase 📈", f"{c_data['EV_Share_Pct']}% Share")

    with col2:
        st.subheader("🕰️ Time Audit (2023 vs 2024)")
        m1, m2, m3 = st.columns(3)
        share_diff = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
        m1.metric("Market Share Shift", f"{c_data['EV_Share_Pct']}%", f"{share_diff:+.1f}% vs 2023")
        
        pol_diff = c_data['Policy_Score'] - c_data['Policy_Score_2023']
        m2.metric("Policy Environment", f"{c_data['Policy_Score']:.1f}", f"{pol_diff:+.1f} Support Shift")
        
        m3.metric("Purchasing Power", f"${c_data['GDP_per_capita']:,.0f}")
        
        # Real World Context Logic
        st.markdown("### 📰 Intelligence Briefing")
        context = {
            "Germany": "**⚠️ 2024 Subsidy Crash:** Germany abruptly ended its 'Umweltbonus' in late 2023. Our model correctly predicted the resulting 35% collapse in non-fleet sales.",
            "USA": "**🛡️ Tariff Shielding:** 2024 implementation of 100% tariffs on Chinese imports. Growth is now internally driven by IRA credits and charging density.",
            "China": "**🏭 Saturation War:** Hyper-competition and price wars. High resilience, but 'Market Room' is decreasing rapidly.",
            "Norway": "**✅ Mature Ecosystem:** Past the investment peak. Structural resilience is high, but growth alpha is low for new capital."
        }
        st.info(context.get(selected_country, "ℹ️ **Market Fundamentals:** Trajectory driven by local infrastructure pace and organic purchasing power. No extreme black-swan events recorded."))

# --- TAB 2: COMPARISON ---
with tab_compare:
    st.subheader("⚖️ Side-by-Side Asset Comparison")
    compare_list = st.multiselect("Select Assets for Comparison:", options=c_list, default=["USA", "Germany", "Switzerland", "Australia"])
    
    if compare_list:
        comp_df = df[df['country'].isin(compare_list)]
        
        # Visual 1: ROI Battle
        fig_bar = px.bar(comp_df, x='country', y='ROI_Score', color='country', title="Risk-Adjusted Strategic Value")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Visual 2: Data Grid
        st.dataframe(comp_df[['country', 'Survival_Prob', 'market_room', 'purchasing_power', 'ROI_Score']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
