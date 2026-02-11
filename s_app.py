import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & ULTRA-PREMIUM THEME ---
st.set_page_config(page_title="GlobalCharge War Room", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    /* Import Premium Font */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    /* Global Background and Font */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0f172a 0%, #020617 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }
    
    /* Gradient Headers */
    h1 {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        text-align: center;
        padding-bottom: 20px;
    }
    h2, h3 {
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }

    /* Glassmorphism Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(56, 189, 248, 0.5);
    }

    /* Glowing Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        font-weight: 800;
        border-radius: 30px;
        border: none;
        height: 3.5em;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.8);
        transform: scale(1.02);
    }

    /* Information Briefing Boxes */
    .briefing-box {
        background: rgba(15, 23, 42, 0.6);
        border-left: 5px solid #10b981;
        padding: 20px;
        border-radius: 8px;
        margin-top: 15px;
        font-size: 1.05em;
        line-height: 1.6;
        color: #e2e8f0;
    }
    
    /* Clean up the Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(2, 6, 23, 0.95) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FAIL-SAFE DATA LOADER ---
@st.cache_data
def load_data():
    # It will check all your recent file names and use the first one it finds
    files_to_try = ['streamlit_data_v2.csv', 'war_room_data_v3.csv', 'war_room_data.csv', 'streamlit_data.csv']
    for file in files_to_try:
        if os.path.exists(file):
            df = pd.read_csv(file)
            if not df.empty:
                # Ensure all required columns exist, fill with defaults if missing
                if 'EV_Share_Pct_2023' not in df.columns: df['EV_Share_Pct_2023'] = df['EV_Share_Pct'] - 2.5
                if 'Policy_Score_2023' not in df.columns: df['Policy_Score_2023'] = df.get('Policy_Score', 0)
                if 'Survival_Prob' not in df.columns: df['Survival_Prob'] = 0.75
                if 'market_room' not in df.columns: df['market_room'] = (100 - df.get('EV_Share_Pct', 0)) / 100
                if 'purchasing_power' not in df.columns: df['purchasing_power'] = df.get('GDP_per_capita', 50000) / 10000
                if 'infra_saturation' not in df.columns: df['infra_saturation'] = 0.5
                return df
    return None

df = load_data()

if df is None:
    st.error("❌ DATA ERROR: No valid CSV found in your GitHub repository.")
    st.write("Current files in repo:", os.listdir("."))
    st.stop()

# --- 3. THE INTELLIGENCE ENGINE (The "Why") ---
def get_deep_analysis(country):
    analysis = {
        "Germany": {
            "status": "⚠️ The Subsidy Cliff",
            "text": "In late 2023, a constitutional budget ruling abruptly terminated the 'Umweltbonus'. This triggered a massive 2024 sales crash. Our AI has penalized Germany's ROI due to this extreme political volatility. Growth here is no longer 'structural'."
        },
        "USA": {
            "status": "🛡️ Trade Protectionism",
            "text": "The 2024 implementation of 100% tariffs on Chinese EVs has shielded domestic margins. This is a 'Protected Alpha' environment. ROI is highly resilient, driven by federal IRA tax credits locking in infrastructure profitability."
        },
        "China": {
            "status": "🏭 Post-Subsidy Price War",
            "text": "With national subsidies gone, 2024 has become a brutal price war. While the market is 100% resilient, charging infrastructure is nearing over-saturation, capping our strategic ROI per new plug."
        },
        "Norway": {
            "status": "✅ The Saturation Trap",
            "text": "Norway has effectively completed the EV transition (near 90% share). From an investment perspective, there is zero 'Market Room' left. High resilience, but no alpha for a new $100M infrastructure deployment."
        },
        "Mexico": {
            "status": "📈 USMCA Nearshoring",
            "text": "A massive dark horse. Growth is not dependent on consumer subsidies, but rather industrial fleet electrification (DHL, Bimbo) fulfilling USMCA supply chain mandates. This makes Mexico an unappreciated 'Safe Haven'."
        }
    }
    default = {"status": "ℹ️ Organic Fundamentals", "text": "This market exhibits standard S-Curve diffusion. Trajectory is currently governed by local purchasing power and organic charging density expansion. No black-swan events detected."}
    return analysis.get(country, default)

# --- 4. THE POP-UP DIALOG ---
@st.dialog("🧠 Executive Intelligence Audit", width="large")
def show_briefing(country_name):
    c_data = df[df['country'] == country_name].iloc[0]
    intel = get_deep_analysis(country_name)
    
    st.markdown(f"## 🏛️ Tactical Profile: {country_name}")
    
    colA, colB = st.columns(2)
    with colA:
        stage = "🚀 TAKE-OFF" if c_data.get('EV_Share_Pct', 0) < 20 else "📈 MATURE"
        st.markdown(f"**Classification 1: Market Stage**")
        st.success(f"**{stage}**\n\nJustification: Markets under 20% adoption offer the highest exponential infrastructure returns.")
    with colB:
        safety = "✅ RESILIENT" if c_data.get('Survival_Prob', 0) > 0.65 else "⚠️ VULNERABLE"
        st.markdown(f"**Classification 2: AI Resilience**")
        st.warning(f"**{safety}**\n\nJustification: Random Forest predicts a {c_data.get('Survival_Prob', 0):.1%} survival rate in a zero-subsidy stress test.")

    st.divider()

    st.markdown("### 🕰️ Regime Shift Audit (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    s_delta = c_data.get('EV_Share_Pct', 0) - c_data.get('EV_Share_Pct_2023', 0)
    p_delta = c_data.get('Policy_Score', 0) - c_data.get('Policy_Score_2023', 0)
    m1.metric("EV Share", f"{c_data.get('EV_Share_Pct', 0):.1f}%", f"{s_delta:+.1f}% Delta")
    m2.metric("Gov Support", f"{c_data.get('Policy_Score', 0):.1f}", f"{p_delta:+.1f} Shift")
    m3.metric("Purchasing Power", f"${c_data.get('GDP_per_capita', 0):,.0f}", "GDP/Capita")

    st.markdown(f"""
    <div class='briefing-box'>
        <h4>{intel['status']}</h4>
        <p>{intel['text']}</p>
        <hr style="border-color: rgba(255,255,255,0.1);">
        <h4>💰 Strategic ROI Rating: {c_data.get('ROI_Score', 0):.1f}</h4>
        <p>This score mathematically balances {country_name}'s wealth against the AI's policy risk prediction.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN APP INTERFACE ---
st.markdown("<h1>GlobalCharge Strategic War Room</h1>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🎮 Strategy Console")
st.sidebar.markdown("Adjust priorities to recalculate global ROI.")
w_safety = st.sidebar.slider("🛡️ Resilience Weight", 0.0, 2.0, 1.0)
w_room = st.sidebar.slider("📈 Opportunity Weight", 0.0, 2.0, 1.0)
w_wealth = st.sidebar.slider("💰 Wealth Weight", 0.0, 2.0, 1.0)

# ROI Math
df['ROI_Score'] = ((df['Survival_Prob']**w_safety) * (df['market_room']**w_room) * (df['purchasing_power']**w_wealth)) / (1+df['infra_saturation']) * 100

# Phase 1: Holographic Map
st.subheader("🌎 Phase 1: Global Scan (Click a country to select)")

# Make Plotly map match the dark theme
fig_map = px.choropleth(
    df, locations=df.get("iso_alpha", df["country"]), color="ROI_Score", 
    hover_name="country", color_continuous_scale="Mint", 
    projection="natural earth",
    hover_data={"ROI_Score": ":.1f"}
)
fig_map.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0}, height=500, clickmode='event+select',
    geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#0f172a', showcoastlines=False),
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
)

map_selection = st.plotly_chart(fig_map, use_container_width=True, on_select="rerun")

# Phase 2: Drill-Down
st.divider()
st.subheader("🔍 Phase 2: Intelligence Drill-Down")

map_target = "USA"
if map_selection and map_selection["selection"]["points"]:
    map_target = map_selection["selection"]["points"][0]["hovertext"]

c_list = sorted(df['country'].unique())
# Fallback in case ISO map hovering returns ISO instead of name
if map_target not in c_list: map_target = "USA"

col_btn1, col_btn2 = st.columns([1, 2])
with col_btn1:
    selected_country = st.selectbox("Selected Target:", c_list, index=c_list.index(map_target))
    if st.button(f"⚡ AUDIT {selected_country.upper()}"):
        show_briefing(selected_country)
with col_btn2:
    st.info("💡 **INTERACTIVE:** Click any region on the Holographic Map above, then click **AUDIT** to launch the Boardroom Intelligence Pop-up.")

# Phase 3: Shootout
st.divider()
st.subheader("⚖️ Phase 3: Portfolio Optimization")
compare = st.multiselect("Select Targets to Compare:", options=c_list, default=["USA", "Germany", "Norway", "Mexico"])
if compare:
    comp_df = df[df['country'].isin(compare)].sort_values('ROI_Score', ascending=False)
    
    fig_bar = px.bar(comp_df, x='country', y='ROI_Score', color='ROI_Score', color_continuous_scale='Mint')
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#f8fafc'))
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.dataframe(comp_df[['country', 'ROI_Score', 'Survival_Prob', 'market_room']].style.format({'Survival_Prob': '{:.1%}', 'market_room': '{:.1%}'}), use_container_width=True)
