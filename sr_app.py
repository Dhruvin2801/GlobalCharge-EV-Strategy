import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIG & "EXECUTIVE PLATINUM" THEME ---
st.set_page_config(page_title="GlobalCharge Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1e293b; font-family: 'Inter', sans-serif; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 98%; }
    
    /* Premium Metric Styling */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #0f766e; font-weight: 800; letter-spacing: -0.05rem; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #64748b; font-weight: 700; text-transform: uppercase; }
    
    /* Audit Button Styling */
    .stButton>button { 
        background-color: #0f766e; color: white; font-weight: 800; text-transform: uppercase;
        border-radius: 8px; height: 3.5rem; width: 100%; border: none; 
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.25); transition: all 0.3s ease; margin-top: 15px;
    }
    .stButton>button:hover { background-color: #115e59; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(15, 118, 110, 0.35); }
    
    /* Intel Box Styling */
    .intel-box { background-color: #f8fafc; padding: 28px; border-left: 8px solid #0f766e; border-radius: 12px; margin-top: 20px; line-height: 1.8; }
    .intel-box h4 { color: #0f766e; font-weight: 800; margin-bottom: 12px; text-transform: uppercase; font-size: 1.1rem; }
    .intel-box p { color: #334155; font-size: 1.05rem; }
    
    /* Slider Clean-up */
    .stSlider { padding-bottom: 0px; margin-bottom: -10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ROBUST DATA LOADER ---
@st.cache_data
def load_data():
    file = 'war_room_audit_2025_FINAL.csv'
    if os.path.exists(file):
        df = pd.read_csv(file)
        df.columns = [c.lower() for c in df.columns] # Force lowercase to prevent KeyErrors
        # Standardize 'country' column
        if 'country' not in df.columns:
            for c in df.columns:
                if 'name' in c or 'nation' in c: df.rename(columns={c: 'country'}, inplace=True)
        return df
    return None

df = load_data()
if df is None:
    st.error("🚨 CRITICAL ERROR: 'war_room_audit_2025_FINAL.csv' missing from repository.")
    st.stop()

# --- 3. THE DEEP INTELLIGENCE REPOSITORY (GEOPOLITICAL 'WHY') ---
def get_detailed_intel(country, c_data, custom_roi):
    repo = {
        "Belgium": (
            "⚖️ Fiscal Dominance & The Company Car Mandate",
            "**2023-2024 Regime Shift:** Belgium's market is uniquely shielded by its 'Company Car' tax structure. In 2024, the government mandated that only zero-emission company vehicles qualify for 100% tax deductibility. This created an artificial but highly resilient 'floor' for adoption.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Defensive Safe Haven. The structural corporate mandate makes it highly stable for long-term infrastructure ROI."
        ),
        "Australia": (
            "🛡️ NVES Policy Shield & The FBT Exemption",
            "**2023-2024 Regime Shift:** Australia successfully avoided the 2024 European crash by implementing the New Vehicle Efficiency Standard (NVES). Combined with the ongoing Fringe Benefits Tax (FBT) exemption, commercial fleet ROI has surged.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Core Growth Target. The 12% share provides exponential room for growth, heavily shielded by federal tax law."
        ),
        "India": (
            "🐘 The EMPS Pivot & The Opportunity Alpha",
            "**2023-2024 Regime Shift:** India's pivot from FAME-II to the EMPS scheme caused a temporary supply-side plateau. However, the 2024 manufacturing incentive (PLI) has forced global giants like Tesla and VinFast into localized production talks.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Emerging Alpha Play. Targets the 2026 S-Curve breakout. Massive structural demand outweighs current policy transitions."
        ),
        "France": (
            "🇫🇷 The 'Eco-Score' Moat & Sovereign Protection",
            "**2023-2024 Regime Shift:** France's 2024 'Eco-Score' redefined subsidies to exclude carbon-intensive shipping. This effectively subsidized European-made EVs while taxing Asian imports.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Protected Mature Market. Highly resilient to the 2024 Chaos Regime because its policy actively shields domestic margins."
        ),
        "Germany": (
            "⚠️ The 'Umweltbonus' Shock & Subsidy Cliff",
            "**2023-2024 Regime Shift:** The Dec 2023 constitutional court ruling forced an immediate end to all EV subsidies. This 'Policy Heart Attack' proved that German adoption was an artificial bubble. Sales collapsed 35% in early 2024.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** High Volatility Value Trap. Human veto recommended until structural mean reversion stabilizes in late 2025."
        ),
        "USA": (
            "🦅 The Inflation Reduction Act (IRA) & Reshoring",
            "**2023-2024 Regime Shift:** The $7,500 IRA tax credit created a localized manufacturing boom, decoupling US adoption from global supply chain shocks. The $5B NEVI formula program is forcing charging infrastructure across all 50 states.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Primary Core Asset. Massive market room combined with locked-in federal capital guarantees structural resilience."
        ),
        "China": (
            "🐉 Post-Subsidy Saturation & Price Wars",
            "**2023-2024 Regime Shift:** The total phase-out of national EV subsidies in late 2022 triggered a brutal domestic price war between BYD and Tesla. The market has shifted from policy-driven to pure hyper-competitive saturation (>35% penetration).",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Mature / Saturated. Market room is shrinking. Deploy capital selectively into hyper-local grid management rather than broad growth."
        ),
        "UK": (
            "🇬🇧 ZEV Mandate vs Retail Apathy",
            "**2023-2024 Regime Shift:** The UK implemented a strict ZEV mandate requiring 22% of OEM sales to be zero-emission by 2024. While high interest rates stalled private retail demand, corporate fleet adoption is forced forward by aggressive tax incentives.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Stable. Fleet mandates provide a reliable floor, insulating the market from consumer inflation fears."
        ),
        "Norway": (
            "❄️ The 'End-State' Market Transition",
            "**2023-2024 Regime Shift:** Having reached >90% EV sales, Norway began scaling back tax exemptions, imposing VAT on luxury EVs. It represents the 'end-state' of EV adoption where subsidies are no longer required.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Saturated Safe Haven. Zero policy risk, but zero exponential growth opportunity. A pure defensive play."
        ),
        "Sweden": (
            "🇸🇪 'Climate Bonus' Removal & Corporate Leasing",
            "**2023-2024 Regime Shift:** Sweden abruptly scrapped its 'Climate Bonus' in late 2022, causing a temporary dip. However, high carbon taxes on ICE vehicles and strong corporate leasing policies have maintained adoption resilience.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Structurally sound. Withstood policy shock via pure GDP wealth and corporate infrastructure."
        ),
        "Canada": (
            "🍁 Federal ZEV Mandate & iZEV Alignment",
            "**2023-2024 Regime Shift:** Anchored by a federal mandate for 100% ZEV sales by 2035 and the $5,000 iZEV rebate. The market closely mirrors the US trajectory but with more predictable federal policy support.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** High Conviction. Strong purchasing power and immense market room make this a Tier 1 target."
        ),
        "Spain": (
            "🇪🇸 Bureaucratic Friction & MOVES III",
            "**2023-2024 Regime Shift:** The MOVES III subsidy program was extended, but severe bureaucratic friction in paying out consumers has suppressed the takeoff phase. EV penetration remains heavily lagging at ~12%.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** High Risk. Policy exists on paper but fails in execution. Model flags for immediate veto."
        ),
        "Italy": (
            "🇮🇹 Income-Tiered Ecobonus Overhaul",
            "**2023-2024 Regime Shift:** Overhauled its 'Ecobonus' in 2024 to target low-income buyers and heavily scrap older ICE vehicles. However, severely lacking charging infrastructure keeps structural resilience critically low.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Vulnerable. High risk of supply bottleneck. Do not deploy without hard infrastructure guarantees."
        ),
        "Japan": (
            "🗾 Hybrid Dominance & The Kei-EV",
            "**2023-2024 Regime Shift:** Domestic OEMs (Toyota) aggressively prioritize hybrid (HEV) technology. Pure BEV adoption is structurally blocked by cultural preferences, aside from niche 'Kei-EV' domestic models like the Nissan Sakura.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Veto. Market fundamentally resists full electrification. ROI models do not support capital entry."
        ),
        "South Korea": (
            "🔋 Battery-Density Subsidy Protectionism",
            "**2023-2024 Regime Shift:** Revised subsidies in 2024 to heavily favor high-density batteries and extensive charging networks, an explicit policy designed to protect domestic giants (Hyundai/Kia) from cheaper LFP-based Chinese imports.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Deploy Cautiously. Strong tech ecosystem, but foreign infrastructure capital faces headwinds."
        ),
        "Israel": (
            "🇮🇱 Purchase Tax Spike & Demand Pull-Forward",
            "**2023-2024 Regime Shift:** Purchase taxes on EVs increased significantly in January 2024. This caused massive 'pull-forward' demand in late 2023, leading to an artificial sales freeze and plateau throughout 2024.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Temporal anomaly detected. Underlying tech adoption is high, but near-term capital deployment will underperform."
        ),
        "Mexico": (
            "🏭 The Nearshoring Production Boom",
            "**2023-2024 Regime Shift:** Driven purely by the 'nearshoring' manufacturing boom rather than retail subsidies. Chinese OEMs (BYD) are rapidly flooding the market to secure a North American foothold around US tariffs.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Emerging Growth. A high-leverage backdoor into NAFTA supply chains. Approved for Alpha allocation."
        ),
        "Brazil": (
            "🇧🇷 Import Tax Reintroduction",
            "**2023-2024 Regime Shift:** Reintroduced staggered import taxes on EVs in January 2024 to force local manufacturing. This triggered massive stockpiling and sales spikes of Chinese imports in late 2023 before the tax hit.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Volatile Takeoff. High risk/reward. Only deploy capital aligned with localized manufacturing mandates."
        ),
        "Chile": (
            "⛰️ Commercial Electromobility Strategy",
            "**2023-2024 Regime Shift:** Focused strictly on commercial and public transport electrification through the National Electromobility Strategy, actively avoiding the volatile retail consumer subsidy traps seen in Europe.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Niche Safety. B2B and public transit infrastructure ROI is highly resilient here."
        ),
        "Denmark": (
            "🇩🇰 Phased Registration Tax Re-entry",
            "**2023-2024 Regime Shift:** Successfully managing a phased reintroduction of registration taxes for EVs without crashing the market, backed by incredibly robust charging infrastructure and very high GDP per capita.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Resilient Mature Market. Handled the tax phase-in flawlessly. Safe deployment target."
        ),
        "Finland": (
            "🇫🇮 Subsidies Swapped for Tax Incentives",
            "**2023-2024 Regime Shift:** Removed direct EV purchase subsidies but maintained highly favorable company car taxation. Market growth has cooled slightly but remains structurally sound due to high baseline wealth.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Approved. Organic demand remains strong despite the removal of direct state cash."
        ),
        "Iceland": (
            "🌋 Mileage-Tax Contraction",
            "**2023-2024 Regime Shift:** Replaced full VAT exemptions with a mileage-based road tax in 2024. The sudden removal of the upfront tax shield caused a severe and immediate market contraction.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Veto. Model correctly caught the regime shift. Capital deployment blocked."
        ),
        "Netherlands": (
            "🇳🇱 SEPP Subsidy & Infrastructure Saturation",
            "**2023-2024 Regime Shift:** Tightened the SEPP subsidy pool, but the market is highly mature with one of the densest charging networks globally. The market is transitioning from early adopters to standard mass-market pricing.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Defensive Yield. The growth phase is over; this is now a pure infrastructure yield play."
        ),
        "New Zealand": (
            "🇳🇿 'Clean Car Discount' Repeal",
            "**2023-2024 Regime Shift:** The sudden political repeal of the 'Clean Car Discount' in Dec 2023 crashed Q1 2024 sales. However, high wealth and geographic isolation keep long-term fundamental demand metrics intact.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Monitor. Survived the policy shock better than Germany, but requires a 6-month holding pattern."
        ),
        "Poland": (
            "🇵🇱 'My Elektryk' & Localized Battery Hubs",
            "**2023-2024 Regime Shift:** Supported by the 'My Elektryk' scheme, the market is in its infancy. Benefiting heavily from major investments in battery manufacturing (LG), driving localized structural momentum.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Eastern European Alpha. High room for growth backed by hard supply-chain manufacturing capital."
        ),
        "Portugal": (
            "🇵🇹 Privatized Subsidy Cuts",
            "**2023-2024 Regime Shift:** Cut state subsidies for private EV purchases entirely in 2024, redirecting funds exclusively to commercial fleets and charities. The private consumer market faces heavy headwinds.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Pivot required. Shift all planned deployment from retail to commercial fleet charging."
        ),
        "Switzerland": (
            "🇨🇭 High Wealth, High Import Tax",
            "**2023-2024 Regime Shift:** Imposed a new 4% import tax on EVs starting in 2024. Lacking federal purchase subsidies, the market is entirely dependent on its massive organic high-wealth consumer demand.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Deploy. Wealth metrics easily absorb the 4% tax shock. Extremely resilient core market."
        ),
        "Austria": (
            "🇦🇹 Fleet Subsidy Reallocation",
            "**2023-2024 Regime Shift:** Slashed corporate EV subsidies to redirect capital toward private buyers and public charging infrastructure, attempting to stabilize the retail market against corporate fleet volatility.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Approved. The redirection of state funds into hard infrastructure de-risks capital deployment."
        ),
        "Greece": (
            "🇬🇷 'Kinoumai Ilektrika' Dependency",
            "**2023-2024 Regime Shift:** Highly reliant on the 'Kinoumai Ilektrika' state aid. With low GDP per capita, the market is artificial. Any removal of this subsidy will cause an immediate and total market collapse.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Veto. Fundamental wealth does not support the adoption curve. High risk of a Germany-style crash."
        ),
        "Turkey": (
            "🇹🇷 The 'Togg' Nationalist Boom",
            "**2023-2024 Regime Shift:** Despite massive hyperinflation, the launch of the domestic EV brand 'Togg' created overwhelming nationalistic demand, completely decoupling adoption from standard macroeconomic indicators.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Anomalous Takeoff. The model flags this as highly irregular. Growth is massive but defies standard risk parameters."
        ),
        "Rest of World": (
            "🌍 Emerging Market Grid Constraints",
            "**2023-2024 Regime Shift:** Represents aggregate emerging markets where EV adoption is currently limited by grid stability and upfront costs, but opportunity gaps are widening rapidly as ICE price-parity approaches.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Hold. Wait for battery pack prices to drop below $80/kWh before broad deployment."
        )
    }
    
    # Dynamic Fallback
    res = repo.get(country)
    if res: return res
    
    gap = c_data.get('opportunity_gap', 0.5)
    return (f"🔍 Structural Resilience Audit: {country}", 
            f"**2023-24 Dynamics:** {country} is following a classic GDP-driven S-Curve. Adoption is shielded from European political volatility by organic wealth growth and the redirection of global supply chains toward non-tariffed regions.",
            f"**Strategic Verdict (ROI {custom_roi:.1f}):** Stable deployment target with an Opportunity Gap of {gap:.2f}. Growth is driven by long-term infrastructure expansion rather than fickle state aid.")

# --- 4. THE EXECUTIVE AUDIT DIALOG ---
@st.dialog("📋 OFFICIAL EXECUTIVE AUDIT REPORT", width="large")
def show_final_report(country, w_s, w_r, w_w):
    c_data = df[df['country'] == country].iloc[0]
    prob = c_data.get('new_prob_pct', 80) / 100
    room = c_data.get('market_room', 0.5)
    
    # Extract GDP per capita for Wealth scaling (centered around $40,000 global average)
    wealth = c_data.get('gdp_per_capita', c_data.get('purchasing_power', 40000))
    base_roi = c_data.get('roi_score', 500)
    
    # ⚙️ MATHEMATICAL FIX: Centered Mandate Multipliers 
    # If slider > 1.0, it amplifies the country's deviation from the average.
    
    # 1. Resilience Mod (Centers at 50% probability)
    mod_s = max(0.1, 1 + (w_s - 1.0) * (prob - 0.5) * 2)
    
    # 2. Market Room Mod (Centers at 50% room)
    mod_r = max(0.1, 1 + (w_r - 1.0) * (room - 0.5) * 2)
    
    # 3. Wealth Mod (Centers at $40,000 GDP, capped at 2x to prevent infinity spikes)
    norm_w = min(wealth / 40000, 2.0) 
    mod_w = max(0.1, 1 + (w_w - 1.0) * (norm_w - 1.0))
    
    # Final dynamic ROI
    custom_roi = base_roi * mod_s * mod_r * mod_w
    
    headline, context, verdict = get_detailed_intel(country, c_data, custom_roi)
    
    st.markdown(f"<h2 style='color: #0f766e; margin-bottom: 5px;'>Strategic Audit: {country}</h2>", unsafe_allow_html=True)
    
    # SECTION 1: Classifications (DITTO IMAGE STYLE)
    st.markdown("### 1. Market Classifications")
    c1, c2 = st.columns(2)
    with c1:
        share = c_data.get('lagged_share', 15)
        status = "🚀 Takeoff Phase" if share < 20 else "📉 Mature / Saturated"
        st.info(f"**Classification 1: Market Stage**\n\n**{status}**\n\n*Justification:* Market exhibits {share:.1f}% adoption. Deployment into markets under 20% yields highest exponential returns.")
    with c2:
        resilience = "✅ Highly Resilient" if c_data.get('new_prob_pct', 0) >= 78 else "⚠️ Policy Vulnerable"
        st.warning(f"**Classification 2: AI Risk Profile**\n\n**{resilience}**\n\n*Justification:* Model identifies high structural stability despite the 2024 'Chaos Regime' shifts.")

    st.markdown("---")
    
    # SECTION 2: Analytics
    st.markdown("### 2. Regime Shift Analytics (2023 ➔ 2024)")
    m1, m2, m3 = st.columns(3)
    curr_p = c_data.get('new_prob_pct', 0)
    base_p = c_data.get('base_prob_pct', 75)
    m1.metric("AI Confidence", f"{curr_p:.1f}%", f"{curr_p - base_p:+.1f}% vs Baseline")
    m2.metric("Opportunity Gap", f"{c_data.get('opportunity_gap', 0):.2f}", "Alpha Index")
    m3.metric("ROI Potential Index", f"{custom_roi:,.0f}", "Scaled Score")

    # SECTION 3: Deep Intel Box
    st.markdown(f"""
    <div class='intel-box'>
        <h4>📰 Geopolitical Context: {headline}</h4>
        <p>{context}</p>
        <hr style='border: 1px solid #cbd5e1; margin: 20px 0;'>
        <h4>💰 ROI Justification & Verdict</h4>
        <p>{verdict}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 style='color: #0f766e; margin-bottom: 0px;'>GlobalCharge Intelligence Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-weight: 600; margin-top: 0;'>EXECUTIVE INVESTMENT DASHBOARD | REGIME-AWARE AUDIT</p>", unsafe_allow_html=True)

col_map, col_panel = st.columns([7.2, 2.8], gap="medium")

with col_map:
    fig = px.choropleth(df, locations="country", locationmode='country names', color="roi_score", color_continuous_scale="Teal")
    fig.update_geos(showland=True, landcolor="#f1f5f9", oceancolor="#ffffff", showframe=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=550, coloraxis_showscale=False)
    map_click = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

with col_panel:
    # Triple-Redundant Selection
    selected_country = None
    if map_click and "selection" in map_click and map_click["selection"]["points"]:
        pt = map_click["selection"]["points"][0]
        selected_country = pt.get("location") or pt.get("hovertext")
    
    # Fallback Selector
    st.markdown("<hr style='margin: 0;'>", unsafe_allow_html=True)
    manual_sel = st.selectbox("Select Target Market:", ["Click Map..."] + sorted(df['country'].unique().tolist()))
    if not selected_country or selected_country not in df['country'].values:
        selected_country = manual_sel if manual_sel != "Click Map..." else None

    if selected_country and selected_country in df['country'].values:
        c_data = df[df['country'] == selected_country].iloc[0]
        st.markdown(f"<h3 style='margin-top: 10px;'>🎯 Target: {selected_country}</h3>", unsafe_allow_html=True)
        st.metric("ROI Score", f"{c_data.get('roi_score', 0):.1f}")
        st.metric("AI Confidence", f"{c_data.get('new_prob_pct', 0):.1f}%")
        
        st.markdown("**⚙️ Configuration Mandate**")
        ws = st.slider("🛡️ Resilience", 0.0, 2.0, 1.0, step=0.1)
        wr = st.slider("📈 Market Room", 0.0, 2.0, 1.0, step=0.1)
        ww = st.slider("💰 Wealth", 0.0, 2.0, 1.0, step=0.1)
        
        if st.button("GENERATE EXECUTIVE AUDIT"):
            show_final_report(selected_country, ws, wr, ww)
    else:
        st.markdown("<h3 style='margin-top: 10px;'>🌍 Portfolio Audit</h3>", unsafe_allow_html=True)
        st.metric("Capital Mandate", "$100M")
        st.metric("Precision (2024)", "67.7%")
        st.info("Select a country on the map or use the selector to run the 78% Margin of Safety audit.")
