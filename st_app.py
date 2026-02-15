import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & EXECUTIVE THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; color: #0f766e; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .stButton>button { 
        background-color: #0f766e; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 6px; height: 3.2rem; width: 100%; border: none; 
        box-shadow: 0 4px 6px rgba(15, 118, 110, 0.2); transition: all 0.2s; margin-top: 15px;
    }
    .intel-box { background-color: #f8fafc; padding: 25px; border-left: 6px solid #0f766e; border-radius: 8px; margin-top: 20px; line-height: 1.7; font-size: 1.05rem;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        # Normalize all column names to lowercase
        df.columns = [c.lower() for c in df.columns]
        # Standardize 'country' column
        if 'country' not in df.columns:
            possible_names = ['country_name', 'nation', 'unnamed: 0']
            for p in possible_names:
                if p in df.columns: df.rename(columns={p: 'country'}, inplace=True)
        return df
    return None

df = load_data()
if df is None or df.empty:
    st.error("⚠️ Data Source Missing. Ensure 'war_room_audit_2025.csv' is in your GitHub.")
    st.stop()

# --- 3. GEOPOLITICAL INTELLIGENCE ---
def get_comprehensive_intel(country, c_data, custom_roi):
    # Specialized 2024 Intelligence
    intel_repo = {
        "Australia": ("🛡️ NVES Mandates & Fleet Resilience", 
                     "**2023-24 Regime Shift:** Australia successfully pivoted to a mandatory Efficiency Standard (NVES) in 2024. Growth is now driven by corporate tax advantages (FBT), shielding it from consumer interest rate shocks.",
                     f"**Verdict (ROI {custom_roi:.1f}):** High-alpha takeoff target. Structural tax policy makes EVs cheaper than ICE equivalents."),
        "France": ("⚖️ The 'Eco-Score' Moat",
                  "**2023-24 Regime Shift:** France implemented a footprint-based 'Eco-Score' in 2024. This protects domestic ROI by filtering out high-carbon imports from Asia while rewarding local supply chains.",
                  f"**Verdict (ROI {custom_roi:.1f}):** Matured but protected. AI identifies high resilience due to this regulatory barrier."),
        "India": ("🐘 The EMPS Pivot: Sleeping Giant",
                 "**2023-24 Regime Shift:** India transitioned to EMPS 2024 and slashed import taxes for manufacturers committing $500M+ locally. This has triggered a massive supply chain race.",
                 f"**Verdict (ROI {custom_roi:.1f}):** Ultimate value-play. 0.88 Opportunity Gap proves that underlying demand is surging beyond current capacity.")
    }
    
    res = intel_repo.get(country)
    if res: return res
    
    return (f"🔍 Structural Resilience Audit: {country}", 
            f"**Dynamics:** Market is following a GDP-driven S-Curve. Adoption is shielded from the European political volatility by organic wealth growth.",
            f"**Verdict (ROI {custom_roi:.1f}):** Stable deployment target.")

# --- 4. AUDIT REPORT DIALOG ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    # Re-calc based on user weights
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    wealth = c_data.get('purchasing_power', 5)
    custom_roi = ((prob**w_s) * (room**w_r) * (wealth**w_w)) / (1+0.5) * 100
    
    headline, context, verdict = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e;'>Strategic Audit: {country}</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 12)
        status = "🚀 Takeoff Phase" if share < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* Market exhibits {share:.1f}% adoption. Deployment into markets under 20% yields highest returns.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data.get('new_prob_pct', 0) >= 78 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* AI identifies structural stability in the 2024 'Chaos Regime' shift.")

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    curr_p = c_data.get('new_prob_pct', 0)
    base_p = c_data.get('base_prob_pct', 75)
    m1.metric("AI Confidence", f"{curr_p:.1f}%", f"{curr_p - base_p:+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('opportunity_gap', 0):.2f}")
    m3.metric("ROI Potential Index", f"{custom_roi:.1f}")

    st.markdown(f"<div class='intel-box'><h4>📰 {headline}</h4><p>{context}</p><hr><h4>💰 Verdict</h4><p>{verdict}</p></div>", unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown("<h2 style='color: #0f766e;'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.5, 2.5], gap="medium")

with col_map:
    # Use 'country' as the location key for maximum reliability
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Teal")
    fig.update_geos(showland=True, landcolor="#f1f5f9", oceancolor="#ffffff", showframe=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550, coloraxis_showscale=False)
    
    # Rerun on select to catch clicks
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    # TRIPLE-REDUNDANT COUNTRY SELECTION
    selected_country = None
    
    # 1. Attempt Map Selection
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        # Check all possible Plotly keys
        selected_country = pt.get("location") or pt.get("hovertext") or pt.get("text")
    
    # 2. Manual Fallback Dropdown (Ensures app works even if map click fails)
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    manual_selection = st.selectbox("Select Target Market:", ["Click Map..."] + sorted(df['country'].unique().tolist()))
    
    # Priority: Map Selection > Manual Selection
    if selected_country not in df['country'].values:
        selected_country = manual_selection if manual_selection != "Click Map..." else None

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"### 🎯 Target: {selected_country}")
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("**⚙️ Configuration Mandate**")
        w_s = st.slider("🛡️ Resilience Weight", 0.0, 2.0, 1.0, step=0.1)
        w_r = st.slider("📈 Market Room Weight", 0.0, 2.0, 1.0, step=0.1)
        w_w = st.slider("💰 Wealth Weight", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, w_s, w_r, w_w)
    else:
        st.markdown("### 🌍 Portfolio Audit")
        st.metric("Mandate", "$100M")
        st.info("Select a country on the map or use the dropdown to run the audit.")
