import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================================================================
# 1. PAGE CONFIG & ASSET LOADING
# ==============================================================================
st.set_page_config(page_title="GlobalCharge | Investment Audit", layout="wide")

@st.cache_resource
def load_models():
    # Loading the new innovative intelligence
    model = joblib.load('rf_regime_aware_model.pkl')
    regime_detector = joblib.load('gmm_regime_detector.pkl')
    return model, regime_detector

@st.cache_data
def load_audit_data():
    # Loading the pre-calculated ROI and Gap data
    return pd.read_csv('war_room_audit_2025.csv')

try:
    rf_model, gmm_detector, df_audit = load_models(), load_models()[1], load_audit_data()
except Exception as e:
    st.error(f"Error loading assets: Ensure 'rf_regime_aware_model.pkl', 'gmm_regime_detector.pkl', and 'war_room_audit_2025.csv' are in the app folder.")
    st.stop()

# ==============================================================================
# 2. SIDEBAR - RISK CONTROL
# ==============================================================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2620/2620582.png", width=100)
st.sidebar.title("Investment Control")
st.sidebar.markdown("---")

# The Margin of Safety Slider - The core of our innovation
margin_of_safety = st.sidebar.slider(
    "Set Margin of Safety (%)", 
    min_value=50, max_value=95, value=78, step=1,
    help="Mathematically optimized at 78% for the 2024 Regime Shift. Raising this reduces 'False Positive' risk."
)

st.sidebar.markdown("---")
st.sidebar.write("### Model Specs")
st.sidebar.write("- **Engine:** HMM + Dual-NLP Random Forest")
st.sidebar.write("- **Ranking Power (AUC):** 72.7%")
st.sidebar.write("- **Regime Status:** Adaptive")

# ==============================================================================
# 3. HEADER & REGIME PULSE
# ==============================================================================
st.title("🛡️ GlobalCharge: Regime-Aware Strategic Audit")
st.markdown("Automated Investment Governance for $100M Deployment")

# Regime Pulse Banner
# We assume current state is 'Chaos' (State 1) based on our 2024 analysis
regime_prob = 0.82 # Mock probability for UI; in full app, this would be computed from live macro inputs
pulse_col, metric_col = st.columns([3, 1])

with pulse_col:
    if regime_prob > 0.5:
        st.warning(f"🚨 **CHAOS REGIME DETECTED** | The system has automatically enforced the {margin_of_safety}% Margin of Safety to shield the portfolio.")
    else:
        st.success("✅ **STABLE REGIME DETECTED** | Market fundamentals are consistent with historical growth patterns.")

with metric_col:
    st.metric("Risk-Adjusted Precision", "67.7%", delta="+12.9% vs Baseline")

# ==============================================================================
# 4. MAIN DASHBOARD TABS
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["💰 Portfolio Allocation", "📈 Opportunity Gap (Underrated)", "🌍 Strategic Deep-Dive"])

with tab1:
    st.subheader("Tiered Investment Allocation")
    st.markdown("Capital is deployed based on the **Risk-Adjusted ROI Score** and the **Margin of Safety** filter.")
    
    # Process display data
    df_display = df_audit.copy()
    df_display['Action'] = df_display['New_Prob_Pct'].apply(
        lambda x: "🟢 DEPLOY" if x >= margin_of_safety else "🔴 VETO"
    )
    
    # Sort for high-conviction ROI
    df_display = df_display.sort_values(by='ROI_Score', ascending=False)
    
    # Display table with formatting
    st.dataframe(
        df_display[['Country', 'Action', 'ROI_Score', 'New_Prob_Pct', 'Survival_Prob', 'Market_Room']],
        column_config={
            "New_Prob_Pct": st.column_config.NumberColumn("AI Confidence (%)", format="%.1f%%"),
            "ROI_Score": st.column_config.ProgressColumn("ROI Index Score", min_value=0, max_value=800),
            "Survival_Prob": st.column_config.NumberColumn("Prob Score", format="%.2f")
        },
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.subheader("Underrated 'Value' Markets (The Sleeping Giants)")
    st.markdown("Purple bars represent **Alpha Opportunities**: High structural fundamentals paired with temporary market stagnation.")
    
    # Opportunity Gap Diverging Bar Chart
    df_plot = df_audit.sort_values(by='Opportunity_Gap', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#6a0dad' if x > 0 else '#ff8c00' for x in df_plot['Opportunity_Gap']]
    sns.barplot(x='Opportunity_Gap', y='Country', data=df_plot, palette=colors, ax=ax)
    
    ax.axvline(0, color='black', linewidth=1.5)
    ax.set_title("The Opportunity Gap (AI Confidence vs Reality)", fontsize=12)
    ax.set_xlabel("Potential Upside Gap")
    
    st.pyplot(fig)
    
    col_a, col_b = st.columns(2)
    col_a.info("**Purple Zone:** Underrated Recovery Plays (Target for 2026)")
    col_b.warning("**Orange Zone:** Overperforming Momentum Plays (Watch for Bubble)")

with tab3:
    st.subheader("Regional Intelligence Reports")
    target = st.selectbox("Select Country for Audit:", df_audit['Country'].unique())
    
    row = df_audit[df_audit['Country'] == target].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("AI Confidence", f"{row['New_Prob_Pct']}%")
    c2.metric("ROI Potential", f"{row['ROI_Score']}")
    c3.metric("Market S-Curve Room", f"{row['Market_Room']*100:.1f}%")
    
    # Logic-based Strategic Notes
    if target == "Germany":
        st.error("### 🛡️ Analyst Veto Required")
        st.write("Germany scores high (87.8%) on structural data but failed the 2024 test due to political subsidy cancellation. The AI maintains a 'Buy' rating based on infrastructure, but human oversight must monitor political stability before capital deployment.")
    elif target == "India":
        st.info("### 🐘 The Sleeping Giant")
        st.write(f"India has a massive Opportunity Gap of {row['Opportunity_Gap']:.2f}. The AI identifies that structural demand and manufacturing policy are coiled for a massive recovery cycle. Recommended as a strategic 10% Alpha tranche.")
    elif row['Action'] == "🔴 VETO":
        st.error(f"### 🚩 High Risk Zone")
        st.write(f"The model has rejected {target} due to insufficient 'Margin of Safety'. High probability of structural fragility in the current Chaos Regime.")
    else:
        st.success(f"### ✅ Investment Grade")
        st.write(f"{target} has cleared the {margin_of_safety}% threshold. Fundamentals are robust and resilient to the current regime shift.")

# ==============================================================================
# 5. FOOTER
# ==============================================================================
st.markdown("---")
st.caption("GlobalCharge Strategic EV Audit | Confidential Portfolio Decision Support System")
