import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import json

def evaluate_model():
    print("--- AI Model Evaluation Report ---")
    
    # 1. Load Resources
    model = joblib.load('market_watch_model.pkl')
    df = pd.read_csv('feature_engineered_dataset.csv')
    
    with open('city_mappings.json', 'r') as f:
        city_map = json.load(f)
    with open('commodity_mappings.json', 'r') as f:
        comm_map = json.load(f)

    # 2. Prepare Features
    df['date'] = pd.to_datetime(df['date'])
    df['month_sin'] = np.sin(2 * np.pi * df['date'].dt.month / 12.0)
    df['month_cos'] = np.cos(2 * np.pi * df['date'].dt.month / 12.0)
    
    # Use lag1 for implied exchange rate calculation to avoid leakage
    df['implied_exchange_rate'] = df['lag1'] / (df['usdprice'] + 1e-9)
    
    df['city_target_encoded'] = df['admin2'].map(lambda x: city_map.get(x, {}).get('city_target_encoded', 0))
    df['commodity_target_encoded'] = df['commodity'].map(lambda x: comm_map.get(x, {}).get('commodity_target_encoded', 0))
    df['latitude'] = df['admin2'].map(lambda x: city_map.get(x, {}).get('latitude', 0))
    df['longitude'] = df['admin2'].map(lambda x: city_map.get(x, {}).get('longitude', 0))
    df['commodity_id'] = df['commodity'].map(lambda x: comm_map.get(x, {}).get('commodity_id', 0))
    df['market_id'] = 0
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    feature_cols = [
        'market_id', 'latitude', 'longitude', 'commodity_id', 'usdprice', 
        'year', 'month', 'month_sin', 'month_cos', 'implied_exchange_rate', 
        'lag1', 'lag2', 'rolling_mean_3', 'rolling_std_3', 
        'city_target_encoded', 'commodity_target_encoded'
    ]

    X = df[feature_cols]
    y_true = df['price']

    # 3. Predict
    y_pred = model.predict(X)

    # 4. Calculate Metrics
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    print(f"R-Squared Accuracy: {r2:.4f} ({r2*100:.2f}%)")
    print(f"Mean Absolute Error (MAE): PKR {mae:.2f}")
    print(f"Root Mean Squared Error (RMSE): PKR {rmse:.2f}")
    print("---------------------------------------")

if __name__ == "__main__":
    evaluate_model()
