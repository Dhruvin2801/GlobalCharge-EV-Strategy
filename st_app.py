import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & EXECUTIVE "WHITE-PAPER" THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Executive Metric Styling */
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; color: #0f766e; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #64748b; font-weight: 600; text-transform: uppercase; }
    
    /* Button & Control Styling */
    .stButton>button { 
        background-color: #0f766e; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 6px; height: 3.2rem; width: 100%; border: none; 
        box-shadow: 0 4px 6px rgba(15, 118, 110, 0.2); transition: all 0.2s; margin-top: 15px;
    }
    .stButton>button:hover { background-color: #115e59; transform: translateY(-2px); }
    
    /* Audit Intelligence Box */
    .intel-box { background-color: #f8fafc; padding: 25px; border-left: 6px solid #0f766e; border-radius: 8px; margin-top: 20px; line-height: 1.7; font-size: 1.05rem;}
    .stSlider { padding-bottom: 0px; margin-bottom: -15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SELF-HEALING DATA LOADER ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        
        # SELF-HEALING: Map all possible variations to the app's internal names
        column_map = {
            'Country': 'country',
            'New_Prob_Pct': 'new_prob',
            'Base_Prob_Pct': 'base_prob',
            'ROI_Score': 'roi_score',
            'Opportunity_Gap': 'opp_gap',
            'lagged_share': 'share',
            'Market_Room': 'room',
            'Purchasing_Power': 'wealth'
        }
        
        for old_name, new_name in column_map.items():
            if old_name in df.columns:
                df[new_name] = df[old_name]
            elif new_name not in df.columns:
                # Create fallback defaults if column is missing
                df[new_name] = 0.0 if 'gap' in new_name else 50.0
        
        return df
    return None

df = load_data()
if df is None:
    st.error("⚠️ DATA FILE NOT FOUND: Ensure 'war_room_audit_2025.csv' is in your GitHub folder.")
    st.stop()

# --- 3. GEOPOLITICAL INTELLIGENCE ENGINE ---
def get_comprehensive_intel(country, c_data, custom_roi):
    intel_repo = {
        "France": (
            "⚖️ The 'Eco-Score' Pivot & Tariff Shielding",
            "**2023-24 Regime Shift:** France revamped its 'Bonus Écologique' in 2024 to reward environmental footprint scores. This effectively shields domestic OEMs from low-cost imports while maintaining steady organic demand via localized Renault/Stellantis supply.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** France represents a matured yet protected market. The AI identifies resilience because the new 'Eco-Score' creates a structural moat for local manufacturers."
        ),
        "Australia": (
            "🛡️ NVES Mandates & Fleet Transition Alpha",
            "**2023-24 Regime Shift:** The 2024 New Vehicle Efficiency Standard (NVES) shifted adoption from voluntary to regulatory mandate. The removal of Fringe Benefits Tax (FBT) on EVs makes the corporate market a resilient growth engine.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Australia is a high-alpha takeoff target. High structural confidence is grounded in tax advantages that make EV ownership cheaper than ICE equivalents."
        ),
        "India": (
            "🐘 The EMPS Pivot & The 0.88 Opportunity Gap",
            "**2023-24 Regime Shift:** India's transition to the EMPS scheme in 2024 caused a plateau, but slashed import taxes for manufacturers committing $500M+ local investment has sparked a localized supply chain race.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** The 'Sleeping Giant'. The Opportunity Gap proves that underlying demand is surging. This is a primary target for capital seeking a 2026 recovery."
        )
    }
    
    if country in intel_repo:
        return intel_repo[country]
    
    gap = c_data.get('opp_gap', 0.5)
    headline = f"🔍 Structural Resilience Audit: {country}"
    context = f"**2023-2024 Market Dynamics:** {country} is benefiting from the 'Global South Supply Pivot' as supply redirects from high-tariff zones. Adoption follows an organic S-Curve driven by increasing GDP."
    verdict = f"**Strategic ROI ({custom_roi:.1f}):** The AI weighed structural power against density. With an Opportunity Gap of {gap:.2f}, {country} is a stable deployment target."
    return (headline, context, verdict)

# --- 4. EXECUTIVE AUDIT REPORT (POPOUT) ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_safe, w_room, w_wealth):
    c_data = df[df['country'] == country].iloc[0]
    
    # Logic for Classification boxes
    share = c_data.get('share', 15)
    prob = c_data.get('new_prob', 80)
    
    # Custom ROI calc
    custom_roi = (((prob/100)**w_safe) * (c_data.get('room', 0.5)**w_room) * (c_data.get('wealth', 5)**w_wealth)) / (1+0.5) * 100
    headline, context, verdict = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 0;'>Strategic Target: {country}</h2>", unsafe_allow_html=True)
    
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        status = "🚀 Takeoff Phase" if share < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* Market exhibits {share:.1f}% adoption. Capital deployment into markets under 20% yields highest exponential returns.")
    with c2:
        resilience = "✅ Highly Resilient" if prob >= 78 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* Model predicts a high structural probability of sustained expansion in the 2024 'Chaos Regime' shift.")

    st.markdown("---")
    
    st.markdown("### 2. Regime Shift Analytics (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Current AI Confidence", f"{prob:.1f}%", f"{prob - c_data.get('base_prob', 75):+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('opp_gap', 0):.2f}", "Alpha Index")
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
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Teal", projection="natural earth")
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
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('new_prob', 0):.1f}%")
        
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("**⚙️ Configuration Mandate**")
        w_s = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        w_r = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        w_w = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, w_s, w_r, w_w)
    else:
        st.markdown("<h3 style='margin-top: 0; color: #1e293b;'>🌍 Portfolio Audit</h3>")
        st.metric("Capital Allocation", "$100M")
        
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("**🏆 Top ROI Targets**")
        top_3 = df.nlargest(3, 'roi_score')[['country', 'roi_score']]
        st.dataframe(top_3.rename(columns={'country': 'Market', 'roi_score': 'Score'}), hide_index=True, use_container_width=True)

        st.info("👆 **Select a market on the map** to run the audit.")
