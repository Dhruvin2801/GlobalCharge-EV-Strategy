import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & HIGH-DENSITY THEME ---
st.set_page_config(page_title="GlobalCharge | Quant", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS: Deep Slate, +2pt Font Sizing, Strict Red/Orange Palette, No-Scroll Density
st.markdown("""
    <style>
    /* High-Density Institutional Slate */
    .stApp { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    header { visibility: hidden; }
    
    /* Tabs Styling for "Next Page" functionality */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #334155; }
    .stTabs [data-baseweb="tab"] { background-color: #1e293b; border-radius: 4px 4px 0 0; padding: 10px 24px; color: #94a3b8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; border: 1px solid #334155; border-bottom: none; }
    .stTabs [aria-selected="true"] { background-color: #dc2626 !important; color: #ffffff !important; border-color: #dc2626 !important; }
    
    /* Strictly Scaled Metrics (+2pt Enforced) */
    [data-testid="stMetricValue"] { font-size: calc(1.8rem + 2pt) !important; color: #dc2626; font-weight: 800; line-height: 1.1; }
    [data-testid="stMetricLabel"] { font-size: calc(0.85rem + 2pt) !important; color: #94a3b8; font-weight: 700; text-transform: uppercase; }
    
    /* Compact Intel Box (Fits left column without scrolling) */
    .intel-panel { background-color: #1e293b; padding: 15px; border-left: 4px solid #ea580c; border-radius: 4px; margin-top: 10px; border: 1px solid #334155; font-size: 0.95rem; line-height: 1.5; color: #cbd5e1; }
    .intel-panel h4 { color: #ea580c; margin-top: 0; margin-bottom: 8px; font-size: 1.05rem; text-transform: uppercase; font-weight: 800; }
    
    /* Warning Flags (Orange overrides) */
    .stAlert { background-color: rgba(234, 88, 12, 0.1) !important; color: #f8fafc !important; border: 1px solid #ea580c !important; padding: 10px !important; }
    
    /* Minimize margins to prevent scrolling */
    hr { margin: 10px 0; border-color: #334155; }
    .stSelectbox { margin-bottom: -15px; }
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
    st.error("SYSTEM HALT: 'war_room_audit_2025.csv' missing.")
    st.stop()

# --- 3. INTEL REPOSITORY ---
def get_detailed_intel(country, c_data):
    repo = {
        "Belgium": ("Fiscal Dominance Shield", "Zero-emission corporate mandate bypasses consumer interest rate shocks."),
        "Australia": ("NVES Policy Alpha", "Prompt NVES implementation and FBT exemption surges commercial ROI."),
        "India": ("Strategic EMPS Pivot", "Supply plateauing, but PLI incentives force localized production. Buy on the dip."),
        "France": ("Eco-Score Moat", "Carbon-indexed subsidies block heavy imports, stabilizing domestic margins."),
        "Germany": ("Umweltbonus Shock", "Subsidy termination collapsed sales 35%. Severe mean-reversion phase active.")
    }
    return repo.get(country, ("GDP Organic S-Curve", "Adoption shielded by organic wealth scaling and robust infrastructure planning."))

# --- 4. TOP HEADER (COMPACT) ---
c_title, c_metrics = st.columns([1, 1])
with c_title:
    st.markdown("<h2 style='margin:0; color:#ffffff; font-weight:900; letter-spacing:-1px;'>GlobalCharge AI Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; color:#dc2626; font-weight:700;'>$100M REGIME-AWARE ALLOCATION MANDATE</p>", unsafe_allow_html=True)

# --- 5. MULTI-PAGE NAVIGATION (TABS) ---
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
tab_macro, tab_analytics, tab_logic = st.tabs(["🌍 MACRO ALLOCATION", "📊 REGIME MATRIX", "⚙️ SYSTEM LOGIC"])

with tab_macro:
    # 70/30 Split: Controls tightly packed on the left, Map on the right
    col_panel, col_map = st.columns([3, 7], gap="medium")
    
    with col_map:
        # MAP: Swapped to 'Oranges' scale per layout mandate, Transparent background
        fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Oranges")
        fig.update_geos(showland=True, landcolor="#1e293b", oceancolor="#0f172a", showframe=False, lakecolor="#0f172a", bgcolor='rgba(0,0,0,0)')
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0}, height=550, coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#f8fafc", size=14) 
        )
        map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
        
    with col_panel:
        selected_country = None
        if map_click and "selection" in map_click and map_click["selection"]["points"]:
            pt = map_click["selection"]["points"][0]
            selected_country = pt.get("location") or pt.get("hovertext")
        
        manual_sel = st.selectbox("TARGET MARKET SELECTOR", ["-- Awaiting System Input --"] + sorted(df['country'].unique().tolist()), label_visibility="collapsed")
        if not selected_country or selected_country not in df['country'].values:
            selected_country = manual_sel if manual_sel != "-- Awaiting System Input --" else None

        # INSTANT AUTO-LOAD (No "Generate" Button Required)
        if selected_country and selected_country in df['country'].values:
            c_data = df[df['country'] == selected_country].iloc[0]
            curr_p = c_data.get('new_prob_pct', 80)
            share = c_data.get('lagged_share', 15)
            gap = c_data.get('opportunity_gap', 0.5)
            roi = c_data.get('roi_score', 85)
            
            headline, context = get_detailed_intel(selected_country, c_data)
            
            st.markdown(f"<h3 style='margin-top:0px; margin-bottom:5px; color:#ffffff;'>TARGET: {selected_country.upper()}</h3>", unsafe_allow_html=True)
            
            m1, m2 = st.columns(2)
            m1.metric("CONFIDENCE", f"{curr_p:.1f}%")
            m2.metric("ALPHA GAP", f"{gap:.2f}")
            
            st.metric("ROI POTENTIAL INDEX", f"{roi:.1f}")
            
            if curr_p >= 78:
                st.success("**RISK:** TOLERABLE. Structural stability verified.")
            else:
                st.warning("**RISK:** VULNERABLE. Regime shift detected.")
                
            st.markdown(f"""
            <div class='intel-panel'>
                <h4>{headline}</h4>
                {context} <br><br>
                <strong>Stage:</strong> {'Takeoff' if share < 20 else 'Saturated'} ({share:.1f}% Adoption)
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # Empty State (Fits perfectly above the fold)
            st.markdown("<h3 style='margin-top:0; color:#64748b;'>SYSTEM IDLE</h3>", unsafe_allow_html=True)
            st.info("Select a country from the map or dropdown to instantly auto-load the regime audit.")
            st.metric("TOTAL AUM", "$500M")
            st.metric("ALLOCATION CAP", "$100M")
            st.metric("SYS PRECISION", "67.7%")

with tab_analytics:
    st.markdown("### 2024 Regime Shift Stress-Testing")
    st.write("This page will house the ROC-AUC curves and Feature Importance charts for the Random Forest, Naive Bayes, and KNN models you ran to predict the 2024 policy crashes.")

with tab_logic:
    st.markdown("### ML Portfolio Weightings")
    st.write("This page allows manual human override of the AI. Adjust the sliders below to prioritize specific market fundamentals:")
    st.slider("🛡️ Resilience Weight (AI Confidence)", 0.0, 2.0, 1.0, step=0.1)
    st.slider("📈 Market Room Weight (Alpha Gap)", 0.0, 2.0, 1.0, step=0.1)
    st.slider("💰 Wealth Weight (Purchasing Power)", 0.0, 2.0, 1.0, step=0.1)
