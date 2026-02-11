import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="GlobalCharge Engine", layout="wide", page_icon="⚡")
st.markdown("<h1 style='text-align: center; color: #18BC9C;'>⚡ GlobalCharge Intelligence Engine</h1>", unsafe_allow_html=True)

# --- 2. DATA LOADING ---
@st.cache_data
def load_data():
    try:
        return pd.read_csv('streamlit_data.csv')
    except FileNotFoundError:
        return None

df = load_data()
if df is None:
    st.error("⚠️ 'streamlit_data.csv' missing. Upload it to your repo.")
    st.stop()

# --- 3. THE MATH & PARAMETERS ---
st.sidebar.title("⚙️ Strategy Parameters")
st.sidebar.markdown("Adjust the weights to simulate different $100M Board mandates.")

w_safety = st.sidebar.slider("🛡️ Resilience Weight (Survival)", 0.0, 2.0, 1.0)
st.sidebar.caption("ℹ️ **Use:** Prioritizes markets that survive subsidy cuts. AI predicts this based on historical momentum and wealth.")

w_room = st.sidebar.slider("📈 Market Room Weight (Opportunity)", 0.0, 2.0, 1.0)
st.sidebar.caption("ℹ️ **Use:** Avoids saturated markets (like Norway). High weight finds countries early in the adoption curve.")

w_wealth = st.sidebar.slider("💰 Wealth Weight (GDP)", 0.0, 2.0, 1.0)
st.sidebar.caption("ℹ️ **Use:** Ensures the population has the actual purchasing power to buy EVs without government handouts.")

# LIVE ROI CALCULATION
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

top_targets = df.nlargest(10, 'ROI_Score')

# --- 4. REAL WORLD CONTEXT ENGINE ---
def get_real_world_context(country):
    context = {
        "Germany": "⚠️ **Policy Shock:** In Dec 2023, Germany abruptly cancelled all EV subsidies, causing a ~35% sales crash in early 2024. Our AI flagged this vulnerability.",
        "USA": "🛡️ **Protectionism & Tariffs:** Implemented 100% tariffs on Chinese EVs in 2024. Growth is heavily dependent on IRA tax credits and charging infrastructure build-out.",
        "China": "🏭 **Supply Chain Dominance:** Accounts for ~60% of global sales. Facing severe 2024 tariffs from the US/EU, causing a domestic price war.",
        "Norway": "✅ **Saturation Phase:** EV share is near 90%. Structural resilience is 100%, but 'Market Room' is zero. Bad for high-growth venture capital.",
        "Mexico": "📈 **Nearshoring:** Growth driven by commercial fleet electrification and USMCA supply chain integration rather than consumer subsidies.",
        "Brazil": "🌾 **Alternative Fuels:** Competition from established ethanol/biofuel infrastructure delays pure BEV adoption, creating unique market friction."
    }
    return context.get(country, f"ℹ️ **Standard Dynamics:** {country} adoption is governed by local wealth and infrastructure pace. No extreme policy shocks registered.")

# --- 5. MAIN INTERFACE ---
tab_map, tab_compare = st.tabs(["🌍 Global Choropleth & Deep Dive", "⚖️ Multi-Country Comparison"])

# --- TAB 1: INTERACTIVE MAP & DEEP DIVE ---
with tab_map:
    st.subheader("Global ROI Heatmap (Tableau Style)")
    st.markdown("Darker shades indicate a higher Risk-Adjusted ROI Score based on your parameters.")
    
    # 1. The Choropleth Map
    loc_col = "iso_alpha" if 'iso_alpha' in df.columns else "country"
    fig_map = px.choropleth(
        df, locations=loc_col, locationmode="ISO-3" if 'iso_alpha' in df.columns else "country names",
        color="ROI_Score", hover_name="country",
        hover_data={"Survival_Prob": ":.1%", "market_room": ":.1%", "ROI_Score": ":.1f"},
        color_continuous_scale="Viridis", projection="natural earth"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, geo=dict(showocean=True, oceancolor="LightBlue"))
    
    # Map Selection (Native Streamlit or Fallback)
    st.plotly_chart(fig_map, use_container_width=True)
    
    # 2. Deep Dive Selection
    st.divider()
    st.subheader("🔍 Country Deep-Dive Profile")
    selected_country = st.selectbox("Select a country manually (or from map visually):", sorted(df['country'].unique()), index=sorted(df['country'].unique()).index('Germany'))
    
    country_data = df[df['country'] == selected_country].iloc[0]
    
    # 3. Deep Dive Metrics
    st.info(get_real_world_context(selected_country))
    
    col1, col2, col3 = st.columns(3)
    
    # AI Classification
    is_takeoff = "🚀 High Growth Phase" if country_data['EV_Share_Pct'] < 20 else "📈 Mature Market"
    is_resilient = "✅ Safe Haven" if country_data['Survival_Prob'] > 0.60 else "⚠️ Policy Dependent"
    
    col1.metric("Classification 1: Stage", is_takeoff, f"Share: {country_data['EV_Share_Pct']}%")
    col2.metric("Classification 2: AI Safety", is_resilient, f"Survival: {country_data['Survival_Prob']:.1%}")
    col3.metric("Calculated ROI Score", f"{country_data['ROI_Score']:.1f}", "Based on Sliders")

# --- TAB 2: DASHBOARD COMPARISON ---
with tab_compare:
    st.subheader("⚖️ Target Market Comparison Dashboard")
    st.markdown("Select multiple countries to compare their fundamentals side-by-side.")
    
    compare_countries = st.multiselect(
        "Select Countries to Compare:", 
        options=sorted(df['country'].unique()), 
        default=["USA", "Germany", "China", "Norway"]
    )
    
    if compare_countries:
        compare_df = df[df['country'].isin(compare_countries)]
        
        # Bar Chart Comparison
        fig_bar = px.bar(
            compare_df, x="country", y=["Survival_Prob", "market_room"], 
            barmode="group", title="AI Survival vs. Remaining Market Room",
            labels={"value": "Percentage (0 to 1)", "variable": "Metric"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Raw Data Table
        display_cols = ['country', 'Survival_Prob', 'ROI_Score', 'EV_Share_Pct', 'GDP_per_capita']
        st.dataframe(
            compare_df[display_cols].sort_values('ROI_Score', ascending=False)
            .style.format({'Survival_Prob': '{:.1%}', 'ROI_Score': '{:.1f}', 'GDP_per_capita': '${:,.0f}', 'EV_Share_Pct': '{:.1f}%'}),
            use_container_width=True
        )
    else:
        st.warning("Please select at least one country to compare.")
