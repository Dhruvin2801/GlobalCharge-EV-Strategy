import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. SETUP ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Strategic Intelligence Engine</h1>", unsafe_allow_html=True)

# --- DEBUG: FILE CHECKER ---
# This helps you see why the file isn't loading
files_in_repo = os.listdir(".")
if 'streamlit_data_v2.csv' not in files_in_repo:
    st.error(f"❌ File 'streamlit_data_v2.csv' not found in root directory!")
    st.write("Files I can see in your GitHub:")
    st.write(files_in_repo)
    st.stop()

# --- 2. LOAD DATA ---
@st.cache_data
def load_data():
    return pd.read_csv('streamlit_data_v2.csv')

df = load_data()

# --- 3. SIDEBAR: BOARD MANDATES ---
st.sidebar.title("💎 Strategy Mandate")
w_safety = st.sidebar.slider("🛡️ Resilience (Safety)", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity (Growth Room)", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth (Purchasing Power)", 0.0, 2.0, 1.0)

# LIVE ROI MATH
# (Survival * Room * Wealth) / (1 + Saturation)
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 4. TABS ---
tab_map, tab_compare = st.tabs(["🌍 Strategic Map & Deep Dive", "📊 Portfolio Comparison"])

with tab_map:
    st.subheader("Global ROI Heatmap (Tableau Style)")
    
    # 1. The Choropleth Map
    fig_map = px.choropleth(
        df, locations="iso_alpha", color="ROI_Score",
        hover_name="country", color_continuous_scale="Viridis",
        projection="natural earth", labels={'ROI_Score': 'Rating'}
    )
    fig_map.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    
    # Use fallback dropdown since click-events require extra config
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.divider()
    
    # 2. Deep Dive Selection
    c_list = sorted(df['country'].unique())
    selected_country = st.selectbox("🔍 Select Country for Deep-Dive Intelligence:", c_list, index=c_list.index('Germany') if 'Germany' in c_list else 0)
    
    c_data = df[df['country'] == selected_country].iloc[0]
    
    # 3. Country Details
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"Profile: {selected_country}")
        st.metric("Final Strategic ROI", f"{c_data['ROI_Score']:.1f}")
        st.metric("AI Resilience Grade", "Resilient ✅" if c_data['Survival_Prob'] > 0.6 else "Vulnerable ⚠️", f"{c_data['Survival_Prob']:.1%}")
        st.metric("Market Stage", "Growth Phase 🚀" if c_data['EV_Share_Pct'] < 20 else "Mature Phase 📈", f"{c_data['EV_Share_Pct']}% Share")

    with col2:
        st.subheader("🕰️ Time Audit (2023 vs 2024)")
        m1, m2, m3 = st.columns(3)
        share_diff = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
        m1.metric("Market Share Shift", f"{c_data['EV_Share_Pct']}%", f"{share_diff:+.1f}% vs 2023")
        
        pol_diff = c_data['Policy_Score'] - c_data['Policy_Score_2023']
        m2.metric("Policy Environment", f"{c_data['Policy_Score']:.1f}", f"{pol_diff:+.1f} Support Shift")
        
        m3.metric("Purchasing Power", f"${c_data['GDP_per_capita']:,.0f}")
        
        # Real World Intelligence
        st.markdown("### 📰 Intelligence Briefing")
        context = {
            "Germany": "**⚠️ 2024 Subsidy Crash:** Germany ended EV subsidies in late 2023. AI flagged this vulnerability before the 35% sales collapse.",
            "USA": "**🛡️ Tariff Shielding:** 2024 implementation of 100% tariffs on Chinese imports. Growth is now internally driven by IRA credits.",
            "China": "**🏭 Saturation War:** Hyper-competition and price wars. High resilience, but 'Market Room' alpha is decreasing.",
            "Norway": "**✅ Mature Ecosystem:** Past the investment peak. Resilience is high, but growth alpha is low for new capital."
        }
        st.info(context.get(selected_country, "ℹ️ **Market Fundamentals:** Trajectory driven by local infrastructure pace and organic purchasing power."))

with tab_compare:
    st.subheader("⚖️ Side-by-Side Asset Comparison")
    compare_list = st.multiselect("Select Assets for Comparison:", options=c_list, default=["USA", "Germany", "Norway"])
    
    if compare_list:
        comp_df = df[df['country'].isin(compare_list)]
        fig_bar = px.bar(comp_df, x='country', y='ROI_Score', color='country', title="Risk-Adjusted Strategic Value")
        st.plotly_chart(fig_bar, use_container_width=True)
        st.dataframe(comp_df[['country', 'Survival_Prob', 'market_room', 'purchasing_power', 'ROI_Score']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
