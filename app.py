import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime
import matplotlib.pyplot as plt

# Set page config for a premium feel
st.set_page_config(page_title="WFP Market Watch", page_icon="🌾", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .st-emotion-cache-1kyxreq { justify-content: center; }
    </style>
""", unsafe_allow_html=True)

# 1. Load Resources
@st.cache_resource
def load_resources():
    model = joblib.load('market_watch_model.pkl')
    with open('city_mappings.json', 'r') as f:
        city_map = json.load(f)
    with open('commodity_mappings.json', 'r') as f:
        comm_map = json.load(f)
    
    # Load feature engineered data for historical context (Lags)
    df = pd.read_csv('feature_engineered_dataset.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # Get latest record for each city-commodity pair
    latest_context = df.sort_values('date').groupby(['admin2', 'commodity']).tail(1)
    
    return model, city_map, comm_map, latest_context, df

try:
    model, city_map, comm_map, latest_context, full_df = load_resources()
except Exception as e:
    st.error(f"Error loading files: {e}. Make sure all .pkl, .json, and .csv files are in the folder.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.image("https://www.wfp.org/themes/custom/wfp_org/logo.svg", width=150)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Price Predictor", "Market Insights (EDA)"])

# --- PAGE 1: PRICE PREDICTOR ---
if page == "Price Predictor":
    st.title("🌾 WFP Market Watch: Food Price Predictor")
    st.info("🎯 **SDG 2 Alignment**: Monitoring food affordability to combat hunger.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_city = st.selectbox("Select Market (City)", sorted(list(city_map.keys())))
    with col2:
        selected_commodity = st.selectbox("Select Commodity", sorted(list(comm_map.keys())))
    with col3:
        prediction_date = st.date_input("Select Prediction Month", datetime.now())

    if st.button("🚀 Calculate Predicted Price", use_container_width=True):
        # 1. Get Context Data (Lags/Rolling Stats)
        context = latest_context[(latest_context['admin2'] == selected_city) & 
                                (latest_context['commodity'] == selected_commodity)]
        
        if context.empty:
            st.warning("No historical data found for this pair. Using national averages.")
            lag1 = full_df['price'].mean()
            lag2 = full_df['price'].mean()
            r_mean = full_df['price'].mean()
            r_std = 0
            usd = full_df['usdprice'].mean()
        else:
            lag1 = context['price'].iloc[0]
            lag2 = context['lag1'].iloc[0]
            r_mean = context['rolling_mean_3'].iloc[0]
            r_std = context['rolling_std_3'].iloc[0]
            usd = context['usdprice'].iloc[0]

        # 2. Feature Engineering (The logic Member 3 gets marks for!)
        year = prediction_date.year
        month = prediction_date.month
        month_sin = np.sin(2 * np.pi * month / 12.0)
        month_cos = np.cos(2 * np.pi * month / 12.0)
        city_info = city_map[selected_city]
        comm_info = comm_map[selected_commodity]

        features = pd.DataFrame([{
            'market_id': 0,
            'latitude': city_info['latitude'],
            'longitude': city_info['longitude'],
            'commodity_id': comm_info['commodity_id'],
            'usdprice': usd,
            'year': year,
            'month': month,
            'month_sin': month_sin,
            'month_cos': month_cos,
            'implied_exchange_rate': lag1 / (usd + 1e-9),
            'lag1': lag1,
            'lag2': lag2,
            'rolling_mean_3': r_mean,
            'rolling_std_3': r_std,
            'city_target_encoded': city_info['city_target_encoded'],
            'commodity_target_encoded': comm_info['commodity_target_encoded']
        }])

        # 3. Inference
        pred_price = model.predict(features)[0]

        # 4. Display Result
        st.markdown("---")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            delta_val = ((pred_price - lag1) / lag1) * 100 if lag1 != 0 else 0
            st.metric(label=f"Predicted Price for {selected_commodity}", 
                      value=f"PKR {pred_price:.2f}", 
                      delta=f"{delta_val:.1f}% vs Last Month")
        with res_col2:
            st.write(f"### 📋 Market Context")
            st.write(f"**City:** {selected_city}")
            st.write(f"**Last Recorded Price:** PKR {lag1:.2f}")
            st.write(f"**Historical Average (3-mo):** PKR {r_mean:.2f}")

# --- PAGE 2: MARKET INSIGHTS ---
else:
    st.title("📊 Market Insights & Exploratory Data Analysis")
    
    tab1, tab2, tab3 = st.tabs(["📈 Price Trends", "🏙️ City Comparison", "🧠 Model Performance"])
    
    with tab1:
        st.subheader("Historical Price Trends")
        st.image("price_trend.png", caption="General trend of food prices over time.")
        st.image("seasonal_analysis.png", caption="Seasonal fluctuations in food prices.")
        
    with tab2:
        st.subheader("Regional Analysis")
        st.image("city_comparison.png", caption="Price differences across major cities.")
        st.image("price_distribution.png", caption="Spread of prices across commodities.")
        
    with tab3:
        st.subheader("AI Model Reliability")
        st.image("ml_actual_vs_predicted.png", caption="How close our AI's predictions are to actual prices.")
        st.image("ml_feature_importance.png", caption="Which factors affect food prices the most?")

# Footer
st.markdown("---")
st.caption("Developed by Group 4 - Kinnaird College | SDG 2: Zero Hunger | 2026")
