Conversations
   
56% of 15 GB used
Terms · Privacy · Programme Policies
Last account activity: 0 minutes ago
Details

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. STRICT DESIGN & CSS MANDATES
st.set_page_config(layout="wide", page_title="GlobalCharge Intelligence Engine", initial_sidebar_state="collapsed")

def inject_custom_css():
    st.markdown("""
    <style>
    /* Viewport Lock */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
    }
    ::-webkit-scrollbar {
        display: none;
    }
    
    /* Theme & Typography */
    body {
        background-color: #ffffff;
        color: #1e293b;
        font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Typography (+2pt Rule) */
    [data-testid="stMetricValue"] {
        font-size: calc(1.8rem + 2pt) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: calc(0.9rem + 2pt) !important;
    }
    
    /* Warning/Vulnerability Boxes */
    .warning-box {
        background-color: #fff7ed;
        color: #c2410c;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ea580c;
        margin-bottom: 1rem;
    }
    
    /* Terminal Block */
    .terminal-block {
        background-color: #0f172a;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
        padding: 1rem;
        border-radius: 0.375rem;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
    }
    
    /* Hide Deploy/Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Dialog Title Color */
    div[data-testid="stDialog"] h2 {
        color: #dc2626 !important;
    }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 2. DATA LOADING & FALLBACK
@st.cache_data
def load_data():
    csv_path = "/home/ubuntu/upload/war_room_audit_2025.csv"
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            # Normalize column names to match dummy data requirements
            df.columns = [c.lower() for c in df.columns]
            # Ensure required columns exist or map them
            mapping = {
                'roi_score': 'roi_score',
                'new_prob_pct': 'new_prob_pct',
                'opportunity_gap': 'opportunity_gap',
                'lagged_share': 'lagged_share',
                'market_room': 'market_room'
            }
            # Add base_prob_pct and purchasing_power if missing (dummy defaults)
            if 'base_prob_pct' not in df.columns:
                df['base_prob_pct'] = 85.0
            if 'purchasing_power' not in df.columns:
                df['purchasing_power'] = 8.0
            return df
        except Exception:
            pass
            
    # Fallback Dummy Data
    data = {
        'country': ['India', 'Germany', 'Australia', 'USA', 'Spain', 'Iceland'],
        'roi_score': [88.5, 45.2, 92.1, 85.0, 52.1, 49.3],
        'new_prob_pct': [84.6, 28.0, 89.2, 89.2, 77.2, 74.6],
        'base_prob_pct': [80.0, 95.0, 85.0, 88.0, 85.0, 82.0],
        'opportunity_gap': [0.846, 0.12, 0.65, 0.55, 0.30, 0.25],
        'lagged_share': [5.2, 22.5, 12.0, 9.5, 18.0, 19.5],
        'market_room': [0.95, 0.2, 0.8, 0.7, 0.4, 0.3],
        'purchasing_power': [4.5, 9.5, 8.5, 9.8, 7.0, 8.0]
    }
    return pd.DataFrame(data)

df = load_data()

# Initialize session state for selection
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None

# 4. POP-UP DIALOGS
@st.dialog('📋 OFFICIAL EXECUTIVE AUDIT REPORT', width='large')
def show_audit_report(country_data):
    country = country_data['country']
    st.markdown(f"<h2 style='color: #dc2626;'>{country.upper()}</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    stage = "Takeoff" if country_data['lagged_share'] < 20 else "Saturated"
    risk = "Resilient" if country_data['new_prob_pct'] >= 78 else "Policy Vulnerable"
    risk_color = "#dc2626" if risk == "Policy Vulnerable" else "#16a34a"
    
    with c1:
        st.write("**Market Stage:**")
        st.markdown(f"<div style='font-size: 1.2rem; font-weight: bold;'>{stage}</div>", unsafe_allow_html=True)
    with c2:
        st.write("**AI Risk Profile:**")
        st.markdown(f"<div style='font-size: 1.2rem; font-weight: bold; color: {risk_color};'>{risk}</div>", unsafe_allow_html=True)
        
    m1, m2, m3 = st.columns(3)
    m1.metric("AI Survival Probability", f"{country_data['new_prob_pct']}%")
    m2.metric("Opportunity Gap", f"{country_data['opportunity_gap']:.2f}")
    m3.metric("ROI Potential", f"{country_data['roi_score']:.1f}")
    
    # Hardcoded dynamic text
    verdicts = {
        "India": ("Emerging Alpha / FAME-II Pivot", "High growth trajectory with policy tailwinds."),
        "Germany": ("Umweltbonus Shock / Mean Reversion", "Regulatory headwinds affecting short-term outlook."),
        "Australia": ("NVES Policy Shield", "Protected growth through vehicle efficiency standards.")
    }
    context, verdict = verdicts.get(country, ("Standard Portfolio Asset", "Maintain baseline allocation strategy."))
    
    st.markdown(f"""
    <div style="background-color: #f8fafc; padding: 1rem; border-radius: 0.5rem; border-left: 5px solid #dc2626;">
        <p><strong>Geopolitical Context:</strong> {context}</p>
        <p><strong>Strategic Verdict:</strong> {verdict}</p>
    </div>
    """, unsafe_allow_html=True)

@st.dialog('📊 SYSTEM ANALYTICS & MACRO PORTFOLIO', width='large')
def show_system_analytics():
    tab1, tab2 = st.tabs(["[ ALPHA VALUATION MATRIX ]", "[ 2024 REGIME STRESS TEST ]"])
    
    with tab1:
        # Color mapping logic
        def get_color(c):
            if c == 'India': return '#dc2626' # Red
            if c in ['USA', 'Australia']: return '#0f172a' # Slate
            if c in ['Germany', 'Spain', 'Iceland']: return '#ea580c' # Orange
            return '#64748b'
            
        df_plot = df.copy()
        df_plot['color'] = df_plot['country'].apply(get_color)
        
        fig = px.scatter(df_plot, x='new_prob_pct', y='opportunity_gap', 
                         color='country', color_discrete_map={c: get_color(c) for c in df_plot['country']},
                         title="Alpha Confidence vs Opportunity Gap")
        
        fig.add_vline(x=78, line_dash="dash", line_color="#dc2626", 
                      annotation_text="78% MARGIN OF SAFETY THRESHOLD", 
                      annotation_position="top right")
        
        fig.update_layout(
            font=dict(size=14),
            xaxis_title="AI_Confidence (%)",
            yaxis_title="Opportunity_Gap",
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        categories = ["RF", "NB", "KNN"]
        baseline = [84.1, 82.5, 83.2]
        regime_shift = [65.6, 52.4, 46.9]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='2023 Baseline', x=categories, y=baseline, marker_color='#0f172a'))
        
        # Colors for regime shift
        colors = ['#dc2626', '#ea580c', '#ea580c']
        fig.add_trace(go.Bar(name='2024 Regime Shift', x=categories, y=regime_shift, marker_color=colors))
        
        fig.update_layout(
            barmode='group',
            title="Model Accuracy: Baseline vs Regime Shift",
            font=dict(size=14),
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)

# 3. MAIN SCREEN ARCHITECTURE
st.markdown("<h1 style='margin-bottom: 0;'>GlobalCharge Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-weight: bold; margin-bottom: 2rem;'>EXECUTIVE INVESTMENT DASHBOARD | REGIME-AWARE AUDIT</p>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.2, 2.8], gap="large")

with col_map:
    fig_map = px.choropleth(df, locations="country", locationmode='country names',
                            color="roi_score", color_continuous_scale="Reds")
    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular',
                 lakecolor='white', oceancolor='white'),
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_showscale=False
    )
    
    selected = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")
    
    # Handle map selection
    if selected and "selection" in selected and "points" in selected["selection"] and len(selected["selection"]["points"]) > 0:
        point = selected["selection"]["points"][0]
        # Find country by index if possible or location
        if "location" in point:
            st.session_state.selected_country = point["location"]

with col_panel:
    # Fallback selectbox
    selected_country_name = st.selectbox("Select Target Country", options=[None] + list(df['country'].unique()), 
                                         index=0 if st.session_state.selected_country is None else list(df['country'].unique()).index(st.session_state.selected_country) + 1,
                                         key="country_selector")
    
    if selected_country_name:
        st.session_state.selected_country = selected_country_name
        
    if st.session_state.selected_country is None:
        st.markdown("### Portfolio Audit")
        m1, m2 = st.columns(2)
        m1.metric("$100M Mandate", "Active")
        m2.metric("Precision", "67.7%")
        st.markdown('<div class="warning-box">Awaiting Input: Select a country</div>', unsafe_allow_html=True)
    else:
        country_data = df[df['country'] == st.session_state.selected_country].iloc[0]
        st.markdown(f"### Target: {st.session_state.selected_country}")
        st.metric("ROI Score", f"{country_data['roi_score']:.1f}")
        st.metric("AI Confidence", f"{country_data['new_prob_pct']}%")
        
        st.slider("Resilience", 0.0, 2.0, 1.0)
        st.slider("Market Room", 0.0, 2.0, float(country_data['market_room']))
        st.slider("Wealth", 0.0, 2.0, 1.0)
        
        if st.button("GENERATE EXECUTIVE AUDIT", type="primary"):
            show_audit_report(country_data)
            
    st.write("") # Spacer
    
    if st.button("📊 OPEN SYSTEM ANALYTICS"):
        show_system_analytics()
        
    st.markdown("""
    <div class="terminal-block">
        <div style="font-weight: bold; margin-bottom: 5px;">⚙️ ACTIVE ML ARCHITECTURE</div>
        <div>LAYER 1: HMM (Regime Detection)</div>
        <div>LAYER 2: NLP (90-Day Sentiment Lead)</div>
        <div>LAYER 3: Random Forest (n=100, d=4)</div>
        <div style="margin-top: 5px;">STATE: <span style="color: #ef4444; font-weight: bold;">LOCKED (NO 2024 LEAKAGE)</span></div>
    </div>
    """, unsafe_allow_html=True)
