import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & HIGH-CONTRAST THEME ---
st.set_page_config(page_title="GlobalCharge | Executive Audit", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS: Maximum Visibility "Executive Print" Theme
st.markdown("""
    <style>
    /* Clean, High-Contrast Light Background */
    .stApp { background-color: #ffffff; color: #0f172a; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1.5rem; padding-bottom: 0rem; max-width: 95%; }
    
    /* Executive Pitch Block */
    .quant-pitch {
        border-left: 5px solid #dc2626; 
        background-color: #f8fafc;
        padding: 18px 24px; margin-bottom: 30px;
        color: #475569; font-size: 1.15rem; font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .quant-pitch strong { color: #0f172a; font-weight: 700; }
    
    /* High-Visibility Metrics (+2pt Scaling Applied) */
    [data-testid="stMetricValue"] { font-size: calc(2.0rem + 2pt) !important; color: #dc2626; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: calc(1.0rem + 2pt) !important; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Executive Action Button (Primary Red) */
    .stButton>button { 
        background-color: #dc2626; color: white; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
        border-radius: 4px; height: 3.5rem; width: 100%; border: none; 
        box-shadow: 0 4px 6px -1px rgba(220, 38, 38, 0.2); transition: all 0.2s; margin-top: 15px;
    }
    .stButton>button:hover { background-color: #b91c1c; box-shadow: 0 10px 15px -3px rgba(220, 38, 38, 0.3); color: white; }
    
    /* Intel Box (Crisp separation) */
    .intel-box { background-color: #ffffff; padding: 30px; border: 1px solid #e2e8f0; border-top: 5px solid #dc2626; border-radius: 6px; margin-top: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    .intel-box h4 { color: #0f172a; font-weight: 800; margin-bottom: 15px; text-transform: uppercase; font-size: 1.25rem; }
    .intel-box p { color: #334155; font-size: 1.1rem; line-height: 1.7; }
    
    /* Warning/Regime Alerts (Strict Orange) */
    .stAlert { background-color: #fff7ed !important; color: #c2410c !important; border: 1px solid #fdba74 !important; }
    
    /* Structural Cleanups */
    .stSlider { padding-bottom: 0px; margin-bottom: -10px; }
    hr { border-color: #e2e8f0; margin: 2rem 0; }
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
    st.error("CRITICAL ERROR: 'war_room_audit_2025.csv' missing from local directory.")
    st.stop()

# --- 3. INTEL REPOSITORY ---
def get_detailed_intel(country, c_data, custom_roi):
    repo = {
        "Belgium": ("Fiscal Dominance & Company Car Mandate", "2024 Regime Shift: The market is uniquely shielded by its corporate tax structure. The zero-emission mandate creates an artificial but highly resilient floor, entirely bypassing consumer interest rate shocks.", f"Verdict: Defensive Safe Haven. ROI Potential {custom_roi:.1f}."),
        "Australia": ("NVES Policy Shield & FBT Exemption", "2024 Regime Shift: Australia successfully bypassed the European crash via prompt NVES implementation. The FBT exemption is surging ROI for commercial charging networks.", f"Verdict: Core Growth Target. ROI Potential {custom_roi:.1f}."),
        "India": ("EMPS Pivot & 0.88 Opportunity Alpha", "2024 Regime Shift: The FAME-II transition caused a temporary supply plateau, but PLI manufacturing incentives are forcing localized production. The system identifies a strategic accumulation zone.", f"Verdict: Strategic Buy on the Dip. ROI Potential {custom_roi:.1f}."),
        "France": ("The 'Eco-Score' Moat", "2024 Regime Shift: Carbon-indexed subsidies effectively block carbon-heavy imports. Domestic ROI is stabilized by active sovereign protectionism against global price wars.", f"Verdict: Protected Mature Market. ROI Potential {custom_roi:.1f}."),
        "Germany": ("The 'Umweltbonus' Shock", "2024 Regime Shift: The constitutional court mandate abruptly terminated EV subsidies, collapsing sales by 35%. The market has entered a severe mean-reversion phase.", f"Verdict: HIGH VOLATILITY. Human veto recommended. ROI Potential {custom_roi:.1f}.")
    }
    res = repo.get(country)
    if res: return res
    gap = c_data.get('opportunity_gap', 0.5)
    return (f"Structural Audit: {country}", f"Dynamics: A classic GDP-driven S-Curve shielded from policy volatility by organic wealth scaling and robust infrastructure planning.", f"Verdict: Stable Target. Opportunity Gap {gap:.2f}")

# --- 4. EXECUTIVE MODAL ---
@st.dialog("STRATEGIC ASSET ALLOCATION REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    wealth = c_data.get('purchasing_power', 5)
    custom_roi = ((prob**w_s) * (room**w_r) * (wealth**w_w)) / (1.5) * 100
    headline, context, verdict = get_detailed_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f172a; margin-bottom: 5px; font-weight: 800;'>TARGET MARKET: {country.upper()}</h2>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #475569; font-size: 1.1rem;'>1. MARKET CLASSIFICATION</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 15)
        st.info(f"**Market Stage:** {'Takeoff Phase' if share < 20 else 'Saturated'}\n\nCurrent Adoption: {share:.1f}%")
    with c2:
        resilience = c_data.get('new_prob_pct', 0) >= 78
        if resilience:
            st.success("**Risk Profile:** Tolerable\n\nModel verifies structural stability.")
        else:
            st.warning("**Risk Profile:** Vulnerable\n\nRegime shift detected. Exercise caution.")

    st.markdown("<h3 style='color: #475569; font-size: 1.1rem; margin-top: 20px;'>2. QUANTITATIVE METRICS (2024 REGIME)</h3>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    curr_p = c_data.get('new_prob_pct', 0)
    base_p = c_data.get('base_prob_pct', 75)
    m1.metric("Model Confidence", f"{curr_p:.1f}%", f"{curr_p - base_p:+.1f}%")
    m2.metric("Alpha Gap", f"{c_data.get('opportunity_gap', 0):.2f}")
    m3.metric("ROI Potential Index", f"{custom_roi:.1f}")

    st.markdown(f"""
    <div class='intel-box'>
        <h4 style='color: #dc2626;'>Geopolitical Context: {headline}</h4>
        <p>{context}</p>
        <hr style='margin: 15px 0;'>
        <p style='color: #0f172a; font-weight: 700; font-size: 1.15rem;'>{verdict}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN UI LAYOUT ---
st.markdown("<h1 style='color: #0f172a; margin-bottom: 0px; font-weight: 900; letter-spacing: -1px;'>GlobalCharge Intelligence Engine</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='quant-pitch'>
    <strong>MANDATE:</strong> Deploy $100M into global EV infrastructure.<br>
    <strong>EDGE:</strong> Regime-aware machine learning engine executing strict downside protection.<br>
    <strong>OBJECTIVE:</strong> Identify structural policy breaks. Avoid artificial bubbles.
</div>
""", unsafe_allow_html=True)

col_map, col_panel = st.columns([7, 3], gap="large")

with col_map:
    # High-Visibility Map Layout (Light background, Red target scale)
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Reds")
    fig.update_geos(
        showland=True, landcolor="#f1f5f9", oceancolor="#ffffff", 
        showframe=False, lakecolor="#ffffff", bordercolor="#cbd5e1"
    )
    # +2pt Font Sizing explicitly added to layout for projector clarity
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, height=600, coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Helvetica Neue, sans-serif", color="#0f172a", size=16)
    )
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    selected_country = None
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        selected_country = pt.get("location") or pt.get("hovertext")
    
    manual_sel = st.selectbox("Select Target Market:", ["Awaiting Selection..."] + sorted(df['country'].unique().tolist()))
    if not selected_country or selected_country not in df['country'].values:
        selected_country = manual_sel if manual_sel != "Awaiting Selection..." else None

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 10px; color: #0f172a; font-weight: 800;'>Target: {selected_country}</h3>", unsafe_allow_html=True)
        
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("System Confidence", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-weight: 700; color: #475569; margin-bottom: 5px;'>OVERRIDE PARAMETERS</p>", unsafe_allow_html=True)
        ws = st.slider("Resilience Weight", 0.0, 2.0, 1.0, step=0.1)
        wr = st.slider("Capacity Weight", 0.0, 2.0, 1.0, step=0.1)
        ww = st.slider("Wealth Weight", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("EXECUTE PORTFOLIO AUDIT"):
            show_final_report(selected_country, ws, wr, ww)
    else:
        st.markdown("<h3 style='margin-top: 10px; color: #64748b; font-weight: 700;'>Portfolio Overview</h3>", unsafe_allow_html=True)
        st.metric("Capital Mandate", "$100M")
        st.metric("System Precision", "67.7%")
        st.warning("Please select a target market from the map or dropdown to initiate the resilience audit.")
