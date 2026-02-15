import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & "WHITE-PAPER" THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

# Professional White-Paper Styling (Restored Ditto)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Clean metric cards */
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; color: #0f766e; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #64748b; font-weight: 600; text-transform: uppercase; }
    
    /* Action Button Styling */
    .stButton>button { 
        background-color: #0f766e; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 6px; height: 3.2rem; width: 100%; border: none; 
        box-shadow: 0 4px 6px rgba(15, 118, 110, 0.2); transition: all 0.2s; margin-top: 15px;
    }
    .stButton>button:hover { background-color: #115e59; transform: translateY(-2px); }
    
    /* Pop-up Box styling */
    .intel-box { background-color: #f8fafc; padding: 25px; border-left: 6px solid #0f766e; border-radius: 8px; margin-top: 20px; line-height: 1.7; font-size: 1.05rem;}
    
    /* Adjust Slider spacing */
    .stSlider { padding-bottom: 0px; margin-bottom: -15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        if 'Country' in df.columns and 'country' not in df.columns: df['country'] = df['Country']
        if 'New_Prob_Pct' in df.columns: df['Survival_Prob'] = df['New_Prob_Pct'] / 100
        # Fallback values if baseline data is missing
        if 'Base_Prob_Pct' not in df.columns: df['Base_Prob_Pct'] = df.get('New_Prob_Pct', 50) - 5
        if 'Market_Room' not in df.columns: df['Market_Room'] = 0.5
        if 'Purchasing_Power' not in df.columns: df['Purchasing_Power'] = df.get('GDP_per_capita', 50000) / 10000
        return df
    return None

df = load_data()
if df is None:
    st.error("Audit Data missing. Please ensure 'war_room_audit_2025.csv' is in your GitHub repository.")
    st.stop()

# --- 3. AUDIT INTELLIGENCE ENGINE ---
def get_comprehensive_intel(country, c_data, custom_roi):
    intel = {
        "Germany": (
            "⚠️ Constitutional Crisis & The Subsidy Cliff",
            "**2023-2024 Regime Shift:** In December 2023, the German Federal Constitutional Court struck down €60 billion in climate funding. This forced the immediate, premature cancellation of the *Umweltbonus* (up to €4,500 per EV). Consequently, H1 2024 saw a 35% collapse in domestic EV sales. European OEMs have formally delayed their ICE phase-out targets as a result.",
            f"**Strategic ROI ({custom_roi:.1f}):** The AI model correctly identifies structural utility, but the extreme political volatility makes this a high-risk capital deployment zone. Auditor discretion is required regarding the sustainability of growth without state aid."
        ),
        "USA": (
            "🛡️ IRA Deployment & Section 301 Trade Walls",
            "**2023-2024 Regime Shift:** The US market underwent a structural isolation event. In May 2024, the Biden Administration enacted 100% Section 301 tariffs on Chinese EVs, effectively blocking BYD and NIO from undercutting domestic OEMs. Growth is secured by long-term IRA tax credits locked through 2030.",
            f"**Strategic ROI ({custom_roi:.1f}):** Classified as a 'Safe Haven' with massive Protected Alpha. High wealth and artificially protected margins yield top-tier infrastructure ROI, virtually eliminating European-style 'Subsidy Cliff' risks."
        ),
        "India": (
            "🌱 Local Manufacturing Subsidy Overhauls",
            "**2023-2024 Regime Shift:** Flagship FAME-II subsidies were replaced by the EMPS 2024 scheme. Crucially, India slashed EV import taxes (down to 15%) for global automakers *only if* they commit to investing at least $500M in local manufacturing. This sparked a race for supply chain localization.",
            f"**Strategic ROI ({custom_roi:.1f}):** India possesses astronomical 'Market Room'. The AI views the transition to manufacturing-incentives as a positive long-term resilience indicator. The 0.82 Opportunity Gap suggests India is the primary 'Sleeping Giant' for 2026."
        )
    }
    
    if country not in intel:
        gap = c_data.get('Opportunity_Gap', 0)
        dyn_headline = f"🔍 Structural Resilience Audit"
        dyn_context = f"**2023-2024 Market Dynamics:** {country} exhibits a Risk-Adjusted Confidence of {c_data.get('New_Prob_Pct', 0):.1f}%. Adoption is following organic GDP S-Curve modeling, rather than being driven by sudden, disruptive geopolitical black-swan events."
        dyn_roi = f"**Strategic ROI ({custom_roi:.1f}):** The AI weighed structural purchasing power against infrastructure saturation. Auditor judgment is advised based on the Opportunity Gap of {gap:.2f}."
        return (dyn_headline, dyn_context, dyn_roi)
    return intel[country]

# --- 4. THE FINAL POP-UP REPORT (SAME AS IMAGE) ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_safe, w_room, w_wealth):
    c_data = df[df['country'] == country].iloc[0]
    
    # ROI Re-calculation
    custom_roi = ((c_data['Survival_Prob']**w_safe) * (c_data['Market_Room']**w_room) * (c_data['Purchasing_Power']**w_wealth)) / (1+0.5) * 100
    headline, context, roi_justification = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 0;'>Strategic Target: {country}</h2>", unsafe_allow_html=True)
    
    # Section 1: Classifications
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        # Using 20% as a takeoff threshold
        status = "🚀 Takeoff Phase" if c_data.get('lagged_share', 0) < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* Market exhibits {c_data.get('lagged_share', 0):.1f}% adoption. Capital deployment into markets under 20% yields highest exponential returns.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data['New_Prob_Pct'] >= 78 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* Model predicts a {c_data['New_Prob_Pct']:.1f}% probability of sustained expansion in a strict, zero-subsidy environment.")

    st.markdown("---")
    
    # Section 2: Regime Shift Analytics
    st.markdown("### 2. Regime Shift Analytics (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    
    ai_conf = c_data.get('New_Prob_Pct', 0)
    base_conf = c_data.get('Base_Prob_Pct', 0)
    
    m1.metric("Current AI Confidence", f"{ai_conf:.1f}%", f"{ai_conf - base_conf:+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('Opportunity_Gap', 0):.2f}", "Alpha Index")
    m3.metric("ROI Potential Index", f"{custom_roi:.1f}", "Scaled Score")

    # Section 3: Deep Intelligence Box
    st.markdown(f"""
    <div class='intel-box'>
        <h4 style='color: #0f766e; margin-top: 0;'>📰 Geopolitical & Policy Context: {headline}</h4>
        <p>{context}</p>
        <hr style="border: 1px solid #cbd5e1;">
        <h4 style='color: #0f766e;'>💰 ROI Justification & Verdict</h4>
        <p>{roi_justification}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SINGLE-PAGE LAYOUT ---
st.markdown("<h2 style='color: #0f766e; margin-bottom: 5px;'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.5, 2.5], gap="medium")

with col_map:
    fig = px.choropleth(
        df, locations=df["country"], locationmode='country names', 
        color="ROI_Score", hover_name="country", color_continuous_scale="Teal", 
        projection="natural earth"
    )
    fig.update_geos(showland=True, landcolor="#f1f5f9", showocean=True, oceancolor="#ffffff", showframe=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550, coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)')
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    selected_country = None
    if map_click and map_click["selection"]["points"]:
        selected_country = map_click["selection"]["points"][0]["hovertext"]
    
    if selected_country:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 0; color: #1e293b;'>🎯 Target: {selected_country}</h3>", unsafe_allow_html=True)
        
        st.metric("ROI Score", f"{c_data.get('ROI_Score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('New_Prob_Pct', 0):.1f}%")
        
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("**⚙️ Configuration Mandate**")
        w_safe = st.slider("🛡️ Resilience Weight", 0.0, 2.0, 1.0, step=0.1)
        w_room = st.slider("📈 Market Room Weight", 0.0, 2.0, 1.0, step=0.1)
        w_wealth = st.slider("💰 Wealth Weight", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, w_safe, w_room, w_wealth)
    else:
        st.markdown("<h3 style='margin-top: 0; color: #1e293b;'>🌍 Portfolio Audit</h3>")
        st.metric("Capital Mandate", "$100M")
        st.metric("System Precision", "67.74%")
        st.info("Select a market on the map to run the strategic intelligence audit.")
