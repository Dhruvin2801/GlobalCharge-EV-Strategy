import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & BASE THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

# Base Theme (Dark Mode Base)
st.markdown("""
    <style>
    .stApp { background-color: #0A0B10; color: #E2E8F0; font-family: 'Inter', monospace; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Main Page Metrics */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #00FF41; font-weight: 800; letter-spacing: 0.05rem; text-shadow: 0 0 8px rgba(0,255,65,0.4); }
    [data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #94A3B8; font-weight: 700; text-transform: uppercase; }
    
    /* Audit Button Styling (Neon Green) */
    .stButton>button { 
        background-color: transparent; color: #00FF41; font-weight: 800; text-transform: uppercase;
        border-radius: 4px; height: 3.5rem; width: 100%; border: 2px solid #00FF41; 
        box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); transition: all 0.3s ease; margin-top: 15px; letter-spacing: 2px;
    }
    .stButton>button:hover { background-color: rgba(0, 255, 65, 0.1); transform: translateY(-2px); box-shadow: 0 0 20px rgba(0, 255, 65, 0.6); color: #FFFFFF;}
    
    .stSlider { padding-bottom: 0px; margin-bottom: -10px; }
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

# --- 3. GEOPOLITICAL INTELLIGENCE REPOSITORY ---
def get_detailed_intel(country, c_data, custom_roi):
    repo = {
        "Belgium": (
            "THE 'COMPANY CAR' MANDATE",
            "In 2024, Belgium mandated that only zero-emission corporate vehicles qualify for 100% tax deductibility. This created a highly resilient floor for adoption, bypassing the consumer interest rate anxieties that crashed Germany. The market is artificially shielded by corporate tax code.",
            f"STRATEGIC VERDICT (ROI {custom_roi:.1f}): A 'Defensive Safe Haven'. Structural tax mandates make corporate fleet turnover mandatory, guaranteeing long-term infrastructure utilization regardless of consumer sentiment."
        ),
        "Australia": (
            "NVES POLICY SHIELD & FBT EXEMPTION",
            "Australia avoided the 2024 European crash by passing the New Vehicle Efficiency Standard (NVES). Combined with ongoing Fringe Benefits Tax (FBT) exemptions, the ROI for commercial charging has surged, shifting growth from 'voluntary' to 'regulatory necessity'.",
            f"STRATEGIC VERDICT (ROI {custom_roi:.1f}): Core Growth Target (#1). 12% share provides exponential 'takeoff' room. The structural tax advantage mathematically makes EV ownership cheaper than ICE for the middle class."
        ),
        "India": (
            "THE EMPS PIVOT & PLI MANUFACTURING",
            "India's pivot from FAME-II to EMPS caused a temporary 2024 plateau. However, the new 15% import tax threshold for global OEMs committing $500M+ to local factories has forced a massive supply chain race. The AI flags this as a deep-value anomaly.",
            f"STRATEGIC VERDICT (ROI {custom_roi:.1f}): The 'Sleeping Giant'. Holds the highest Opportunity Gap (0.88). Deployment targets the 2026 S-Curve breakout. Primary Emerging Alpha play."
        ),
        "France": (
            "THE 'ECO-SCORE' MOAT",
            "France redefined subsidies in 2024 to exclude carbon-intensive shipping. This effectively subsidized European EVs while taxing Asian imports. This sovereign protectionism stabilized domestic ROI against global price volatility.",
            f"STRATEGIC VERDICT (ROI {custom_roi:.1f}): A 'Protected Mature' market. Highly resilient to the 2024 Chaos Regime because its policy actively shields domestic margins."
        ),
        "Germany": (
            "THE 'UMWELTBONUS' SHOCK",
            "The Dec 2023 constitutional court ruling forced an immediate end to all EV subsidies. This 'Policy Heart Attack' proved 2023 adoption was an artificial bubble. Sales collapsed 35% as the market entered severe mean-reversion.",
            f"STRATEGIC VERDICT (ROI {custom_roi:.1f}): HIGH VOLATILITY. Human veto recommended until H2 2025. High structural wealth exists, but political regime shifts make capital deployment overly risky."
        )
    }
    
    res = repo.get(country)
    if res: return res
    
    gap = c_data.get('opportunity_gap', 0.5)
    return (f"STRUCTURAL RESILIENCE: {country.upper()}", 
            f"Benefiting from the 'Global South Supply Pivot' as Chinese OEMs redirect inventory away from high-tariff zones (EU/US). Adoption is currently following a GDP-driven S-Curve, shielded from European political volatility.",
            f"STRATEGIC VERDICT (ROI {custom_roi:.1f}): Stable secondary deployment target. Growth is driven by long-term infrastructure expansion rather than fickle state aid. (Opportunity Gap: {gap:.2f})")

# --- 4. CYBERPUNK AUDIT DIALOG ---
@st.dialog("SYSTEM OVERRIDE: EXECUTIVE AUDIT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    wealth = c_data.get('purchasing_power', 5)
    custom_roi = ((prob**w_s) * (room**w_r) * (wealth**w_w)) / (1.5) * 100
    
    headline, context, verdict = get_detailed_intel(country, c_data, custom_roi)
    
    share = c_data.get('lagged_share', 15)
    stage_status = "TAKEOFF PHASE" if share < 20 else "MATURE / SATURATED"
    resilience_status = "HIGHLY RESILIENT" if c_data.get('new_prob_pct', 0) >= 78 else "POLICY VULNERABLE"
    res_color = "#00FF41" if resilience_status == "HIGHLY RESILIENT" else "#FF003C" # Red for vulnerable
    
    # Custom HTML/CSS for the Pop-up to force the Cyberpunk Theme regardless of Streamlit's base theme
    st.markdown(f"""
        <style>
        .cyber-container {{ background-color: #050505; color: #E2E8F0; font-family: 'Courier New', monospace; padding: 20px; border: 1px solid #333; }}
        .cyber-header {{ color: #00FF41; font-size: 2rem; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; border-bottom: 2px solid #00FF41; padding-bottom: 10px; margin-bottom: 20px; text-shadow: 0 0 10px rgba(0,255,65,0.5); }}
        
        /* Classification Grid */
        .class-grid {{ display: flex; gap: 20px; margin-bottom: 25px; }}
        .class-box {{ flex: 1; background-color: #111; border-left: 4px solid; padding: 15px; }}
        .box-1 {{ border-color: #00FF41; }}
        .box-2 {{ border-color: {res_color}; }}
        .class-title {{ color: #888; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px; }}
        .class-value {{ font-size: 1.4rem; font-weight: bold; margin-bottom: 8px; color: #FFF; }}
        .class-desc {{ font-size: 0.85rem; color: #AAA; }}
        
        /* Metrics Grid */
        .metric-grid {{ display: flex; gap: 15px; margin-bottom: 25px; background: #0A0A0A; padding: 15px; border: 1px dashed #333; }}
        .m-box {{ flex: 1; text-align: center; }}
        .m-val {{ color: #00FF41; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 8px rgba(0,255,65,0.3); }}
        .m-lbl {{ color: #888; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }}
        
        /* Intel Box */
        .cyber-intel {{ background: linear-gradient(180deg, #111 0%, #050505 100%); border: 1px solid #222; border-top: 3px solid #00FF41; padding: 25px; }}
        .intel-head {{ color: #00FF41; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px; letter-spacing: 1px; }}
        .intel-body {{ color: #CCC; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px; }}
        .intel-verdict {{ background: rgba(0, 255, 65, 0.05); padding: 15px; border-left: 2px solid #00FF41; color: #FFF; font-weight: bold; font-size: 0.95rem; }}
        </style>
        
        <div class="cyber-container">
            <div class="cyber-header">TARGET LOG: {country.upper()}</div>
            
            <div class="class-grid">
                <div class="class-box box-1">
                    <div class="class-title">Market Stage [Class 1]</div>
                    <div class="class-value">{stage_status}</div>
                    <div class="class-desc">Current Adoption: {share:.1f}%. Capital deployment into early-stage markets yields highest structural returns.</div>
                </div>
                <div class="class-box box-2">
                    <div class="class-title">AI Risk Profile [Class 2]</div>
                    <div class="class-value" style="color: {res_color}">{resilience_status}</div>
                    <div class="class-desc">System indicates structural stability during the 2024 'Chaos Regime' shifts.</div>
                </div>
            </div>
            
            <div class="metric-grid">
                <div class="m-box">
                    <div class="m-val">{c_data.get('new_prob_pct', 0):.1f}%</div>
                    <div class="m-lbl">AI Confidence</div>
                </div>
                <div class="m-box">
                    <div class="m-val">{c_data.get('opportunity_gap', 0):.2f}</div>
                    <div class="m-lbl">Alpha Gap</div>
                </div>
                <div class="m-box">
                    <div class="m-val">{custom_roi:.1f}</div>
                    <div class="m-lbl">ROI Index</div>
                </div>
            </div>
            
            <div class="cyber-intel">
                <div class="intel-head">>> INTELLIGENCE BRIEF: {headline}</div>
                <div class="intel-body">{context}</div>
                <div class="intel-verdict">>> {verdict}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='color: #00FF41; margin-bottom: 0px; text-shadow: 0 0 15px rgba(0,255,65,0.5);'>GlobalCharge / Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888; font-family: monospace; letter-spacing: 2px; margin-top: 0;'>SYSTEM.STATUS: ONLINE // REGIME-AWARE AUDIT ACTIVE</p>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.2, 2.8], gap="medium")

with col_map:
    # Cyberpunk Map: Dark background, glowing green countries
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", 
                        color_continuous_scale=[(0, "#050505"), (1, "#00FF41")]) # Black to Neon Green
    fig.update_geos(showland=True, landcolor="#111111", oceancolor="#050505", showframe=False, coastlinecolor="#333333")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550, coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    selected_country = None
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        selected_country = pt.get("location") or pt.get("hovertext")
    
    st.markdown("<hr style='border-color: #333; margin: 0;'>", unsafe_allow_html=True)
    manual_sel = st.selectbox("QUERY.DATABASE:", ["SELECT_TARGET..."] + sorted(df['country'].unique().tolist()))
    if not selected_country or selected_country not in df['country'].values:
        selected_country = manual_sel if manual_sel != "SELECT_TARGET..." else None

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 15px; color: #FFF;'>TARGET: {selected_country.upper()}</h3>", unsafe_allow_html=True)
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("<br><span style='color: #888; font-family: monospace;'>// CONFIGURATION PROTOCOL</span>", unsafe_allow_html=True)
        ws = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        wr = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        ww = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("EXECUTE AUDIT PROTOCOL"):
            show_final_report(selected_country, ws, wr, ww)
    else:
        st.markdown("<h3 style='margin-top: 15px; color: #FFF;'>PORTFOLIO LOG</h3>", unsafe_allow_html=True)
        st.metric("Capital Mandate", "$100M")
        st.metric("Precision (2024)", "67.7%")
        st.markdown("<span style='color: #888; font-family: monospace;'>Awaiting target selection...</span>", unsafe_allow_html=True)
