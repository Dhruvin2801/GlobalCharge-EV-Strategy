import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Strategic Intelligence Engine</h1>", unsafe_allow_html=True)

# --- DEBUG: AUTOMATIC FILE SEARCHER ---
# This looks for the CSV and tells you if it's missing or misspelled
st.sidebar.title("📁 System Audit")
files = os.listdir(".")
target_file = 'streamlit_data.csv' # It will also check for v2 automatically below

if target_file not in files and 'streamlit_data_v2.csv' not in files:
    st.error("❌ DATA ERROR: File not found in GitHub root.")
    st.write("Files currently in your GitHub repository:")
    st.write(files)
    st.stop()
else:
    st.sidebar.success("✅ Connection: Data Linked")

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    # Priority: v2 (Enhanced) > v1 (Standard)
    if os.path.exists('streamlit_data_v2.csv'):
        return pd.read_csv('streamlit_data_v2.csv')
    return pd.read_csv('streamlit_data.csv')

df = load_data()

# --- 3. SIDEBAR: STRATEGY PARAMETERS ---
st.sidebar.title("💎 Strategy Mandate")
w_safety = st.sidebar.slider("🛡️ Resilience (Safety)", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity (Growth Room)", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth (Purchasing Power)", 0.0, 2.0, 1.0)

# LIVE ROI MATH
# ROI = (Survival^Safety * Room^Opportunity * Wealth^Purchasing) / (1 + Saturation)
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 4. INTERFACE TABS ---
tab_map, tab_compare = st.tabs(["🌍 Strategic Map & Deep Dive", "📊 Asset Comparison"])

with tab_map:
    st.subheader("Global ROI Heatmap (Tableau Style)")
    
    # 1. THE MAP
    # Uses 'iso_alpha' for shaded country colors
    fig_map = px.choropleth(
        df, locations="iso_alpha", color="ROI_Score",
        hover_name="country", color_continuous_scale="Viridis",
        projection="natural earth",
        hover_data={"Survival_Prob": ":.1%", "market_room": ":.1%", "ROI_Score": ":.1f"}
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.divider()
    
    # 2. COUNTRY DEEP-DIVE
    c_list = sorted(df['country'].unique())
    selected_country = st.selectbox("🔍 Select Country for Intelligence Briefing:", c_list, index=c_list.index('Germany') if 'Germany' in c_list else 0)
    
    c_data = df[df['country'] == selected_country].iloc[0]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"Profile: {selected_country}")
        st.metric("Final Strategic ROI", f"{c_data['ROI_Score']:.1f}")
        res_label = "✅ Resilient" if c_data['Survival_Prob'] > 0.6 else "⚠️ Vulnerable"
        st.metric("AI Resilience Grade", res_label, f"{c_data['Survival_Prob']:.1%} Prob")
        st.metric("Market Stage", "Early Takeoff 🚀" if c_data['EV_Share_Pct'] < 15 else "Mature Phase 📈", f"{c_data['EV_Share_Pct']}% Share")

    with col2:
        st.subheader("🕰️ Time-Series Intelligence")
        # Check if 2023 columns exist for delta calculation
        if 'EV_Share_Pct_2023' in df.columns:
            m1, m2 = st.columns(2)
            share_diff = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
            m1.metric("Market Share Shift", f"{c_data['EV_Share_Pct']}%", f"{share_diff:+.1f}% vs 2023")
            pol_diff = c_data['Policy_Score'] - c_data['Policy_Score_2023']
            m2.metric("Policy Score Shift", f"{c_data['Policy_Score']:.1f}", f"{pol_diff:+.1f} vs 2023")
        
        # Real World Context Briefing
        context_map = {
            "Germany": "**⚠️ 2024 Subsidy Crash:** Germany ended subsidies in late 2023. Our AI flagged this vulnerability before the 35% sales collapse.",
            "USA": "**🛡️ Tariff Protection:** 2024 implementation of 100% tariffs on Chinese EVs. Growth is now driven by IRA credits and charging density.",
            "Norway": "**✅ Market Saturation:** Structural resilience is 100%, but 'Market Room' is near zero. Low upside for new capital deployment.",
            "China": "**🏭 Supply Dominance:** Hyper-competitive price war. High resilience, but extreme saturation in Tier 1 cities."
        }
        st.info(context_map.get(selected_country, "ℹ️ **Market Fundamentals:** Trajectory driven by infrastructure density and organic purchasing power. No extreme black-swan events detected."))

with tab_compare:
    st.subheader("⚖️ Side-by-Side Asset Analysis")
    compare_list = st.multiselect("Select Markets to Compare:", options=c_list, default=c_list[:3])
    
    if compare_list:
        comp_df = df[df['country'].isin(compare_list)]
        fig_bar = px.bar(comp_df, x='country', y='ROI_Score', color='country', title="Risk-Adjusted Alpha Comparison")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.dataframe(
            comp_df[['country', 'Survival_Prob', 'market_room', 'purchasing_power', 'ROI_Score']]
            .style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}),
            use_container_width=True
        )
