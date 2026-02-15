import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

# --- ASSET LOADING ---
@st.cache_data
def load_data():
    # Load your exported CSV
    df = pd.read_csv('war_room_audit_2025.csv')
    return df

df_audit = load_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.title("Audit Controls")
# This slider dynamically drives the 'Action' logic
margin = st.sidebar.slider("Margin of Safety (%)", 50, 95, 78)

# --- APP LOGIC: Calculate Action Live ---
# This ensures 'Action' is ALWAYS present in the dataframe used by the app
df_audit['Current_Action'] = df_audit['New_Prob_Pct'].apply(
    lambda x: "🟢 DEPLOY" if x >= margin else "🔴 VETO"
)

# --- UI HEADER ---
st.set_page_config(page_title="GlobalCharge Audit", layout="wide")
st.title("🛡️ GlobalCharge: Regime-Aware Strategic Audit")
st.markdown("---")

# --- THE WORLD MAP (RESTORED) ---
st.subheader("Global Risk Map")
fig = px.choropleth(
    df_audit, 
    locations="Country", 
    locationmode='country names',
    color="New_Prob_Pct", 
    hover_name="Country",
    color_continuous_scale="RdYlGn",
    range_color=[50, 100],
    labels={'New_Prob_Pct': 'AI Confidence %'}
)
fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# --- TABS ---
tab1, tab2 = st.tabs(["💰 Investment Tiers", "🌍 Market Deep-Dive"])

with tab1:
    st.write("### Portfolio Allocation Rankings")
    # Displaying the table with the live 'Current_Action' column
    display_df = df_audit[['Country', 'Current_Action', 'ROI_Score', 'New_Prob_Pct']].sort_values('ROI_Score', ascending=False)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    target = st.selectbox("Select Country for Audit:", df_audit['Country'].unique())
    # Locate the specific row for the selected country
    row = df_audit[df_audit['Country'] == target].iloc[0]
    
    # Logic Fix: Use the live calculated action to avoid KeyError
    current_status = "🟢 DEPLOY" if row['New_Prob_Pct'] >= margin else "🔴 VETO"
    
    c1, c2, c3 = st.columns(3)
    c1.metric("AI Confidence", f"{row['New_Prob_Pct']}%")
    c2.metric("Decision Status", current_status)
    c3.metric("ROI Score", f"{row['ROI_Score']}")

    st.markdown("---")
    # Strategic Deep-Dive Notes
    if target == "Germany":
        st.error("### 🛡️ Analyst Veto Required")
        st.write("Germany scores high (87.8%) on structural data but failed the 2024 test due to political subsidy cancellation. Use human oversight for final deployment.")
    elif target == "India":
        st.info("### 🐘 The Sleeping Giant")
        st.write(f"India has a massive Opportunity Gap of {row['Opportunity_Gap']:.2f}. The AI identifies that structural demand is coiled for a recovery cycle.")
    elif current_status == "🔴 VETO":
        st.error(f"### 🚩 High Risk: {target} has been vetoed by the {margin}% Margin of Safety.")
    else:
        st.success(f"### ✅ Investment Grade: {target} cleared the safety threshold.")
