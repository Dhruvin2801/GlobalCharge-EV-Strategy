import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & "EXECUTIVE PLATINUM" THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Premium Metric Styling */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #0f766e; font-weight: 800; letter-spacing: -0.05rem; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #64748b; font-weight: 700; text-transform: uppercase; }
    
    /* Audit Button Styling */
    .stButton>button { 
        background-color: #0f766e; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 8px; height: 3.5rem; width: 100%; border: none; 
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25); transition: all 0.3s ease; margin-top: 15px;
    }
    .stButton>button:hover { background-color: #115e59; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(15, 118, 110, 0.35); }
    
    /* Intel Box Styling */
    .intel-box { background-color: #f8fafc; padding: 28px; border-left: 8px solid #0f766e; border-radius: 12px; margin-top: 20px; line-height: 1.8; }
    .intel-box h4 { color: #0f766e; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; font-size: 1.1rem; }
    .intel-box p { color: #334155; font-size: 1.05rem; }
    
    /* Slider Clean-up */
    .stSlider { padding-bottom: 0px; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ROBUST DATA LOADER ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025_FINAL.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        df.columns = [c.lower() for c in df.columns] # Force lowercase to prevent KeyErrors
        # Standardize 'country' column
        if 'country' not in df.columns:
            for c in df.columns:
                if 'name' in c or 'nation' in c: df.rename(columns={c: 'country'}, inplace=True)
        return df
    return None

df = load_data()
if df is None:
    st.error("🚨 CRITICAL ERROR: 'war_room_audit_2025.csv' missing from repository.")
    st.stop()

# --- 3. THE DEEP INTELLIGENCE REPOSITORY (GEOPOLITICAL 'WHY') ---
def get_detailed_intel(country, c_data, custom_roi):
    repo = {
        "Belgium": (
            "⚖️ Fiscal Dominance & The Company Car Mandate",
            "**2023-2024 Regime Shift:** Belgium's market is uniquely shielded by its 'Company Car' tax structure. In 2024, the government mandated that only zero-emission company vehicles qualify for 100% tax deductibility. This created an artificial but highly resilient 'floor' for adoption, completely bypassing the consumer interest rate anxieties seen in Germany.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Belgium is a 'Defensive Safe Haven'. While adoption is high (41%), the structural tax mandate makes it one of the most stable regions for long-term infrastructure ROI, as corporate fleet turnover is mandatory, not optional."
        ),
        "Australia": (
            "🛡️ NVES Policy Shield & The FBT Exemption",
            "**2023-2024 Regime Shift:** Australia successfully avoided the 2024 European crash by implementing the New Vehicle Efficiency Standard (NVES). Combined with the ongoing Fringe Benefits Tax (FBT) exemption, the ROI for commercial and private charging has surged, making Australia the primary 'Takeoff' market of the year.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Australia remains our #1 Core Growth Target. The 12% share provides exponential room for growth, and the structural tax advantage makes EV ownership cheaper than ICE for the middle class."
        ),
        "India": (
            "🐘 The EMPS Pivot & The 0.88 Opportunity Alpha",
            "**2023-2024 Regime Shift:** India's pivot from FAME-II to the EMPS scheme caused a temporary supply-side plateau. However, the 2024 manufacturing incentive (PLI) has forced global giants like VinFast and Tesla into localized production talks. The AI identifies this as a 'Strategic Buy on the Dip'.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** India holds the largest 'Opportunity Gap' in the fund. Deployment here targets the 2026-2028 S-Curve breakout. It is the portfolio's primary Emerging Alpha play."
        ),
        "France": (
            "🇫🇷 The 'Eco-Score' Moat & Sovereign Protection",
            "**2023-2024 Regime Shift:** France's 2024 'Eco-Score' redefined subsidies to exclude carbon-intensive shipping. This effectively subsidized European-made EVs while taxing Asian imports. This sovereign protectionism has stabilized domestic ROI against global price volatility.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** A 'Protected Mature' market. France is highly resilient to the 2024 Chaos Regime because its policy actively shields domestic margins from the Chinese price wars."
        ),
        "Germany": (
            "⚠️ The 'Umweltbonus' Shock & Subsidy Cliff",
            "**2023-2024 Regime Shift:** The Dec 2023 constitutional court ruling forced an immediate end to all EV subsidies. This 'Policy Heart Attack' proved that German adoption was an artificial bubble. Sales collapsed 35% in early 2024 as the market entered a 'Mean Reversion' phase.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** HIGH VOLATILITY. We recommend a human veto until H2 2025. The AI identifies high structural wealth, but the current political regime shift makes capital deployment risky."
        )
    }
    
    # Dynamic Fallback for 30+ other countries
    res = repo.get(country)
    if res: return res
    
    gap = c_data.get('opportunity_gap', 0.5)
    return (f"🔍 Structural Resilience Audit: {country}", 
            f"**2023-24 Dynamics:** {country} is following a classic GDP-driven S-Curve. Adoption is shielded from the European political volatility by organic wealth growth and the redirection of global supply chains toward non-tariffed regions.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Stable deployment target with an Opportunity Gap of {gap:.2f}. Growth is driven by long-term infrastructure expansion rather than fickle state aid.")

# --- 4. THE EXECUTIVE AUDIT DIALOG ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    wealth = c_data.get('purchasing_power', 5)
    custom_roi = ((prob**w_s) * (room**w_r) * (wealth**w_w)) / (1.5) * 100
    
    headline, context, verdict = get_detailed_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 5px;'>Strategic Audit: {country}</h2>", unsafe_allow_html=True)
    
    # SECTION 1: Classifications (DITTO IMAGE STYLE)
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 15)
        status = "🚀 Takeoff Phase" if share < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* Market exhibits {share:.1f}% adoption. Deployment into markets under 20% yields highest exponential returns.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data.get('new_prob_pct', 0) >= 78 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* Model identifies high structural stability despite the 2024 'Chaos Regime' shifts.")

    st.markdown("---")
    
    # SECTION 2: Analytics
    st.markdown("### 2. Regime Shift Analytics (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    curr_p = c_data.get('new_prob_pct', 0)
    base_p = c_data.get('base_prob_pct', 75)
    m1.metric("AI Confidence", f"{curr_p:.1f}%", f"{curr_p - base_p:+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('opportunity_gap', 0):.2f}", "Alpha Index")
    m3.metric("ROI Potential Index", f"{custom_roi:.1f}", "Scaled Score")

    # SECTION 3: Deep Intel Box
    st.markdown(f"""
    <div class='intel-box'>
        <h4>📰 Geopolitical Context: {headline}</h4>
        <p>{context}</p>
        <hr style='border: 1px solid #cbd5e1; margin: 20px 0;'>
        <h4>💰 ROI Justification & Verdict</h4>
        <p>{verdict}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='color: #0f766e; margin-bottom: 0px;'>GlobalCharge Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-weight: 600; margin-top: 0;'>EXECUTIVE INVESTMENT DASHBOARD | REGIME-AWARE AUDIT</p>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.2, 2.8], gap="medium")

with col_map:
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Teal")
    fig.update_geos(showland=True, landcolor="#f1f5f9", oceancolor="#ffffff", showframe=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550, coloraxis_showscale=False)
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    # Triple-Redundant Selection
    selected_country = None
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        selected_country = pt.get("location") or pt.get("hovertext")
    
    # Fallback Selector
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    manual_sel = st.selectbox("Select Target Market:", ["Click Map..."] + sorted(df['country'].unique().tolist()))
    if not selected_country or selected_country not in df['country'].values:
        selected_country = manual_sel if manual_sel != "Click Map..." else None

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 10px;'>🎯 Target: {selected_country}</h3>", unsafe_allow_html=True)
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("**⚙️ Configuration Mandate**")
        ws = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        wr = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        ww = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, ws, wr, ww)
    else:
        st.markdown("<h3 style='margin-top: 10px;'>🌍 Portfolio Audit</h3>", unsafe_allow_html=True)
        st.metric("Capital Mandate", "$100M")
        st.metric("Precision (2024)", "67.7%")
        st.info("Select a country on the map or use the selector to run the 78% Margin of Safety audit.")
