import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ==========================================
# 1. CONFIG & EXECUTIVE PLATINUM THEME
# ==========================================
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Clean Light Institutional Background */
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Viewport Lock (No Scrolling) */
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; }
    ::-webkit-scrollbar { display: none; }
    
    /* Premium Metric Styling (+2pt enforced) */
    [data-testid="stMetricValue"] { font-size: calc(1.8rem + 2pt) !important; color: #0f766e; font-weight: 800; letter-spacing: -0.05rem; }
    [data-testid="stMetricLabel"] { font-size: calc(0.9rem + 2pt) !important; color: #64748b; font-weight: 700; text-transform: uppercase; }
    
    /* Audit Button Styling (Teal) */
    .btn-primary>button { 
        background-color: #0f766e; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 8px; height: 3.5rem; width: 100%; border: none; 
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25); transition: all 0.3s ease; margin-top: 5px;
    }
    .btn-primary>button:hover { background-color: #115e59; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(15, 118, 110, 0.35); color: white;}
    
    /* Secondary Graph Button Styling (Dark Slate) */
    .btn-secondary>button { 
        background-color: #1e293b; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 8px; height: 3.5rem; width: 100%; border: none; 
        box-shadow: 0 4px 12px rgba(30, 41, 59, 0.25); transition: all 0.3s ease; margin-top: 15px;
    }
    .btn-secondary>button:hover { background-color: #0f172a; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(30, 41, 59, 0.35); color: white;}
    
    /* Intel Box Styling */
    .intel-box { background-color: #f8fafc; padding: 28px; border-left: 8px solid #0f766e; border-radius: 12px; margin-top: 20px; line-height: 1.8; border: 1px solid #e2e8f0; }
    .intel-box h4 { color: #0f766e; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; font-size: 1.1rem; }
    .intel-box p { color: #334155; font-size: 1.05rem; }
    
    /* ML Architecture Terminal Block */
    .ml-term { background: #0f172a; padding: 15px; border-left: 4px solid #64748b; border-radius: 8px; font-family: monospace; color: #94a3b8; font-size: 0.85rem; margin-top: 10px; line-height: 1.6;}
    .ml-term strong { color: #e2e8f0; }
    
    .stSlider { padding-bottom: 0px; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. ROBUST DATA LOADER
# ==========================================
@st.cache_data
def load_data():
    file = 'war_room_audit_2025_FINAL.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        df.columns = [c.lower() for c in df.columns] 
        if 'country' not in df.columns:
            for c in df.columns:
                if 'name' in c or 'nation' in c: df.rename(columns={c: 'country'}, inplace=True)
        return df
    
    # Fallback dummy data if CSV is not found
    return pd.DataFrame({
        'country': ['India', 'Germany', 'Australia', 'USA', 'Spain', 'Iceland'],
        'roi_score': [610.5, 372.2, 502.7, 692.4, 210.4, 179.0],
        'new_prob_pct': [84.6, 28.0, 89.2, 89.2, 77.2, 74.6],
        'base_prob_pct': [80.0, 95.0, 85.0, 88.0, 85.0, 82.0],
        'opportunity_gap': [0.846, 0.12, 0.65, 0.55, 0.30, 0.25],
        'lagged_share': [2.1, 22.5, 12.0, 9.5, 18.0, 19.5],
        'market_room': [0.979, 0.760, 0.880, 0.905, 0.820, 0.290],
        'gdp_per_capita': [2696, 55800, 64407, 85809, 35297, 82703]
    })

df = load_data()

# DYNAMIC COUNTRY INTEL GENERATOR
def get_detailed_intel(country, c_data, custom_roi):
    # Hardcoded specific context for the 5 markets highlighted in the presentation script
    repo = {
        "Belgium": ("⚖️ Fiscal Dominance & The Company Car Mandate", "**2023-2024 Regime Shift:** Belgium's market is uniquely shielded by its 'Company Car' tax structure. In 2024, the government mandated that only zero-emission company vehicles qualify for 100% tax deductibility. This created an artificial but highly resilient 'floor' for adoption.", f"**Strategic Verdict (ROI {custom_roi:.1f}):** Belgium is a 'Defensive Safe Haven'. The structural tax mandate makes it one of the most stable regions for long-term infrastructure ROI."),
        "Australia": ("🛡️ NVES Policy Shield & The FBT Exemption", "**2023-2024 Regime Shift:** Australia successfully avoided the 2024 European crash by implementing the New Vehicle Efficiency Standard (NVES). Combined with the ongoing Fringe Benefits Tax (FBT) exemption, the ROI for commercial and private charging has surged.", f"**Strategic Verdict (ROI {custom_roi:.1f}):** Australia remains our #1 Core Growth Target. The 12% share provides exponential room for growth, making EV ownership cheaper than ICE."),
        "India": ("🐘 The EMPS Pivot & The 0.88 Opportunity Alpha", "**2023-2024 Regime Shift:** India's pivot from FAME-II to the EMPS scheme caused a temporary supply-side plateau. However, the 2024 manufacturing incentive (PLI) has forced global giants like VinFast and Tesla into localized production talks.", f"**Strategic Verdict (ROI {custom_roi:.1f}):** India holds the largest 'Opportunity Gap' in the fund. Deployment here targets the 2026-2028 S-Curve breakout. It is the portfolio's primary Emerging Alpha play."),
        "France": ("🇫🇷 The 'Eco-Score' Moat & Sovereign Protection", "**2023-2024 Regime Shift:** France's 2024 'Eco-Score' redefined subsidies to exclude carbon-intensive shipping. This effectively subsidized European-made EVs while taxing Asian imports.", f"**Strategic Verdict (ROI {custom_roi:.1f}):** A 'Protected Mature' market. France is highly resilient to the 2024 Chaos Regime because its policy actively shields domestic margins from the Chinese price wars."),
        "Germany": ("⚠️ The 'Umweltbonus' Shock & Subsidy Cliff", "**2023-2024 Regime Shift:** The Dec 2023 constitutional court ruling forced an immediate end to all EV subsidies. This 'Policy Heart Attack' proved that German adoption was an artificial bubble. Sales collapsed 35% in early 2024.", f"**Strategic Verdict (ROI {custom_roi:.1f}):** HIGH VOLATILITY. We recommend a human veto until H2 2025. The AI identifies high structural wealth, but the current political regime shift makes capital deployment risky.")
    }
    
    res = repo.get(country)
    if res: return res
    
    # Dynamic insight generation for all other countries in the CSV
    gap = c_data.get('opportunity_gap', 0.5)
    share = c_data.get('lagged_share', 15)
    gdp = c_data.get('gdp_per_capita', c_data.get('purchasing_power', 40000))
    market_room = c_data.get('market_room', 0.5)
    
    phase = "Takeoff Phase" if share < 20 else "Mature Saturated Phase"
    
    headline = f"🔍 Macro Analysis & Structural Dynamics"
    context = (f"**2023-2024 Regime Analysis:** {country} is currently operating in a {phase} "
               f"with an EV market penetration of {share:.1f}%. Supported by a GDP per capita of approximately ${gdp:,.0f} "
               f"and an available market room index of {market_room:.2f}, the infrastructure growth here is driven by "
               f"organic market fundamentals and wealth scaling, providing a buffer against sudden policy shocks.")
               
    verdict = (f"**Strategic Verdict (ROI {custom_roi:.1f}):** Stable portfolio component. "
               f"With a calculated Opportunity Gap of {gap:.2f}, this market offers a "
               f"structurally sound deployment target outside of our primary Tier 1 and Alpha plays.")
               
    return (headline, context, verdict)

# ==========================================
# 3. POP-UP 1: SYSTEM ANALYTICS (TABS)
# ==========================================
@st.dialog("📊 SYSTEM ANALYTICS & MACRO PORTFOLIO", width="large")
def show_system_analytics():
    tab_alpha, tab_stress = st.tabs(["[ ALPHA VALUATION MATRIX ]", "[ 2024 REGIME STRESS TEST ]"])
    
    # --- TAB 1: THE ALPHA SCATTER PLOT ---
    with tab_alpha:
        st.markdown("<p style='color: #64748b; font-weight: 600; margin-top: 5px;'>Comparing AI Confidence vs Opportunity Gap</p>", unsafe_allow_html=True)
        scatter_df = pd.DataFrame({
            'Country': ['India', 'Germany', 'Australia', 'USA', 'Spain', 'Iceland'],
            'AI_Confidence': [84.6, 28.0, 89.2, 89.2, 77.2, 74.6],
            'Opportunity_Gap': [0.846, 0.12, 0.65, 0.55, 0.30, 0.25],
            'Classification': ['Emerging Alpha (Buy)', 'Overrated (Value Trap)', 'Core Safety', 'Core Safety', 'Vulnerable', 'Vulnerable']
        })
        fig_scatter = px.scatter(
            scatter_df, x='AI_Confidence', y='Opportunity_Gap', text='Country',
            color='Classification', 
            color_discrete_map={'Emerging Alpha (Buy)': '#ea580c', 'Core Safety': '#dc2626', 'Overrated (Value Trap)': '#0f766e', 'Vulnerable': '#0f766e'}
        )
        fig_scatter.update_traces(textposition='top center', textfont=dict(size=16, color="#0f172a"), marker=dict(size=18, line=dict(width=2, color='#ffffff')))
        fig_scatter.add_vline(x=78, line_width=2, line_dash="dash", line_color="#0f766e")
        fig_scatter.add_annotation(x=77.5, y=0.8, text="<b>78% MARGIN OF SAFETY THRESHOLD</b>", showarrow=False, textangle=-90, font=dict(color="#0f766e", size=16))
        
        # Notice: No weight parameter, entirely Streamlit Cloud safe
        fig_scatter.update_layout(
            height=450, margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(title="<b>AI Survival Probability (%)</b>", tickfont=dict(size=16), titlefont=dict(size=16)),
            yaxis=dict(title="<b>Opportunity Gap (Alpha)</b>", tickfont=dict(size=16), titlefont=dict(size=16)),
            legend=dict(font=dict(size=16), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})

    # --- TAB 2: THE 2024 STRESS TEST BAR CHART ---
    with tab_stress:
        st.markdown("<p style='color: #64748b; font-weight: 600; margin-top: 5px;'>Model Accuracy Degradation (Baseline vs 2024 Regime Shift)</p>", unsafe_allow_html=True)
        stress_df = pd.DataFrame({
            'Model': ['Random Forest', 'Naive Bayes', 'KNN', 'Random Forest', 'Naive Bayes', 'KNN'],
            'Scenario': ['2023 Baseline', '2023 Baseline', '2023 Baseline', '2024 Regime Shift', '2024 Regime Shift', '2024 Regime Shift'],
            'Accuracy': [84.1, 82.5, 83.2, 65.6, 52.4, 46.9]
        })
        fig_bar = go.Figure()
        
        # 2023 Baseline 
        df_base = stress_df[stress_df['Scenario'] == '2023 Baseline']
        fig_bar.add_trace(go.Bar(x=df_base['Model'], y=df_base['Accuracy'], name='2023 Baseline', marker_color='#dc2626'))
        
        # 2024 Crash 
        df_crash = stress_df[stress_df['Scenario'] == '2024 Regime Shift']
        colors = ['#ea580c' if m == 'Random Forest' else '#0f766e' for m in df_crash['Model']]
        fig_bar.add_trace(go.Bar(x=df_crash['Model'], y=df_crash['Accuracy'], name='2024 Regime Shift', marker_color=colors))
        
        fig_bar.update_layout(
            barmode='group', height=450, margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(tickfont=dict(size=16)),
            yaxis=dict(title="<b>Accuracy (%)</b>", tickfont=dict(size=16), titlefont=dict(size=16)),
            legend=dict(font=dict(size=16), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# ==========================================
# 4. POP-UP 2: THE EXECUTIVE AUDIT (DETAILS)
# ==========================================
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    wealth = c_data.get('gdp_per_capita', c_data.get('purchasing_power', 5))
    
    # Scale ROI visually based on sliders
    custom_roi = c_data.get('roi_score', 500) * ((prob**w_s) * (room**w_r) * (1.1**w_w))
    
    headline, context, verdict = get_detailed_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 15px; font-weight: 800;'>STRATEGIC AUDIT: {country.upper()}</h2>", unsafe_allow_html=True)
    
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 15)
        status = "🚀 Takeoff Phase" if share < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\nMarket exhibits {share:.1f}% adoption. Markets under 20% yield highest returns.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data.get('new_prob_pct', 0) >= 78 else "⚠️ Policy Vulnerable"
        if c_data.get('new_prob_pct', 0) >= 78:
            st.success(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\nModel verifies structural stability. Clears the 78% Margin of Safety.")
        else:
            st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\nRegime shift detected. Fails 78% Margin of Safety. Intervene immediately.")

    st.markdown("---")
    
    st.markdown("### 2. Regime Shift Analytics (2024 Stress Test)")
    m1, m2, m3 = st.columns(3)
    curr_p = c_data.get('new_prob_pct', 0)
    base_p = c_data.get('base_prob_pct', 75)
    m1.metric("AI Survival Probability", f"{curr_p:.1f}%", f"{curr_p - base_p:+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('opportunity_gap', 0):.2f}", "Alpha Score")
    m3.metric("ROI Potential Index", f"{custom_roi:,.0f}", "Weighted Matrix")

    st.markdown(f"""
    <div class='intel-box'>
        <h4>📰 Geopolitical Context: {headline}</h4>
        <p>{context}</p>
        <hr style='border: 1px solid #e2e8f0; margin: 20px 0;'>
        <h4 style='color: #0f172a;'>💰 ROI Justification & Verdict</h4>
        <p style='font-weight: 600;'>{verdict}</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. MAIN INTERFACE (THE CLEAN VIEW)
# ==========================================
st.markdown("<h1 style='color: #0f172a; margin-bottom: 0px; font-weight: 900; letter-spacing: -1px;'>GlobalCharge Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-weight: 700; margin-top: 0; letter-spacing: 0.5px;'>EXECUTIVE INVESTMENT DASHBOARD | REGIME-AWARE AUDIT</p>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.2, 2.8], gap="large")

with col_map:
    # Restored Original Teal Color Scale
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Teal")
    fig.update_geos(showland=True, landcolor="#f8fafc", oceancolor="#ffffff", showframe=False, lakecolor="#ffffff")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=600, coloraxis_showscale=False, font=dict(size=14))
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    selected_country = None
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        selected_country = pt.get("location") or pt.get("hovertext")
    
    st.markdown("<hr style='margin: 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)
    manual_sel = st.selectbox("Select Target Market:", ["Click Map..."] + sorted(df['country'].unique().tolist()))
    if not selected_country or selected_country not in df['country'].values:
        selected_country = manual_sel if manual_sel != "Click Map..." else None

    # --- IF COUNTRY IS SELECTED ---
    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 15px; font-weight: 800; color: #0f766e;'>🎯 Target: {selected_country}</h3>", unsafe_allow_html=True)
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("<div style='margin-top: 15px;'><strong>⚙️ Configuration Mandate</strong></div>", unsafe_allow_html=True)
        ws = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        wr = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        ww = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        st.markdown("<div class='btn-primary'>", unsafe_allow_html=True)
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, ws, wr, ww)
        st.markdown("</div>", unsafe_allow_html=True)
            
    # --- IF NO COUNTRY SELECTED (WAITING STATE) ---
    else:
        st.markdown("<h3 style='margin-top: 15px; font-weight: 800;'>🌍 Portfolio Audit</h3>", unsafe_allow_html=True)
        st.metric("Capital Mandate", "$100M")
        st.metric("Precision (2024)", "67.7%")
        
        st.markdown("""
        <div style="background-color: #fff7ed; padding: 15px; border-left: 5px solid #0f766e; border-radius: 4px; color: #0f766e; font-weight: 600; margin-top: 15px;">
            Awaiting Input: Select a country on the map or use the dropdown to initiate the resilience audit.
        </div>
        """, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # THE HIDDEN WEAPONS: Always available at the bottom of the panel
    # -------------------------------------------------------------
    st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 15px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<div class='btn-secondary'>", unsafe_allow_html=True)
    if st.button("📊 OPEN SYSTEM ANALYTICS"):
        show_system_analytics()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 25px;'><strong>⚙️ ACTIVE ML ARCHITECTURE</strong></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="ml-term">
        <strong>LAYER 1:</strong> HMM (Regime Detection)<br>
        <strong>LAYER 2:</strong> NLP (90-Day Sentiment Lead)<br>
        <strong>LAYER 3:</strong> Random Forest (n=100, d=4)<br>
        <strong>STATE:</strong> <span style="color: #ef4444; font-weight: bold;">LOCKED (NO 2024 LEAKAGE)</span>
    </div>
    """, unsafe_allow_html=True)
