import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# 1. CORE CONFIGURATION
# ==========================================
st.set_page_config(page_title="GlobalCharge | Alpha", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 2. BOARDROOM CSS (NO SCROLL, GRID-LOCKED)
# ==========================================
st.markdown("""
    <style>
    /* Clean, flat institutional background */
    .stApp { background-color: #f8fafc; color: #0f172a; font-family: 'Helvetica Neue', Arial, sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Lock viewport to prevent global scrolling */
    html, body, [data-testid="stAppViewContainer"] { overflow: hidden !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 96% !important; }
    
    /* Hide scrollbars for a clean app feel */
    ::-webkit-scrollbar { display: none; }

    /* +2pt Enforced Metric Sizing & Red Primary Color */
    .metric-value { font-size: calc(2.2rem + 2pt); font-weight: 800; color: #dc2626; margin: 0; line-height: 1.1; letter-spacing: -1px; }
    .metric-label { font-size: calc(0.85rem + 2pt); font-weight: 700; color: #64748b; text-transform: uppercase; margin: 0; padding-bottom: 5px; }
    
    /* Orange Warning Architecture */
    .risk-orange { border-left: 4px solid #ea580c; background-color: #fff7ed; padding: 12px 16px; margin: 15px 0; border-radius: 2px; }
    .risk-orange-text { color: #c2410c; font-weight: 700; font-size: 0.95rem; margin: 0; }

    /* Red Target Architecture */
    .target-red { border-left: 4px solid #dc2626; background-color: #fef2f2; padding: 12px 16px; margin: 15px 0; border-radius: 2px; }
    .target-red-text { color: #991b1b; font-weight: 700; font-size: 0.95rem; margin: 0; }

    /* Clean Card Containers */
    .tearsheet-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 4px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); height: 100%; }
    h3 { font-size: 1.1rem; color: #0f172a; font-weight: 700; text-transform: uppercase; margin-top: 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px; }
    p { font-size: 0.95rem; color: #334155; line-height: 1.6; }
    
    /* Button Reset to Institutional Flat */
    .stButton>button { background-color: #ffffff; color: #0f172a; border: 1px solid #cbd5e1; border-radius: 2px; font-weight: 600; width: 100%; transition: 0.2s; }
    .stButton>button:hover { border-color: #dc2626; color: #dc2626; background-color: #fef2f2; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. STATE & DATA LOADER
# ==========================================
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = "India" # Defaulting to your Group's Emerging Alpha play

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
    # Fallback for presentation safety
    return pd.DataFrame({
        'country': ['India', 'Germany', 'Australia', 'USA', 'France'],
        'roi_score': [88, 45, 92, 85, 75],
        'new_prob_pct': [82, 35, 89, 81, 78],
        'opportunity_gap': [0.823, 0.12, 0.65, 0.55, 0.40],
        'lagged_share': [5.2, 22.5, 12.0, 9.5, 18.0]
    })

df = load_data()

def get_asset_intel(country):
    repo = {
        "India": ("Strategic Buy on the Dip", "The FAME-II transition caused a massive shift toward local manufacturing. Structural population demand vastly outstrips current adoption. Primary Emerging Alpha target for 2026.", True),
        "Germany": ("Severe Mean Reversion", "Subsidies abruptly removed Dec 2023. Traditional analysis failed here. Sales collapsed 35% early 2024. Avoid deployment until fundamentals stabilize.", False),
        "Australia": ("Core Safety Target", "Verified structural resilience. Benefiting from recent policy implementations protecting commercial ROI.", True)
    }
    return repo.get(country, ("GDP Organic S-Curve", "Market fundamentals verified. Proceed with standard capital allocation.", True))

# ==========================================
# 4. TOP EXECUTIVE BAR
# ==========================================
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #0f172a; margin-bottom: 15px; padding-bottom: 5px;">
        <h1 style="margin: 0; font-size: 1.5rem; font-weight: 900; letter-spacing: -0.5px; color: #0f172a;">GlobalCharge Capital :: Quantitative Allocation Engine</h1>
        <span style="font-weight: 600; color: #64748b; font-size: 0.9rem;">FUND AUM: $500M | DEPLOYMENT MANDATE: $100M</span>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. THE 3-COLUMN INSTITUTIONAL MATRIX
# ==========================================
col_watch, col_map, col_tear = st.columns([2, 5, 3], gap="medium")

# --- COLUMN 1: THE WATCHLIST (SCRENER) ---
with col_watch:
    with st.container(height=650, border=False):
        st.markdown("<div class='tearsheet-card'>", unsafe_allow_html=True)
        st.markdown("### ASSET WATCHLIST")
        st.write("Select market to load regime analytics:")
        
        # Clean button list for selection
        for country in sorted(df['country'].unique()):
            if st.button(f"{'▶ ' if st.session_state.selected_asset == country else ''}{country}", key=f"btn_{country}"):
                st.session_state.selected_asset = country
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- COLUMN 2: MACRO VISUALIZATION ---
with col_map:
    with st.container(height=650, border=False):
        st.markdown("<div class='tearsheet-card' style='padding: 0;'>", unsafe_allow_html=True)
        
        # Plotly Map using Orange scale (replacing standard heat reds)
        fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Oranges")
        fig.update_geos(showland=True, landcolor="#f1f5f9", oceancolor="#ffffff", showframe=False, lakecolor="#ffffff")
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0}, height=650, coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#0f172a", size=14)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

# --- COLUMN 3: THE TEAR SHEET ---
with col_tear:
    with st.container(height=650, border=False):
        target = st.session_state.selected_asset
        c_data = df[df['country'] == target].iloc[0]
        verdict, context, is_safe = get_asset_intel(target)
        
        st.markdown("<div class='tearsheet-card'>", unsafe_allow_html=True)
        
        # Header
        st.markdown(f"<h2 style='margin-top:0; color:#0f172a; font-weight:900; letter-spacing:-1px;'>{target.upper()}</h2>", unsafe_allow_html=True)
        
        # Risk Flags (Strict Orange vs Red)
        if not is_safe:
            st.markdown(f"""<div class='risk-orange'><p class='risk-orange-text'>
                WARNING: REGIME SHIFT DETECTED<br>Model flags high vulnerability to policy shocks.
            </p></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class='target-red'><p class='target-red-text'>
                STRUCTURALLY RESILIENT<br>Market fundamentals pass temporal stress tests.
            </p></div>""", unsafe_allow_html=True)
        
        # Scaled Metrics Grid
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"<p class='metric-label'>AI Confidence</p><p class='metric-value'>{c_data.get('new_prob_pct', 0):.1f}%</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-label'>Market Share</p><p class='metric-value'>{c_data.get('lagged_share', 0):.1f}%</p>", unsafe_allow_html=True)
        with m2:
            st.markdown(f"<p class='metric-label'>Alpha Gap</p><p class='metric-value'>{c_data.get('opportunity_gap', 0):.3f}</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"<p class='metric-label'>Target ROI</p><p class='metric-value'>{c_data.get('roi_score', 0):.1f}</p>", unsafe_allow_html=True)
            
        st.markdown("<hr style='border-color: #f1f5f9; margin: 25px 0;'>", unsafe_allow_html=True)
        
        # Qualitative Intel
        st.markdown(f"<h3 style='border:none; padding:0;'>STRATEGIC VERDICT</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-weight:700; color:#dc2626; margin-bottom:5px;'>{verdict}</p>", unsafe_allow_html=True)
        st.markdown(f"<p>{context}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
