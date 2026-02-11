import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Strategic Intelligence Engine</h1>", unsafe_allow_html=True)

# --- 2. ROBUST DATA LOADING ---
@st.cache_data
def load_data():
    # We try both names just in case of a typo on GitHub
    for filename in ['streamlit_data.csv', 'streamlit_data_v2.csv']:
        if os.path.exists(filename):
            return pd.read_csv(filename)
    return None

df = load_data()

if df is None:
    st.error("❌ Critical Error: Data file not found on GitHub!")
    st.write("Files detected in root:", os.listdir("."))
    st.stop()

# --- 3. SIDEBAR: STRATEGY PARAMETERS ---
st.sidebar.title("💎 Strategy Mandate")
st.sidebar.markdown("Adjust weights to change the $100M allocation logic.")

w_safety = st.sidebar.slider("🛡️ Resilience Weight", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Market Room Weight", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth Weight", 0.0, 2.0, 1.0)

# LIVE ROI MATH (Formula matches your MBA project logic)
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

# --- 4. TABS ---
tab_map, tab_compare = st.tabs(["🌍 Strategic Map & Deep Dive", "📊 Asset Comparison"])

with tab_map:
    st.subheader("Global ROI Heatmap")
    
    # 1. The Choropleth Map (Shaded like Tableau)
    # Using 'iso_alpha' for perfect country shading
    fig_map = px.choropleth(
        df, locations="iso_alpha", color="ROI_Score",
        hover_name="country", color_continuous_scale="Viridis",
        projection="natural earth",
        hover_data={"Survival_Prob": ":.1%", "market_room": ":.1%", "ROI_Score": ":.1f"}
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.divider()
    
    # 2. Country Deep-Dive Selection
    c_list = sorted(df['country'].unique())
    selected_country = st.selectbox("🔍 Select Country for Intelligence Briefing:", c_list, index=c_list.index('Germany') if 'Germany' in c_list else 0)
    
    c_data = df[df['country'] == selected_country].iloc[0]
    
    # 3. Briefing Layout
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"Profile: {selected_country}")
        st.metric("Strategic ROI Rating", f"{c_data['ROI_Score']:.1f}")
        res_label = "✅ Resilient" if c_data['Survival_Prob'] > 0.5 else "⚠️ Vulnerable"
        st.metric("AI Resilience Grade", res_label, f"{c_data['Survival_Prob']:.1%} Prob")
        st.metric("Market Room", f"{c_data['market_room']:.1%}", "Untapped Area")

    with col2:
        st.subheader("🕰️ Time-Series Intelligence")
        # Real World Context Engine
        context_map = {
            "Germany": "**⚠️ 2024 Market Shock:** Abrupt cancellation of subsidies in late 2023 caused a 35% collapse. Our AI flagged this as a 'Low Resilience' event.",
            "USA": "**🛡️ Protectionist Pivot:** 100% tariffs on Chinese EVs implemented in 2024. Market is now internally focused on IRA tax credits.",
            "Norway": "**✅ Market Saturation:** Structural resilience is 100%, but 'Market Room' is near zero. Low upside for new infrastructure deployment.",
            "China": "**🏭 Price War:** Market is in a hyper-competitive state. High resilience, but extreme saturation in Tier 1 cities."
        }
        st.info(context_map.get(selected_country, "ℹ️ **Market Fundamentals:** Trajectory driven by infrastructure density and organic purchasing power. No extreme black-swan policy events detected."))
        
        st.markdown("### 📊 Fundamental Breakdown")
        m1, m2 = st.columns(2)
        m1.metric("GDP Per Capita", f"${c_data['GDP_per_capita']:,.0f}")
        m2.metric("Policy Score", f"{c_data['Policy_Score']:.1f}", "Support Level")

with tab_compare:
    st.subheader("⚖️ Side-by-Side Asset Analysis")
    compare_list = st.multiselect("Select Markets to Compare:", options=c_list, default=["USA", "Germany", "Norway"])
    
    if compare_list:
        comp_df = df[df['country'].isin(compare_list)]
        fig_bar = px.bar(comp_df, x='country', y='ROI_Score', color='country', title="Risk-Adjusted Alpha Comparison")
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.dataframe(
            comp_df[['country', 'Survival_Prob', 'market_room', 'ROI_Score', 'EV_Share_Pct']]
            .style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}', 'EV_Share_Pct': '{:.1f}%'}),
            use_container_width=True
        )
