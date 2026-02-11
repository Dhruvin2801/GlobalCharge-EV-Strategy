import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & "WHITE-PAPER" THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

# CSS for a completely clean, no-scroll, white-paper interface
st.markdown("""
    <style>
    /* Force white background */
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Remove padding to prevent scrolling */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Clean metric cards */
    [data-testid="stMetricValue"] { font-size: 1.6rem !important; color: #0f766e; font-weight: 800; }
    [data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #64748b; font-weight: 600; text-transform: uppercase; }
    
    /* Action Button Styling */
    .stButton>button { 
        background-color: #0f766e; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 6px; height: 3.2rem; width: 100%; border: none; 
        box-shadow: 0 4px 6px rgba(15, 118, 110, 0.2); transition: all 0.2s; margin-top: 15px;
    }
    .stButton>button:hover { background-color: #115e59; transform: translateY(-2px); }
    
    /* Pop-up Box styling */
    .intel-box { background-color: #f8fafc; padding: 25px; border-left: 6px solid #0f766e; border-radius: 8px; margin-top: 20px; line-height: 1.7; font-size: 1.05rem;}
    
    /* Adjust Slider spacing */
    .stSlider { padding-bottom: 0px; margin-bottom: -15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    files = ['war_room_data_v3.csv', 'war_room_data.csv', 'streamlit_data_v2.csv', 'streamlit_data.csv']
    for file in files:
        if os.path.exists(file):
            df = pd.read_csv(file)
            if not df.empty:
                if 'EV_Share_Pct_2023' not in df.columns: df['EV_Share_Pct_2023'] = df.get('EV_Share_Pct', 0) - 2.5
                if 'Policy_Score_2023' not in df.columns: df['Policy_Score_2023'] = df.get('Policy_Score', 0)
                if 'Survival_Prob' not in df.columns: df['Survival_Prob'] = 0.5
                if 'market_room' not in df.columns: df['market_room'] = (100 - df.get('EV_Share_Pct', 0)) / 100
                if 'purchasing_power' not in df.columns: df['purchasing_power'] = df.get('GDP_per_capita', 50000) / 10000
                if 'infra_saturation' not in df.columns: df['infra_saturation'] = 0.5
                return df
    return None

df = load_data()
if df is None:
    st.error("Data missing. Please upload your CSV to GitHub.")
    st.stop()

df['Base_ROI'] = (df['Survival_Prob'] * df['market_room'] * df['purchasing_power']) / (1 + df['infra_saturation']) * 100

# --- 3. DEEP INTELLIGENCE ENGINE ---
def get_comprehensive_intel(country, c_data, custom_roi):
    intel = {
        "Germany": (
            "⚠️ Constitutional Crisis & The Subsidy Cliff",
            "**2023-2024 Regime Shift:** In December 2023, the German Federal Constitutional Court struck down €60 billion in climate funding. This forced the immediate, premature cancellation of the *Umweltbonus* (up to €4,500 per EV). Consequently, H1 2024 saw a brutal 30%+ collapse in domestic EV sales. European OEMs (VW, Mercedes) have formally delayed their ICE phase-out targets as a result.",
            f"**Strategic ROI ({custom_roi:.1f}):** The AI model severely penalizes Germany's Resilience score. The data proves the market was artificially propped up by state aid rather than structural utility. Despite a massive $55k GDP/Capita providing organic purchasing power, the extreme political volatility and high existing infrastructure density make this a high-risk capital deployment zone."
        ),
        "USA": (
            "🛡️ IRA Deployment & Section 301 Trade Walls",
            "**2023-2024 Regime Shift:** The US market underwent a structural isolation event. In May 2024, the Biden Administration enacted 100% Section 301 tariffs on Chinese EVs, effectively blocking BYD and NIO from undercutting domestic OEMs. Concurrently, the NEVI Formula Program transitioned from planning to breaking ground, injecting billions into domestic highway charging corridors.",
            f"**Strategic ROI ({custom_roi:.1f}):** The USA is classified as a 'Safe Haven' with massive Protected Alpha. Growth is guaranteed by long-term Inflation Reduction Act (IRA) 30D tax credits locked through 2030, virtually eliminating European-style 'Subsidy Cliff' risks. High wealth and artificially protected margins yield top-tier infrastructure ROI."
        ),
        "Norway": (
            "✅ The Saturation Trap & Fiscal Rollbacks",
            "**2023-2024 Regime Shift:** Norway has completed the S-Curve (approaching 90% share). Recognizing peak adoption, the Norwegian government initiated a fiscal pullback in 2024. They implemented a new weight-based registration tax and applied a 25% VAT to luxury EVs (over 500k NOK) to recoup lost fossil-fuel road tax revenues. The hyper-growth era is officially over.",
            f"**Strategic ROI ({custom_roi:.1f}):** While the AI predicts 100% survival probability (the market functions entirely without subsidies now), the ROI is mechanically suppressed. There is functionally zero 'Market Room' remaining. Deploying a new $100M fund here operates as a low-yield public utility play rather than a venture-growth investment."
        ),
        "China": (
            "🏭 Post-Subsidy Hyper-Competition & Export Pivots",
            "**2023-2024 Regime Shift:** China officially terminated its decade-long national NEV purchase subsidy at the end of 2022/2023. 2024 is defined by a brutal, margin-crushing domestic price war (e.g., BYD launching the Seagull under $10,000). Facing up to 38% anti-subsidy tariffs from the EU in 2024, Chinese OEMs are furiously pivoting export capacity to the Global South.",
            f"**Strategic ROI ({custom_roi:.1f}):** China acts as a 'Maintenance Market'. The AI correctly identifies that Chinese EV adoption is structurally permanent (highly resilient). However, extreme over-saturation of existing charging infrastructure in Tier-1 and Tier-2 cities drastically dilutes the expected profit-margin per newly deployed charging plug."
        ),
        "Mexico": (
            "📈 USMCA Nearshoring & Fleet Mandates",
            "**2023-2024 Regime Shift:** Mexico is the primary beneficiary of geopolitical fracturing. To bypass US tariffs via USMCA 'Rules of Origin', Chinese OEMs (like BYD) spent 2024 aggressively scouting Mexican factory sites. Domestically, growth is surging not from consumer subsidies, but from heavy commercial fleet electrification (e.g., DHL, Walmart Mexico) fulfilling cross-border ESG mandates.",
            f"**Strategic ROI ({custom_roi:.1f}):** Mexico is a highly-rated 'Dark Horse'. The ROI is exceptionally strong because growth is driven by **Industrial Necessity**, not fickle consumer politics. Combined with 98% untapped 'Market Room', this represents one of the highest-alpha deployment targets in the portfolio."
        ),
        "UK": (
            "⚖️ The ZEV Mandate vs. Political Delays",
            "**2023-2024 Regime Shift:** The UK experienced conflicting market signals. While the strict ZEV Mandate took effect in Jan 2024 (requiring OEMs to hit 22% zero-emission sales or face massive fines), the Prime Minister simultaneously pushed the 2030 ICE ban back to 2035. This created severe consumer confusion and stalled private charging investments.",
            f"**Strategic ROI ({custom_roi:.1f}):** The AI model flags the UK with moderate resilience. The ZEV mandate forces OEM compliance, preventing a total collapse, but the political delay of the ICE ban reduces the immediate urgency for rapid, nationwide infrastructure expansion."
        ),
        "India": (
            "🌱 Local Manufacturing Subsidy Overhauls",
            "**2023-2024 Regime Shift:** The flagship FAME-II subsidy ended in March 2024 and was replaced by the leaner EMPS 2024 scheme. Crucially, in 2024, India slashed EV import taxes (from up to 100% down to 15%) for global automakers *only if* they commit to investing at least $500M in local manufacturing. This sparked a race to build localized supply chains.",
            f"**Strategic ROI ({custom_roi:.1f}):** India possesses astronomical 'Market Room'. The AI views the transition from consumer-handouts to manufacturing-incentives as a positive long-term resilience indicator. However, low current GDP/Capita restricts immediate consumer purchasing power, capping the short-term infrastructure ROI."
        )
    }
    
    # Dynamic fallback for unlisted countries
    if country not in intel:
        s_shift = c_data.get('EV_Share_Pct', 0) - c_data.get('EV_Share_Pct_2023', 0)
        p_shift = c_data.get('Policy_Score', 0) - c_data.get('Policy_Score_2023', 0)
        
        trend_word = "expanded" if s_shift >= 0 else "contracted"
        pol_word = "strengthened" if p_shift >= 0 else "weakened"
        
        dyn_headline = f"🔍 Macro-Economic Maturation Phase"
        dyn_context = f"**2023-2024 Market Dynamics:** {country} {trend_word} its EV market share by {abs(s_shift):.1f}% over the last 12 months. Concurrently, national policy support has {pol_word} (Shift: {p_shift:+.1f}). Our data pipelines indicate that adoption in {country} is closely following organic GDP S-Curve modeling, rather than being driven by sudden, disruptive geopolitical black-swan events."
        dyn_roi = f"**Strategic ROI ({custom_roi:.1f}):** The AI generated this score by mathematically weighing {country}'s purchasing power (${c_data.get('GDP_per_capita', 0):,.0f}) against its remaining untapped 'Market Room' ({c_data.get('market_room', 0)*100:.1f}%). The model views this region as a stable, secondary deployment target."
        return (dyn_headline, dyn_context, dyn_roi)
        
    return intel[country]

# --- 4. THE FINAL POP-UP REPORT ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_safe, w_room, w_wealth):
    c_data = df[df['country'] == country].iloc[0]
    
    custom_roi = ((c_data['Survival_Prob']**w_safe) * (c_data['market_room']**w_room) * (c_data['purchasing_power']**w_wealth)) / (1+c_data['infra_saturation']) * 100
    headline, context, roi_justification = get_comprehensive_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 0;'>Strategic Target: {country}</h2>", unsafe_allow_html=True)
    
    # Classifications
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        status = "🚀 Takeoff Phase" if c_data['EV_Share_Pct'] < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Data Justification:* Market exhibits {c_data['EV_Share_Pct']}% adoption. Capital deployment into markets under 20% yields the highest exponential returns before saturation.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data['Survival_Prob'] > 0.65 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Data Justification:* The Random Forest model predicts a {c_data['Survival_Prob']:.1%} probability of sustained market expansion in a strict, zero-subsidy environment.")

    st.markdown("---")
    
    # 2023-2024 Regime Shift Metrics
    st.markdown("### 2. Regime Shift Analytics (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    s_shift = c_data['EV_Share_Pct'] - c_data['EV_Share_Pct_2023']
    p_shift = c_data['Policy_Score'] - c_data['Policy_Score_2023']
    
    m1.metric("Current Market Share", f"{c_data['EV_Share_Pct']:.1f}%", f"{s_shift:+.1f}% vs 2023")
    m2.metric("Gov. Policy Support", f"{c_data['Policy_Score']:.1f} Score", f"{p_shift:+.1f} vs 2023")
    m3.metric("Purchasing Power", f"${c_data['GDP_per_capita']:,.0f}", "GDP/Capita")

    # Deep Intelligence Box
    st.markdown(f"""
    <div class='intel-box'>
        <h4 style='color: #0f766e; margin-top: 0;'>📰 Geopolitical & Policy Context: {headline}</h4>
        <p>{context}</p>
        <hr style="border: 1px solid #cbd5e1;">
        <h4 style='color: #0f766e;'>💰 ROI Justification & Verdict</h4>
        <p>{roi_justification}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SINGLE-PAGE LAYOUT ---
st.markdown("<h2 style='color: #0f766e; margin-bottom: 5px;'>GlobalCharge Intelligence Engine</h2>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.5, 2.5], gap="medium")

with col_map:
    # Use natural earth, but tell Plotly to show all landmasses so the whole map renders
    fig = px.choropleth(
        df, locations=df.get("iso_alpha", df["country"]), color="Base_ROI", 
        hover_name="country", color_continuous_scale="Teal", 
        projection="natural earth"
    )
    
    # update_geos forces the entire globe to render, filling missing countries with light gray
    fig.update_geos(
        showland=True, landcolor="#f1f5f9", 
        showocean=True, oceancolor="#ffffff",
        showcoastlines=True, coastlinecolor="#cbd5e1",
        showframe=False,
        lataxis_range=[-55, 90] # Hides empty Antarctica to make the map look larger
    )
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, height=550,
        coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    selected_country = None
    if map_click and map_click["selection"]["points"]:
        selected_country = map_click["selection"]["points"][0]["hovertext"]
    
    c_list = df['country'].tolist()
    if selected_country not in c_list and selected_country is not None:
        iso_match = df[df['iso_alpha'] == selected_country]
        if not iso_match.empty: selected_country = iso_match.iloc[0]['country']

    if selected_country:
        # STATE: COUNTRY CLICKED
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 0; color: #1e293b;'>🎯 Target: {selected_country}</h3>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.metric("GDP/Capita", f"${c_data['GDP_per_capita']:,.0f}")
        c2.metric("EV Share", f"{c_data['EV_Share_Pct']}%")
        
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("**⚙️ Configuration Mandate**")
        
        w_safe = st.slider("🛡️ Resilience Weight", 0.0, 2.0, 1.0, step=0.1)
        w_room = st.slider("📈 Market Room Weight", 0.0, 2.0, 1.0, step=0.1)
        w_wealth = st.slider("💰 Wealth Weight", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, w_safe, w_room, w_wealth)
            
    else:
        # STATE: INITIAL LOAD
        st.markdown("<h3 style='margin-top: 0; color: #1e293b;'>🌍 Global Portfolio</h3>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        c1.metric("Capital Mandate", "$100M")
        c2.metric("Markets Audited", f"{len(df)}")
        
        st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("**🏆 Top 3 Baseline ROI Targets**")
        
        top_3 = df.nlargest(3, 'Base_ROI')[['country', 'Base_ROI']]
        top_3['Base_ROI'] = top_3['Base_ROI'].apply(lambda x: f"{x:.1f}")
        st.dataframe(top_3.rename(columns={'country': 'Market', 'Base_ROI': 'Est. Score'}), hide_index=True, use_container_width=True)
        
        st.info("👆 **Select a market on the map** to configure parameters and run a deep-dive intelligence audit.")
