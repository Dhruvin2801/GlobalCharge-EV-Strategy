import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & BARE-METAL THEME ---
st.set_page_config(page_title="SYS.GLOBALCHARGE.AUDIT", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS: Tech-Brutalism, Monospace, Sharp Borders, +2pt Sizing
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&display=swap');
    
    /* Bare-Metal Brutalist Background */
    .stApp { background-color: #050505; color: #e5e5e5; font-family: 'JetBrains Mono', 'Courier New', monospace; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Terminal Pitch Block */
    .quant-pitch {
        border-left: 8px solid #ff0000; 
        background-color: #111;
        padding: 15px; margin-bottom: 25px;
        color: #a1a1aa; font-size: 1.1rem; 
        text-transform: uppercase; letter-spacing: 1px;
    }
    .quant-pitch strong { color: #ffffff; }
    
    /* Brutalist Metrics (+2pt Sizing Enforced) */
    [data-testid="stMetricValue"] { font-size: calc(2.2rem + 2pt) !important; color: #ff0000; font-weight: 800; letter-spacing: -2px; }
    [data-testid="stMetricLabel"] { font-size: calc(0.9rem + 2pt) !important; color: #71717a; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Brutalist Button (Harsh Red) */
    .stButton>button { 
        background-color: transparent; color: #ff0000; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;
        border-radius: 0px; height: 3.5rem; width: 100%; border: 3px solid #ff0000; 
        transition: all 0.1s ease; margin-top: 15px; box-shadow: 4px 4px 0px #ff0000;
    }
    .stButton>button:hover { background-color: #ff0000; color: #000; transform: translate(2px, 2px); box-shadow: 2px 2px 0px #ff0000; }
    
    /* Intel Box (Exposed Structure) */
    .intel-box { background-color: transparent; padding: 25px; border: 2px solid #333; border-left: 8px solid #ff0000; margin-top: 20px; }
    .intel-box h4 { color: #ff0000; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; font-size: 1.2rem; letter-spacing: 1px; }
    .intel-box p { color: #d4d4d8; font-size: 1.05rem; }
    
    /* Brutalist Orange Warnings (Replacing standard reds for negative alerts) */
    .stAlert { background-color: #1a0f00 !important; color: #ff8c00 !important; border: 2px solid #ff8c00 !important; border-radius: 0px !important; }
    
    /* Slider Overrides */
    .stSlider { padding-bottom: 0px; margin-bottom: -10px; }
    hr { border-color: #333; }
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
    st.error("SYS.ERR: 'war_room_audit_2025.csv' NOT_FOUND.")
    st.stop()

# --- 3. INTEL REPOSITORY ---
def get_detailed_intel(country, c_data, custom_roi):
    repo = {
        "Belgium": ("FISCAL DOMINANCE // COMPANY CAR MANDATE", "2024 REGIME SHIFT: Market uniquely shielded by corporate tax structure. Zero-emission mandate creates artificial but resilient floor, bypassing consumer interest rate shocks.", f"VERDICT: Defensive Safe Haven. ROI {custom_roi:.1f}."),
        "Australia": ("NVES SHIELD // FBT EXEMPTION", "2024 REGIME SHIFT: Successfully bypassed European crash via NVES implementation. FBT exemption surging ROI for charging networks.", f"VERDICT: Core Growth Target. ROI {custom_roi:.1f}."),
        "India": ("EMPS PIVOT // 0.88 ALPHA", "2024 REGIME SHIFT: FAME-II transition caused supply plateau. PLI incentives forcing localized production. System identifies strategic accumulation zone.", f"VERDICT: Strategic Buy on the Dip. ROI {custom_roi:.1f}."),
        "France": ("ECO-SCORE MOAT // SOVEREIGN PROTECTION", "2024 REGIME SHIFT: Carbon-indexed subsidies effectively block Asian imports. Domestic ROI stabilized against global price wars.", f"VERDICT: Protected Mature. ROI {custom_roi:.1f}."),
        "Germany": ("UMWELTBONUS SHOCK // SUBSIDY CLIFF", "2024 REGIME SHIFT: Constitutional court mandate terminated EV subsidies. Sales collapsed 35%. Market in mean-reversion phase.", f"VERDICT: HIGH VOLATILITY. Human veto recommended. ROI {custom_roi:.1f}.")
    }
    res = repo.get(country)
    if res: return res
    gap = c_data.get('opportunity_gap', 0.5)
    return (f"STRUCTURAL AUDIT: {country.upper()}", f"DYNAMICS: GDP-driven S-Curve shielded from policy volatility by organic wealth scaling.", f"VERDICT: Stable target. Gap: {gap:.2f}")

# --- 4. TERMINAL MODAL ---
@st.dialog("SYS.AUDIT.REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    wealth = c_data.get('purchasing_power', 5)
    custom_roi = ((prob**w_s) * (room**w_r) * (wealth**w_w)) / (1.5) * 100
    headline, context, verdict = get_detailed_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #ff0000; margin-bottom: 5px; font-family: monospace;'>TARGET_LOCK: {country.upper()}</h2>", unsafe_allow_html=True)
    
    st.markdown("### > STAGE_CLASSIFICATION")
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 15)
        st.info(f"**STATUS: {'TAKEOFF' if share < 20 else 'SATURATED'}**\n\nAdoption: {share:.1f}%")
    with c2:
        resilience = c_data.get('new_prob_pct', 0) >= 78
        if resilience:
            st.info("**RISK: TOLERABLE**\n\nModel identifies structural stability.")
        else:
            st.warning("**RISK: VULNERABLE**\n\nRegime shift detected. Exercise caution.")

    st.markdown("### > SHIFT_ANALYTICS (23->24)")
    m1, m2, m3 = st.columns(3)
    curr_p = c_data.get('new_prob_pct', 0)
    base_p = c_data.get('base_prob_pct', 75)
    m1.metric("CONFIDENCE", f"{curr_p:.1f}%", f"{curr_p - base_p:+.1f}%")
    m2.metric("ALPHA_GAP", f"{c_data.get('opportunity_gap', 0):.2f}")
    m3.metric("ROI_INDEX", f"{custom_roi:.1f}")

    st.markdown(f"""
    <div class='intel-box'>
        <h4>> {headline}</h4>
        <p>{context}</p>
        <p style='color: #ff0000; font-weight: bold; margin-top: 15px;'>> {verdict}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN TERMINAL UI ---
st.markdown("<h1 style='color: #fff; margin-bottom: 0px; letter-spacing: -2px;'>SYS.GLOBALCHARGE.ALLOCATION</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='quant-pitch'>
    <strong>MANDATE:</strong> Deploy $100M into global EV infrastructure.<br>
    <strong>EDGE:</strong> Regime-aware ML system executing strict downside protection.<br>
    <strong>OBJECTIVE:</strong> Identify structural policy breaks. Avoid artificial bubbles.
</div>
""", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.2, 2.8], gap="large")

with col_map:
    # STRICT MAP THEME: Red targets (replacing blue), transparent background.
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Reds")
    fig.update_geos(
        showland=True, landcolor="#0f0f0f", oceancolor="#050505", 
        showframe=False, lakecolor="#050505", bgcolor='rgba(0,0,0,0)'
    )
    # +2pt Font Sizing enforced in layout
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, height=600, coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="JetBrains Mono, monospace", color="#e5e5e5", size=16) 
    )
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    selected_country = None
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        selected_country = pt.get("location") or pt.get("hovertext")
    
    manual_sel = st.selectbox("INPUT_TARGET:", ["AWAITING_INPUT..."] + sorted(df['country'].unique().tolist()))
    if not selected_country or selected_country not in df['country'].values:
        selected_country = manual_sel if manual_sel != "AWAITING_INPUT..." else None

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 10px; color: #ff0000;'>> TGT: {selected_country.upper()}</h3>", unsafe_allow_html=True)
        st.metric("ROI_SCORE", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("CONFIDENCE", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("<br>**> OVERRIDE_PARAMETERS**", unsafe_allow_html=True)
        ws = st.slider("RESILIENCE", 0.0, 2.0, 1.0, step=0.1)
        wr = st.slider("CAPACITY", 0.0, 2.0, 1.0, step=0.1)
        ww = st.slider("WEALTH", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("EXECUTE AUDIT"):
            show_final_report(selected_country, ws, wr, ww)
    else:
        st.markdown("<h3 style='margin-top: 10px; color: #71717a;'>> SYSTEM_IDLE</h3>", unsafe_allow_html=True)
        st.metric("CAPITAL_MANDATE", "$100M")
        st.metric("SYS_PRECISION", "67.7%")
        st.markdown("<p style='color: #ff8c00; font-family: monospace;'>WARNING: Select target to initiate resilience audit.</p>", unsafe_allow_html=True)
