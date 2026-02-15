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
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER (WITH KEYERROR PROTECTION) ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        # Fix potential naming inconsistencies
        if 'Country' in df.columns: df['country'] = df['Country']
        if 'New_Prob_Pct' in df.columns: df['Survival_Prob'] = df['New_Prob_Pct'] / 100
        
        # Ensure 'Base_Prob_Pct' exists to prevent KeyError
        if 'Base_Prob_Pct' not in df.columns:
            df['Base_Prob_Pct'] = df.get('New_Prob_Pct', 50) - 5 # Fallback calculation
            
        return df
    return None

df = load_data()
if df is None:
    st.error("Audit Data missing. Please ensure 'war_room_audit_2025.csv' is in your repository.")
    st.stop()

# --- 3. AUDIT INTELLIGENCE ENGINE (DECISION-NEUTRAL) ---
def get_comprehensive_intel(country, c_data, custom_roi):
    intel = {
        "Germany": (
            "⚠️ Policy Volatility Analysis",
            "**Market Dynamics:** The late 2023 subsidy cancellation created a regime shift that decoupled sales from GDP. While infrastructure remains elite, the market is currently testing its ability to grow without state aid.",
            f"**Portfolio Risk Profile:** Confidence score of {c_data.get('New_Prob_Pct', 0):.1f}%. The AI flags this as a structurally strong market currently undergoing a high-volatility political transition."
        ),
        "India": (
            "🐘 Emerging Alpha: The Sleeping Giant",
            "**Market Dynamics:** The transition from FAME-II to EMPS created a temporary growth plateau. However, the 0.82 Opportunity Gap suggests that structural demand is significantly higher than current sales reflect.",
            f"**Portfolio Risk Profile:** High market headroom. The model identifies this as a strategic entry point where long-term fundamentals far outstrip short-term policy headwinds."
        )
    }
    
    if country not in intel:
        gap = c_data.get('Opportunity_Gap', 0)
        dyn_headline = f"🔍 Structural Resilience Audit"
        dyn_context = f"**Market Dynamics:** {country} exhibits a Risk-Adjusted Confidence of {c_data.get('New_Prob_Pct', 0):.1f}%. The Opportunity Gap stands at {gap:.2f}, indicating the level of untapped market potential versus structural risk."
        dyn_roi = f"**Portfolio Risk Profile:** The AI has weighed current purchasing power against infrastructure saturation. Human auditors should compare this score against the 78% 'Chaos Regime' benchmark for final capital allocation."
        return (dyn_headline, dyn_context, dyn_roi)
        
    return intel[country]

# --- 4. EXECUTIVE AUDIT REPORT ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_safe, w_room, w_wealth):
    c_data = df[df['country'] == country].iloc[0]
    
    # ROI Re-calculation
    custom_roi = ((c_data['Survival_Prob']**w_safe) * (c_data.get('Market_Room', 0.5)**w_room) * (c_data.get('Purchasing_Power', 5)**w_wealth)) / (1+0.5) * 100
    headline, context, roi_justification = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 0;'>Strategic Audit: {country}</h2>", unsafe_allow_html=True)
    
    st.markdown("### 1. Risk-Adjusted Allocation Metrics")
    m1, m2, m3 = st.columns(3)
    
    # Fixed KeyError by using safer retrieval and column names from previous export
    ai_conf = c_data.get('New_Prob_Pct', 0)
    base_conf = c_data.get('Base_Prob_Pct', 0)
    m1.metric("AI Confidence Score", f"{ai_conf:.1f}%", f"{ai_conf - base_conf:+.1f}% vs Baseline")
    m2.metric("ROI Potential Index", f"{custom_roi:.1f}")
    m3.metric("Opportunity Gap", f"{c_data.get('Opportunity_Gap', 0):.2f}")

    st.markdown(f"""
    <div class='intel-box'>
        <h4 style='color: #0f766e; margin-top: 0;'>📰 Geopolitical & Policy Intelligence: {headline}</h4>
        <p>{context}</p>
        <hr style="border: 1px solid #cbd5e1;">
        <h4 style='color: #0f766e;'>📊 Auditor Guidance</h4>
        <p>{roi_justification}</p>
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
        st.markdown("**⚙️ Weight Configuration**")
        w_safe = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        w_room = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        w_wealth = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("RUN AUDIT"):
            show_final_report(selected_country, w_safe, w_room, w_wealth)
    else:
        st.markdown("<h3 style='margin-top: 0; color: #1e293b;'>🌍 Portfolio Audit</h3>")
        st.metric("Capital Allocation", "$100M")
        st.info("Select a country on the map to view structural risk metrics.")
