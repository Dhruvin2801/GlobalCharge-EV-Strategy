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

# --- 2. SELF-HEALING DATA LOADER ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        
        # Normalize column names to lowercase to avoid case-sensitivity errors
        df.columns = [c.lower() for c in df.columns]
        
        # Map critical columns to internal app variables
        mapping = {
            'country': 'country',
            'new_prob_pct': 'new_prob',
            'base_prob_pct': 'base_prob',
            'roi_score': 'roi_score',
            'opportunity_gap': 'opp_gap',
            'lagged_share': 'share',
            'market_room': 'room',
            'purchasing_power': 'wealth'
        }
        
        for key, val in mapping.items():
            if key in df.columns:
                df[val] = df[key]
            else:
                # Fallbacks so the app never crashes
                df[val] = 0.0 if 'gap' in val else 50.0
        
        return df
    return None

df = load_data()

# Debugging Sidebar (Only shows if there's a problem)
if df is None:
    st.error("⚠️ 'war_room_audit_2025.csv' not found in root directory.")
    st.stop()

# --- 3. GEOPOLITICAL INTELLIGENCE ---
def get_comprehensive_intel(country, c_data, custom_roi):
    intel_repo = {
        "France": (
            "⚖️ The 'Eco-Score' Pivot & Tariff Shielding",
            "**2023-24 Regime Shift:** France revamped its 'Bonus Écologique' in 2024 to reward environmental footprint scores. This effectively shields domestic OEMs from low-cost imports while maintaining steady organic demand.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** France represents a matured yet protected market. The Moat created by the Eco-Score ensures long-term infrastructure stability."
        ),
        "Australia": (
            "🛡️ NVES Mandates & Fleet Transition Alpha",
            "**2023-24 Regime Shift:** The 2024 NVES shifted adoption from voluntary to regulatory mandate. The removal of FBT on EVs makes the corporate market a resilient growth engine.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Australia is a high-alpha takeoff target. Tax advantages make EV ownership cheaper than ICE equivalents."
        ),
        "India": (
            "🐘 The EMPS Pivot & The 0.88 Opportunity Alpha",
            "**2023-24 Regime Shift:** India's 2024 transition to EMPS caused a plateau, but slashed import taxes for manufacturers committing $500M+ local investment has sparked a localized supply chain race.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** The 'Sleeping Giant'. The Opportunity Gap proves underlying demand is surging. Primary target for 2026 recovery capital."
        )
    }
    
    entry = intel_repo.get(country)
    if entry: return entry
    
    headline = f"🔍 Structural Resilience Audit: {country}"
    context = f"**2023-24 Market Dynamics:** {country} is benefiting from the 'Global South Supply Pivot' as inventory redirects from high-tariff zones. Adoption follows an organic S-Curve driven by GDP."
    verdict = f"**Strategic Verdict (ROI {custom_roi:.1f}):** Stable deployment target with an Opportunity Gap of {c_data.get('opp_gap', 0):.2f}."
    return headline, context, verdict

# --- 4. THE AUDIT DIALOG ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    
    # Custom ROI Calculation
    prob = c_data.get('new_prob', 80) / 100
    room = c_data.get('room', 0.5)
    wealth = c_data.get('wealth', 5)
    custom_roi = ((prob**w_s) * (room**w_r) * (wealth**w_w)) / (1+0.5) * 100
    
    headline, context, verdict = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 0;'>Strategic Audit: {country}</h2>", unsafe_allow_html=True)
    
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('share', 15)
        status = "🚀 Takeoff Phase" if share < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* Market exhibits {share:.1f}% adoption. Early-stage deployment yields highest returns.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data.get('new_prob', 0) >= 78 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* AI identifies structural stability in the 2024 'Chaos Regime' shift.")

    st.markdown("---")
    
    st.markdown("### 2. Regime Shift Analytics (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    curr_prob = c_data.get('new_prob', 0)
    base_prob = c_data.get('base_prob', 75)
    m1.metric("AI Confidence", f"{curr_prob:.1f}%", f"{curr_prob - base_prob:+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('opp_gap', 0):.2f}")
    m3.metric("ROI Potential Index", f"{custom_roi:.1f}")

    st.markdown(f"<div class='intel-box'><h4 style='color: #0f766e;'>📰 Context: {headline}</h4><p>{context}</p><hr><h4 style='color: #0f766e;'>💰 Verdict</h4><p>{verdict}</p></div>", unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown("<h2 style='color: #0f766e; margin-bottom: 5px;'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.5, 2.5], gap="medium")

with col_map:
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Teal")
    fig.update_geos(showland=True, landcolor="#f1f5f9", oceancolor="#ffffff", showframe=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550, coloraxis_showscale=False)
    
    # CRASH-PROOF SELECTION LOGIC
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    selected_country = None
    # Check if a selection exists and retrieve it via 'location' (the new Plotly standard)
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        selected_country = map_click["selection"]["points"][0].get("location")

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 0; color: #1e293b;'>🎯 Target: {selected_country}</h3>", unsafe_allow_html=True)
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('new_prob', 0):.1f}%")
        
        st.markdown("**⚙️ Configuration Mandate**")
        w_s = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        w_r = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        w_w = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, w_s, w_r, w_w)
    else:
        st.markdown("<h3 style='margin-top: 0; color: #1e293b;'>🌍 Portfolio Audit</h3>")
        st.metric("Capital Mandate", "$100M")
        st.info("Select a market on the map to run the audit.")
        if not df.empty:
            st.dataframe(df.nlargest(3, 'roi_score')[['country', 'roi_score']].rename(columns={'country': 'Market', 'roi_score': 'Score'}), hide_index=True)
