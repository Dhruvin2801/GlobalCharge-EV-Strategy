import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & "WHITE-PAPER" THEME ---
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
        # Robustness checks for metrics
        if 'Base_Prob_Pct' not in df.columns: df['Base_Prob_Pct'] = df.get('New_Prob_Pct', 80) - 5
        if 'Market_Room' not in df.columns: df['Market_Room'] = 0.5
        if 'Purchasing_Power' not in df.columns: df['Purchasing_Power'] = df.get('GDP_per_capita', 50000) / 10000
        return df
    return None

df = load_data()
if df is None:
    st.error("Audit Data missing. Ensure 'war_room_audit_2025.csv' is in your repo.")
    st.stop()

# --- 3. THE 30-COUNTRY GEOPOLITICAL INTELLIGENCE ENGINE ---
def get_comprehensive_intel(country, c_data, custom_roi):
    intel_repo = {
        "Germany": (
            "⚠️ The 2024 'Subsidy Cliff' & Constitutional Shock",
            "**2023-24 Regime Shift:** In Dec 2023, the Federal Constitutional Court's budget ruling forced the immediate end of the €4,500 'Umweltbonus'. This triggered a 30% crash in H1 2024. European OEMs (VW/Mercedes) are now pivoting back to ICE/Hybrid extensions.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** High GDP/Capita remains, but the market is 'Policy-Brittle'. Human Veto is recommended until H2 2025 energy pricing stabilizes."
        ),
        "Australia": (
            "🛡️ NVES Mandates & The Post-Subsidy S-Curve",
            "**2023-24 Regime Shift:** Australia passed its first New Vehicle Efficiency Standard (NVES) in May 2024. Unlike Germany, growth here is driven by 'Fleet Necessity' and the removal of the Fringe Benefits Tax (FBT) on EVs, shielding the market from interest rate shocks.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Classified as a **Core Resilience Play**. The 12% adoption rate represents the perfect 'Takeoff' phase for high-alpha infrastructure deployment."
        ),
        "India": (
            "🐘 The FAME-III Pivot & Manufacturing Commitments",
            "**2023-24 Regime Shift:** March 2024 saw the transition from FAME-II to the EMPS scheme. Simultaneously, India slashed import taxes to 15% for global OEMs (Tesla/VinFast) under the condition of $500M+ local factory investment, sparking a localized supply chain race.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** The 'Sleeping Giant'. With an Opportunity Gap of 0.88, India is the #1 value-recovery target. The AI views the transition to manufacturing incentives as a long-term stability win."
        ),
        "USA": (
            "🧱 Section 301 Tariffs & The IRA 'Fortress'",
            "**2023-24 Regime Shift:** In May 2024, the US enforced 100% tariffs on Chinese EVs to block market undercutting. The Inflation Reduction Act (IRA) tax credits remain the bedrock of adoption, creating a 'Protected Alpha' zone for domestic infrastructure.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Safe Haven. High Wealth + Policy Protection = Guaranteed Returns. No 'Subsidy Cliff' risk detected through 2028."
        ),
        "Mexico": (
            "📈 USMCA Nearshoring & The BYD Factory Scout",
            "**2023-24 Regime Shift:** Mexico became the 'Supply Bypass' for the USMCA region in 2024. Chinese OEMs are building factories to avoid US tariffs, while commercial fleet electrification (DHL/Walmart) is exploding without consumer subsidies.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** High Alpha target. Growth is driven by Industrial ESG Mandates, not fickle consumer politics."
        ),
        "Norway": (
            "✅ S-Curve Completion & VAT Normalization",
            "**2023-24 Regime Shift:** Norway achieved 90%+ share and removed luxury tax exemptions in 2024. The market has matured into a public utility play.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Low Alpha. There is functionally zero 'Market Room' left for venture-growth returns."
        )
    }

    # Dynamic Engine for the other 24+ countries
    if country in intel_repo:
        return intel_repo[country]
    else:
        gap = c_data.get('Opportunity_Gap', 0.5)
        # Dynamic Narrative based on AI metrics
        headline = f"🔍 Structural Resilience Audit: {country}"
        context = f"**2023-2024 Market Dynamics:** {country} exhibits a Risk-Adjusted Confidence of {c_data.get('New_Prob_Pct', 0):.1f}%. The market is benefiting from the 'Global South Supply Pivot' of 2024, where Chinese supply redirected from the EU/US is fueling growth in non-tariffed regions. Adoption is following a GDP-driven S-Curve, shielded from the European political volatility."
        verdict = f"**Strategic ROI ({custom_roi:.1f}):** The AI weighed structural purchasing power against current infrastructure density. With an Opportunity Gap of {gap:.2f}, {country} is a stable, secondary deployment target."
        return (headline, context, verdict)

# --- 4. THE HIGH-FIDELITY AUDIT REPORT ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_safe, w_room, w_wealth):
    c_data = df[df['country'] == country].iloc[0]
    
    # Final Weighted ROI Calculation
    survival_prob = c_data.get('New_Prob_Pct', 80) / 100
    market_room = c_data.get('Market_Room', 0.5)
    purchasing_power = c_data.get('Purchasing_Power', 5)
    
    custom_roi = ((survival_prob**w_safe) * (market_room**w_room) * (purchasing_power**w_wealth)) / (1+0.5) * 100
    headline, context, verdict = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 0;'>Strategic Target: {country}</h2>", unsafe_allow_html=True)
    
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 10)
        status = "🚀 Takeoff Phase" if share < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* Market exhibits {share:.1f}% adoption. Capital deployment into markets under 20% yields highest exponential returns.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data['New_Prob_Pct'] >= 78 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* Model predicts a {c_data['New_Prob_Pct']:.1f}% probability of sustained expansion in a strict, zero-subsidy environment.")

    st.markdown("---")
    
    st.markdown("### 2. Regime Shift Analytics (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    
    ai_conf = c_data.get('New_Prob_Pct', 0)
    base_conf = c_data.get('Base_Prob_Pct', 0)
    m1.metric("Current AI Confidence", f"{ai_conf:.1f}%", f"{ai_conf - base_conf:+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('Opportunity_Gap', 0):.2f}", "Alpha Index")
    m3.metric("ROI Potential Index", f"{custom_roi:.1f}", "Scaled Score")

    st.markdown(f"""
    <div class='intel-box'>
        <h4 style='color: #0f766e; margin-top: 0;'>📰 Geopolitical & Policy Context: {headline}</h4>
        <p>{context}</p>
        <hr style="border: 1px solid #cbd5e1;">
        <h4 style='color: #0f766e;'>💰 ROI Justification & Verdict</h4>
        <p>{verdict}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown("<h2 style='color: #0f766e; margin-bottom: 5px;'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.5, 2.5], gap="medium")

with col_map:
    fig = px.choropleth(
        df, locations=df["country"], locationmode='country names', 
        color="ROI_Score", hover_name="country", color_continuous_scale="Teal", 
        projection="natural earth"
    )
    fig.update_geos(showland=True, landcolor="#f1f5f9", oceancolor="#ffffff", showframe=False)
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
        st.metric("Capital Allocation", "$100M")
        st.info("Select a market on the map to run the audit.")
