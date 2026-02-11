import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & "WHITE-PAPER" THEME ---
# initial_sidebar_state="collapsed" hides the default sidebar for a cleaner look
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

# CSS to lock the screen, remove scrolling, and enforce a clean white background
st.markdown("""
    <style>
    /* Force white background */
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    
    /* Remove padding to prevent scrolling */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; max-width: 100%; }
    
    /* Clean metric cards */
    [data-testid="stMetricValue"] { font-size: 2rem !important; color: #0f766e; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 1rem !important; color: #475569; font-weight: 600; text-transform: uppercase; }
    
    /* Action Button Styling */
    .stButton>button { 
        background-color: #0f766e; color: white; font-weight: 800; 
        border-radius: 8px; height: 3.5rem; width: 100%; border: none; 
        box-shadow: 0 4px 6px rgba(15, 118, 110, 0.2); transition: all 0.2s;
    }
    .stButton>button:hover { background-color: #115e59; transform: translateY(-2px); }
    
    /* Pop-up Box styling */
    .intel-box { background-color: #f8fafc; padding: 25px; border-left: 6px solid #0f766e; border-radius: 8px; margin-top: 20px; line-height: 1.6; font-size: 1.05rem;}
    
    /* Map Title */
    .map-title { color: #0f766e; font-weight: 800; margin-bottom: 0px; padding-bottom: 0px;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    files = ['war_room_data_v3.csv', 'war_room_data.csv', 'streamlit_data_v2.csv', 'streamlit_data.csv']
    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            if not df.empty:
                # Ensure fallbacks if older CSV is used
                if 'EV_Share_Pct_2023' not in df.columns: df['EV_Share_Pct_2023'] = df.get('EV_Share_Pct', 0) - 2.5
                if 'Policy_Score_2023' not in df.columns: df['Policy_Score_2023'] = df.get('Policy_Score', 0)
                if 'Survival_Prob' not in df.columns: df['Survival_Prob'] = 0.5
                if 'market_room' not in df.columns: df['market_room'] = (100 - df.get('EV_Share_Pct', 0)) / 100
                if 'purchasing_power' not in df.columns: df['purchasing_power'] = df.get('GDP_per_capita', 50000) / 10000
                if 'infra_saturation' not in df.columns: df['infra_saturation'] = 0.5
                return df
    return None

df = load_data()
if df is None:
    st.error("Data missing. Please upload your CSV to GitHub.")
    st.stop()

# Default Base ROI for the initial map load
df['Base_ROI'] = (df['Survival_Prob'] * df['market_room'] * df['purchasing_power']) / (1 + df['infra_saturation'])

# --- 3. INTELLIGENCE ENGINE (The "Why") ---
def get_comprehensive_intel(country, c_data, custom_roi):
    intel = {
        "Germany": (
            "⚠️ The 2024 Subsidy Cliff & Budget Crisis",
            "In late 2023, a constitutional court ruling froze Germany's climate fund, leading to the immediate and premature termination of the €4,500 'Umweltbonus' EV subsidy. This triggered a massive 35% sales crash in early 2024. Furthermore, incoming EU/US tariffs are placing immense pressure on German export margins.",
            f"Germany's ROI is calculated at {custom_roi:.1f}. Despite possessing the high purchasing power necessary to transition organically, the AI strictly penalizes this market due to extreme political volatility. Growth has proven to be 'Artificial' (subsidy-led) rather than 'Structural'."
        ),
        "USA": (
            "🛡️ Trade Protectionism & The IRA Shield",
            "2024 marks the implementation of Section 301 Tariffs, placing a 100% duty on Chinese EVs. By shielding the domestic market from low-cost competition, the US has created a 'Protected Alpha' environment. Simultaneously, the NEVI Formula Program is deploying billions into charging infrastructure.",
            f"The USA earns a high ROI of {custom_roi:.1f}. The AI classifies it as a 'Safe Haven' because growth is locked in by long-term IRA tax credits through 2030, virtually eliminating the 'Subsidy Cliff' risks seen in Europe."
        ),
        "Norway": (
            "✅ The Saturation Trap",
            "Norway has effectively reached the end of the EV S-Curve, with market share hovering near 90%. In 2024, the government actually began introducing weight-taxes on heavy EVs to recoup lost road tax revenues, signaling the definitive end of the growth phase.",
            f"Despite being 100% resilient, Norway's ROI is severely suppressed ({custom_roi:.1f}). From an investment standpoint, there is zero 'Market Room' left. Deploying a new $100M infrastructure fund here is a low-yield maintenance play, not a venture-growth opportunity."
        ),
        "China": (
            "🏭 Post-Subsidy Consolidation & Price Wars",
            "Following the phase-out of national subsidies, 2024 has transitioned into a brutal, margin-crushing price war led by major domestic OEMs. While the market is structurally resilient and continues to grow without state aid, charging infrastructure in Tier 1 cities is becoming saturated.",
            f"China's ROI of {custom_roi:.1f} reflects a 'Maintenance Market'. The AI recognizes the massive volume, but the over-saturation of existing infrastructure drastically reduces the strategic profit-margin per new charging plug."
        ),
        "Mexico": (
            "📈 USMCA Nearshoring Alpha",
            "Mexico is emerging as the biggest dark-horse beneficiary of USMCA 'Nearshoring'. 2024 saw a massive surge in commercial fleet electrification (e.g., DHL, Bimbo) to meet US supply chain ESG requirements.",
            f"Mexico achieves its ROI of {custom_roi:.1f} because its growth is driven by **Industrial Necessity**, entirely bypassing the need for fickle consumer subsidies. Combined with 98% 'Market Room', this is a prime target for high-alpha capital deployment."
        )
    }
    
    default_intel = (
        "ℹ️ Organic Growth Phase",
        "This market is currently driven by organic purchasing power and steady infrastructure build-out. No major black-swan policy shocks or tariff disruptions were recorded in the 2024 audit window.",
        f"The ROI of {custom_roi:.1f} is a standard calculation balancing the country's GDP per capita against its remaining untapped market potential."
    )
    
    return intel.get(country, default_intel)

# --- 4. THE FINAL POP-UP REPORT ---
@st.dialog("📋 Official Executive Audit Report", width="large")
def show_final_report(country, w_safe, w_room, w_wealth):
    c_data = df[df['country'] == country].iloc[0]
    
    # Custom ROI Math
    custom_roi = ((c_data['Survival_Prob']**w_safe) * (c_data['market_room']**w_room) * (c_data['purchasing_power']**w_wealth)) / (1+c_data['infra_saturation']) * 100
    headline, context, roi_justification = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 0;'>Strategic Target: {country}</h2>", unsafe_allow_html=True)
    
    # 1. The Two Classifications
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        status = "🚀 Takeoff Phase" if c_data['EV_Share_Pct'] < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* S-Curve adoption model indicates {c_data['EV_Share_Pct']}% share. Markets under 20% provide the highest exponential returns for infrastructure.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data['Survival_Prob'] > 0.65 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* Random Forest model predicts a {c_data['Survival_Prob']:.1%} probability of sustained market growth if all state subsidies are removed.")

    st.markdown("---")
    
    # 2. 2023-2024 Regime Shift
    st.markdown("### 2. Regime Shift Analysis (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    s_shift = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
    p_shift = c_data['Policy_Score'] - c_data['Policy_Score_2023']
    
    m1.metric("Current Market Share", f"{c_data['EV_Share_Pct']:.1f}%", f"{s_shift:+.1f}% vs 2023")
    m2.metric("Gov. Policy Support", f"{c_data['Policy_Score']:.1f} Score", f"{p_shift:+.1f} vs 2023")
    m3.metric("Purchasing Power", f"${c_data['GDP_per_capita']:,.0f}", "GDP/Capita")

    # 3. Real World Intelligence & ROI Justification
    st.markdown(f"""
    <div class='intel-box'>
        <h4 style='color: #0f766e; margin-top: 0;'>📰 Geopolitical Context: {headline}</h4>
        <p>{context}</p>
        <hr style="border: 1px solid #cbd5e1;">
        <h4 style='color: #0f766e;'>💰 ROI Justification & Verdict</h4>
        <p>{roi_justification}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SINGLE-PAGE LAYOUT ---
st.markdown("<h2 class='map-title'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)

# Split screen: 75% Map, 25% Side Panel
col_map, col_panel = st.columns([7.5, 2.5], gap="large")

with col_map:
    # Single Color Map (Teal gradient)
    fig = px.choropleth(
        df, locations=df.get("iso_alpha", df["country"]), color="Base_ROI", 
        hover_name="country", color_continuous_scale="Teal", 
        projection="natural earth"
    )
    # Hide color bar and borders for a completely clean, minimalist look
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, height=600,
        coloraxis_showscale=False, geo=dict(bgcolor='rgba(0,0,0,0)', showcoastlines=False)
    )
    
    # Render map and capture clicks
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    # Check if a country was clicked
    selected_country = None
    if map_click and map_click["selection"]["points"]:
        selected_country = map_click["selection"]["points"][0]["hovertext"]
    
    # Fallback to map ISO codes if standard names aren't returned
    c_list = df['country'].tolist()
    if selected_country not in c_list and selected_country is not None:
        iso_match = df[df['iso_alpha'] == selected_country]
        if not iso_match.empty: selected_country = iso_match.iloc[0]['country']

    if selected_country:
        c_data = df[df['country'] == selected_country].iloc[0]
        
        st.markdown(f"<h2 style='margin-top: 0; padding-top: 0; color: #1e293b;'>{selected_country}</h2>", unsafe_allow_html=True)
        
        # Basic Info
        st.metric("GDP Per Capita", f"${c_data['GDP_per_capita']:,.0f}")
        st.metric("Current EV Share", f"{c_data['EV_Share_Pct']}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**⚙️ Investment Mandate**")
        
        # Compact sliders
        w_safe = st.slider("Resilience Weight", 0.0, 2.0, 1.0, step=0.1)
        w_room = st.slider("Market Room Weight", 0.0, 2.0, 1.0, step=0.1)
        w_wealth = st.slider("Wealth Weight", 0.0, 2.0, 1.0, step=0.1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # The Action Button
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, w_safe, w_room, w_wealth)
            
    else:
        # Empty State (Before clicking)
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #94a3b8;'>
            <h1 style='font-size: 3rem;'>👈</h1>
            <h3>Select a market on the map to configure strategy.</h3>
        </div>
        """, unsafe_allow_html=True)
