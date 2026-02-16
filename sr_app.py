import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & NO-SCROLL THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Force True Black and lock scrolling */
    .stApp { background-color: #050505; color: #E2E8F0; font-family: 'Inter', monospace; overflow-y: hidden; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Squash all padding to fit on one screen */
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; padding-left: 2rem !important; padding-right: 2rem !important; max-width: 100%; }
    
    /* Compact Text Headers */
    h1, h2, h3 { margin-top: 0rem !important; margin-bottom: 0.2rem !important; padding-top: 0rem !important; }
    p { margin-bottom: 0.5rem !important; }
    hr { margin: 0.5rem 0 !important; border-color: #222 !important; }
    
    /* Neon Metrics */
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; color: #00FF41; font-weight: 800; text-shadow: 0 0 8px rgba(0,255,65,0.4); line-height: 1.2; }
    [data-testid="stMetricLabel"] { font-size: 0.8rem !important; color: #94A3B8; font-weight: 700; text-transform: uppercase; margin-bottom: -5px;}
    
    /* Compact Button */
    .stButton>button { 
        background-color: transparent; color: #00FF41; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;
        border-radius: 4px; height: 3rem; width: 100%; border: 2px solid #00FF41; 
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); transition: all 0.3s ease; margin-top: 5px;
    }
    .stButton>button:hover { background-color: rgba(0, 255, 65, 0.1); color: #FFFFFF; }
    
    /* Sliders Compact */
    .stSlider { padding-bottom: 0px !important; margin-bottom: -20px !important; }
    
    /* Audit Dialog Box */
    .intel-box { background: linear-gradient(180deg, #111 0%, #050505 100%); border: 1px solid #222; border-top: 2px solid #00FF41; padding: 20px; border-radius: 6px; margin-top: 15px; }
    .intel-box h4 { color: #00FF41; font-weight: bold; margin-bottom: 8px; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        df.columns = [c.lower() for c in df.columns]
        if 'country' not in df.columns:
            for c in df.columns:
                if 'name' in c or 'nation' in c: df.rename(columns={c: 'country'}, inplace=True)
        return df
    return None

df = load_data()
if df is None:
    st.error("🚨 CRITICAL ERROR: 'war_room_audit_2025.csv' missing from repository.")
    st.stop()

# --- 3. GEOPOLITICAL INTELLIGENCE ---
def get_detailed_intel(country, c_data, custom_roi):
    repo = {
        "Belgium": ("⚖️ The Company Car Mandate", "Belgium's market is uniquely shielded by its corporate tax structure. In 2024, only zero-emission company vehicles qualify for 100% tax deductibility.", f"**Verdict (ROI {custom_roi:.1f}):** Defensive Safe Haven. Structural tax mandates make corporate fleet turnover mandatory."),
        "Australia": ("🛡️ NVES Policy Shield & FBT", "Australia avoided the 2024 European crash via the New Vehicle Efficiency Standard (NVES). Combined with FBT exemptions, ROI for commercial charging has surged.", f"**Verdict (ROI {custom_roi:.1f}):** #1 Core Growth Target. Structural tax advantage makes EV ownership cheaper than ICE."),
        "India": ("🐘 The EMPS Pivot", "India's 2024 manufacturing incentive (PLI) forced global giants into localized production talks. The AI identifies this as a 'Strategic Buy on the Dip'.", f"**Verdict (ROI {custom_roi:.1f}):** The 'Sleeping Giant' (Opp Gap 0.88). Primary Emerging Alpha play for 2026 breakout."),
        "France": ("🇫🇷 The 'Eco-Score' Moat", "France redefined subsidies to exclude carbon-intensive shipping, subsidizing European-made EVs while taxing Asian imports.", f"**Verdict (ROI {custom_roi:.1f}):** Protected Mature market. Highly resilient to the 2024 Chaos Regime."),
        "Germany": ("⚠️ The 'Umweltbonus' Shock", "The Dec 2023 constitutional court ruling ended all EV subsidies. Sales collapsed 35% in early 2024 as the market entered a 'Mean Reversion' phase.", f"**Verdict (ROI {custom_roi:.1f}):** HIGH VOLATILITY. Human veto recommended until H2 2025.")
    }
    
    res = repo.get(country)
    if res: return res
    return (f"🔍 Resilience Audit: {country}", f"{country} is shielded from European political volatility by organic wealth growth.", f"**Verdict (ROI {custom_roi:.1f}):** Stable target with an Opportunity Gap of {c_data.get('opportunity_gap', 0.5):.2f}.")

# --- 4. EXECUTIVE AUDIT DIALOG ---
@st.dialog("SYSTEM OVERRIDE: EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    wealth = c_data.get('purchasing_power', 5)
    custom_roi = ((prob**w_s) * (room**w_r) * (wealth**w_w)) / (1.5) * 100
    headline, context, verdict = get_detailed_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #00FF41; margin-bottom: 5px; text-transform: uppercase;'>Target: {country}</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 15)
        st.info(f"**Stage:** {'🚀 Takeoff Phase' if share < 20 else '📉 Mature'}\n\n*Current Adoption: {share:.1f}%*")
    with c2:
        st.warning(f"**AI Risk Profile:** {'✅ Highly Resilient' if c_data.get('new_prob_pct', 0) >= 78 else '⚠️ Policy Vulnerable'}\n\n*2024 Chaos Regime Test*")

    m1, m2, m3 = st.columns(3)
    curr_p = c_data.get('new_prob_pct', 0)
    m1.metric("AI Confidence", f"{curr_p:.1f}%", f"{curr_p - c_data.get('base_prob_pct', 75):+.1f}% vs Base")
    m2.metric("Opportunity Gap", f"{c_data.get('opportunity_gap', 0):.2f}")
    m3.metric("ROI Potential Index", f"{custom_roi:.1f}")

    st.markdown(f"<div class='intel-box'><h4>📰 {headline}</h4><p>{context}</p><hr style='border: 1px solid #333; margin: 10px 0;'><h4>💰 Verdict</h4><p>{verdict}</p></div>", unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown("<h2 style='color: #00FF41; text-shadow: 0 0 10px rgba(0,255,65,0.4); margin-bottom: 0;'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 0.85rem; letter-spacing: 1px;'>SYSTEM.STATUS: ONLINE // REGIME-AWARE AUDIT</p>", unsafe_allow_html=True)

# Adjusted column width to balance the screen better and remove dead space
col_map, col_panel = st.columns([6.5, 3.5], gap="large")

with col_map:
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale=[(0, "#050505"), (1, "#00FF41")])
    
    # --- CRITICAL FIX: Crop the map & force transparent background ---
    fig.update_geos(
        showland=True, landcolor="#111111", oceancolor="#050505", 
        showframe=False, coastlinecolor="#222222",
        projection_type="natural earth",
        lataxis_range=[-55, 75], # Crops out Antarctica and Extreme North to save vertical space
        bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, 
        height=480, # Shorter height guarantees no scrolling
        coloraxis_showscale=False, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # theme=None forces Plotly to respect our dark colors instead of Streamlit's light mode defaults
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun", theme=None)

with col_panel:
    selected_country = None
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        selected_country = pt.get("location") or pt.get("hovertext")
    
    manual_sel = st.selectbox("QUERY.DATABASE:", ["SELECT_TARGET..."] + sorted(df['country'].unique().tolist()))
    if not selected_country or selected_country not in df['country'].values:
        selected_country = manual_sel if manual_sel != "SELECT_TARGET..." else None

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='color: #FFF;'>TARGET: {selected_country.upper()}</h3>", unsafe_allow_html=True)
        
        m1, m2 = st.columns(2)
        m1.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        m2.metric("AI Confidence", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<span style='color: #64748b; font-size: 0.8rem;'>// CONFIGURATION</span>", unsafe_allow_html=True)
        
        ws = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        wr = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        ww = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("EXECUTE AUDIT PROTOCOL"):
            show_final_report(selected_country, ws, wr, ww)
    else:
        st.markdown("<h3 style='color: #FFF;'>PORTFOLIO LOG</h3>", unsafe_allow_html=True)
        
        m1, m2 = st.columns(2)
        m1.metric("Mandate", "$100M")
        m2.metric("Precision", "67.7%")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.info("👆 Select a country on the map to run the 78% Margin of Safety audit.")
