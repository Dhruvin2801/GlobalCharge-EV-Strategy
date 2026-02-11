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

# --- 3. SIDEBAR: NAVIGATION & PARAMETERS ---
st.sidebar.title("🌍 Market Controls")
selected_country = st.sidebar.selectbox("🔍 Select Country to Analyze", sorted(df['country'].unique()))

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ ROI Parameters")

w_safety = st.sidebar.slider("🛡️ Resilience Weight", 0.0, 2.0, 1.0)
with st.sidebar.expander("What does Resilience mean?"):
    st.write("Prioritizes markets with a high AI 'Survival Probability'. A high weight here means we only invest in countries that will survive sudden policy shocks (like subsidy cuts).")

w_room = st.sidebar.slider("📈 Market Room Weight", 0.0, 2.0, 1.0)
with st.sidebar.expander("What does Market Room mean?"):
    st.write("Prioritizes markets that are mostly untapped. A country with 80% market room still has massive growth potential before hitting saturation.")

w_wealth = st.sidebar.slider("💰 Wealth Weight (GDP)", 0.0, 2.0, 1.0)
with st.sidebar.expander("What does Wealth mean?"):
    st.write("Prioritizes purchasing power. It measures whether the local population can actually afford EVs without relying on government handouts.")

# --- 4. LIVE ROI CALCULATION ---
# Formula: (Survival * Room * Wealth) / (1 + Saturation)
df['ROI_Score'] = (
    (df['Survival_Prob'] ** w_safety) * (df['market_room'] ** w_room) * (df['purchasing_power'] ** w_wealth)
) / (1 + df['infra_saturation']) * 100

top_targets = df.nlargest(10, 'ROI_Score')
country_data = df[df['country'] == selected_country].iloc[0]

# --- 5. REAL WORLD CONTEXT ENGINE ---
def get_real_world_context(country):
    context = {
        "Germany": "⚠️ **Policy Shock & Tariff Exposure:** In Dec 2023, Germany abruptly cancelled all EV subsidies, causing a ~35% sales crash in early 2024. Furthermore, the 25% US auto import tariffs (implemented April 2025) place severe strain on its export-heavy automotive core. Our model flags this as a highly volatile transition environment.",
        "United States": "🛡️ **Protectionist Environment:** In May 2024, the US implemented a 100% tariff on Chinese EVs under Section 301, shielding domestic automakers. While this protects local pricing, EV adoption remains heavily dependent on regional charging density and federal tax credits.",
        "China": "🏭 **Supply Chain Dominance:** China accounts for the vast majority of global EV sales. Facing severe 2024/2025 tariffs from the US (100%) and EU, China's domestic market is in a hyper-competitive price war, pushing massive export volumes to secondary markets.",
        "Norway": "✅ **Market Saturation:** Norway is past the 'Takeoff' phase and into deep market saturation. Subsidies are naturally phasing out because EVs have reached price parity. It is structurally resilient but offers very low 'Market Room' for explosive new growth.",
        "Mexico": "📈 **Nearshoring Beneficiary:** Mexico's EV market is strongly influenced by manufacturing nearshoring to comply with USMCA trade rules. Domestic adoption is increasingly driven by operational cost savings for commercial fleets rather than consumer subsidies."
    }
    return context.get(country, "ℹ️ **Standard Market Dynamics:** This market's trajectory is primarily driven by domestic purchasing power and gradual infrastructure build-out. No critical black-swan policy events recorded in the current analysis window.")

# --- 6. MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["🌍 Global Map", "🔍 Country Deep-Dive", "📊 Comparison Dashboard"])

# TAB 1: THE MAP
with tab1:
    st.subheader("Global ROI Heatmap")
    st.markdown("Use the Sidebar sliders to adjust the strategy. The map updates in real-time.")
    loc_col = "iso_alpha" if 'iso_alpha' in df.columns else "country"
    fig_map = px.scatter_geo(
        df, locations=loc_col, locationmode="ISO-3" if 'iso_alpha' in df.columns else "country names",
        color="ROI_Score", size="ROI_Score", hover_name="country",
        projection="natural earth", color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_map, use_container_width=True)

# TAB 2: COUNTRY DEEP DIVE
with tab2:
    st.subheader(f"Target Analysis: {selected_country}")
    
    colA, colB, colC = st.columns(3)
    # Classification 1: Takeoff / Growth Stage
    takeoff_status = "🚀 High Potential" if (country_data['EV_Share_Pct'] > 2 and country_data['EV_Share_Pct'] < 20) else "📉 Saturated / Early"
    colA.metric("Classification 1: Market Stage", takeoff_status, f"{country_data['EV_Share_Pct']}% Current Share")
    
    # Classification 2: Resilience
    resilience_status = "✅ Resilient" if country_data['Survival_Prob'] > 0.65 else "⚠️ Vulnerable"
    colB.metric("Classification 2: AI Safety", resilience_status, f"{country_data['Survival_Prob']:.1%} Survival Prob")
    
    # Final ROI
    colC.metric("Strategic ROI Score", f"{country_data['ROI_Score']:.1f}")

    st.divider()
    st.markdown("### 📰 Real-World Market Intelligence")
    st.info(get_real_world_context(selected_country))

    st.markdown("### 📊 Local Fundamentals")
    m1, m2, m3 = st.columns(3)
    m1.metric("GDP Per Capita", f"${country_data['GDP_per_capita']:,.0f}")
    m2.metric("Market Room", f"{country_data['market_room']:.1%}")
    m3.metric("Infra Saturation Score", f"{country_data['infra_saturation']:.2f}")

# TAB 3: DASHBOARD
with tab3:
    st.subheader("Top 10 Targets & Portfolio Allocation")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        total_score = top_targets['ROI_Score'].sum()
        top_targets['Investment ($M)'] = (top_targets['ROI_Score'] / total_score) * 100
        fig_pie = px.pie(top_targets, values='Investment ($M)', names='country', hole=0.4, color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        display_cols = ['country', 'Survival_Prob', 'ROI_Score', 'Investment ($M)']
        st.dataframe(
            top_targets[display_cols].sort_values('ROI_Score', ascending=False)
            .style.format({'Survival_Prob': '{:.1%}', 'ROI_Score': '{:.1f}', 'Investment ($M)': '${:.1f}M'}),
            use_container_width=True, height=350
        )
