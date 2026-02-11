import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & CLEAN "WHITE-PAPER" THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

# CSS to lock the screen, remove scrolling, and enforce a clean white background
st.markdown("""
    <style>
    /* Force white background and hide header/footer */
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Remove padding to prevent scrolling */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 2rem; padding-right: 2rem; max-width: 100%; }
    
    /* Clean metric cards */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #0f766e; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #64748b; font-weight: 600; text-transform: uppercase; }
    
    /* Action Button */
    .stButton>button { background-color: #0f766e; color: white; font-weight: bold; border-radius: 6px; height: 3rem; width: 100%; border: none; }
    .stButton>button:hover { background-color: #115e59; color: white; }
    
    /* Pop-up Box styling */
    .intel-box { background-color: #f8fafc; padding: 20px; border-left: 5px solid #0f766e; border-radius: 8px; margin-top: 15px; }
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

# --- 3. INTELLIGENCE ENGINE ---
def get_intel(country):
    intel = {
        "Germany": ("The Subsidy Cliff", "In late 2023, the €4,500 'Umweltbonus' was abruptly terminated due to a court budget ruling. This triggered a 35% sales crash in early 2024. Our AI ROI rating is suppressed here due to extreme political volatility. Growth is now forced to be organic rather than state-sponsored."),
        "USA": ("Trade Protectionism", "The 2024 implementation of 100% tariffs on Chinese EVs shielded domestic margins. This 'Protected Alpha' environment, combined with IRA tax credits, makes the US a highly resilient target for infrastructure deployment."),
        "Norway": ("The Saturation Trap", "Norway is the most resilient market globally, but it has 'completed the mission'. With EV share near 90%, there is no 'Market Room' left. High survival, but no alpha for new $100M infrastructure investments."),
        "China": ("Post-Subsidy Price War", "China removed national subsidies in 2023. 2024 has become a brutal price war. While the market continues to grow without aid (100% resilient), charging station over-saturation limits our ROI per new plug."),
        "Mexico": ("USMCA Nearshoring", "A massive dark horse. Growth is driven by industrial fleet electrification (DHL, Bimbo) to meet USMCA supply chain mandates, entirely bypassing the need for consumer subsidies. High growth, high safety.")
    }
    return intel.get(country, ("Organic Growth Phase", "This market is currently driven by organic purchasing power and infrastructure build-out. No major black-swan policy shocks were recorded in the 2024 audit window."))

# --- 4. THE FINAL POP-UP REPORT ---
@st.dialog("📋 Official Boardroom Audit Report", width="large")
def show_final_report(country, w_safe, w_room, w_wealth):
    c_data = df[df['country'] == country].iloc[0]
    
    # Calculate the Custom ROI based on the sliders the user just adjusted
    custom_roi = ((c_data['Survival_Prob']**w_safe) * (c_data['market_room']**w_room) * (c_data['purchasing_power']**w_wealth)) / (1+c_data['infra_saturation']) * 100
    
    st.markdown(f"<h2 style='color: #0f766e;'>Target: {country}</h2>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Calculated Custom ROI", f"{custom_roi:.1f}", "Based on your parameters")
    status = "Takeoff (High Growth)" if c_data['EV_Share_Pct'] < 20 else "Mature (Saturated)"
    c2.metric("Market Classification", status)
    resilience = "Resilient" if c_data['Survival_Prob'] > 0.65 else "Vulnerable"
    c3.metric("AI Risk Classification", resilience, f"{c_data['Survival_Prob']:.1%} Survival Prob")

    st.markdown("---")
    st.markdown("#### 🕰️ Regime Shift Analysis (2023 ➔ 2024)")
    
    m1, m2 = st.columns(2)
    s_shift = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
    p_shift = c_data['Policy_Score'] - c_data['Policy_Score_2023']
    m1.metric("Market Share Shift", f"{c_data['EV_Share_Pct']:.1f}%", f"{s_shift:+.1f}% vs 2023")
    m2.metric("Government Support Shift", f"{c_data['Policy_Score']:.1f} Score", f"{p_shift:+.1f} vs 2023")

    headline, context = get_intel(country)
    st.markdown(f"""
    <div class='intel-box'>
        <h4 style='color: #0f766e; margin-top: 0;'>📰 Geopolitical Context: {headline}</h4>
        <p style='margin-bottom: 0;'>{context}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SINGLE-PAGE LAYOUT ---
st.markdown("<h2 style='color: #0f766e; margin-bottom: 0;'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)

# Split screen: 75% Map, 25% Side Panel
col_map, col_panel = st.columns([7.5, 2.5], gap="large")

with col_map:
    # Single Color Map (Teal gradient)
    fig = px.choropleth(
        df, locations=df.get("iso_alpha", df["country"]), color="Base_ROI", 
        hover_name="country", color_continuous_scale="Teal", 
        projection="natural earth"
    )
    # Hide color bar, background, and borders for maximum clean look
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, height=550,
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
        # Try to map ISO back to country name
        iso_match = df[df['iso_alpha'] == selected_country]
        if not iso_match.empty: selected_country = iso_match.iloc[0]['country']

    if selected_country:
        c_data = df[df['country'] == selected_country].iloc[0]
        
        st.markdown(f"<h3 style='margin-top: 0; padding-top: 0;'>{selected_country}</h3>", unsafe_allow_html=True)
        
        # Basic Info
        st.metric("GDP Per Capita", f"${c_data['GDP_per_capita']:,.0f}")
        st.metric("Current EV Share", f"{c_data['EV_Share_Pct']}%")
        
        st.markdown("---")
        st.markdown("**⚙️ Investment Mandate**")
        
        # Compact sliders
        w_safe = st.slider("Resilience Weight", 0.0, 2.0, 1.0, step=0.1)
        w_room = st.slider("Market Room Weight", 0.0, 2.0, 1.0, step=0.1)
        w_wealth = st.slider("Wealth Weight", 0.0, 2.0, 1.0, step=0.1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # The Action Button
        if st.button("Generate Board Report"):
            show_final_report(selected_country, w_safe, w_room, w_wealth)
            
    else:
        # Empty State (Before clicking)
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style='text-align: center; color: #94a3b8;'>
            <h1 style='font-size: 3rem;'>👈</h1>
            <h3>Select a market on the map to begin strategic analysis.</h3>
        </div>
        """, unsafe_allow_html=True)
