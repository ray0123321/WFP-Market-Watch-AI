import pandas as pd
import numpy as np
import os
import json

def run_pipeline():
    print("Starting Advanced Data Engineering Pipeline...")
    
    # 1. Load Dataset
    file_path = 'wfp_food_prices_pak (1).csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    print(f"Loaded dataset with {len(df)} rows.")
    
    # 2. Data Cleaning
    print("Cleaning data...")
    # Handle missing values
    if df.isnull().sum().sum() > 0:
        df = df.dropna()
    
    # Fix date format
    df['date'] = pd.to_datetime(df['date'])
    
    # Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Removed {initial_rows - len(df)} duplicate rows.")
    
    # Export Clean Dataset
    clean_path = 'clean_dataset.csv'
    df.to_csv(clean_path, index=False)
    print(f"Clean dataset saved to {clean_path}")
    
    # 3. ADVANCED Feature Engineering
    print("Performing Advanced Feature Engineering...")
    
    # Base Time Features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    # A. Cyclical Encoding for Month
    df['month_sin'] = np.sin(2 * np.pi * df['month']/12.0)
    df['month_cos'] = np.cos(2 * np.pi * df['month']/12.0)
    
    # B. Implied Exchange Rate Feature
    df['implied_exchange_rate'] = df['price'] / (df['usdprice'] + 1e-9)
    
    # Sort data for time-series operations
    df = df.sort_values(by=['admin2', 'commodity', 'date'])
    
    # C. Lag and Rolling Features
    grouped = df.groupby(['admin2', 'commodity'])['price']
    
    df['lag1'] = grouped.shift(1)
    df['lag2'] = grouped.shift(2)
    df['rolling_mean_3'] = grouped.rolling(window=3, min_periods=1).mean().reset_index(level=[0, 1], drop=True)
    df['rolling_std_3'] = grouped.rolling(window=3, min_periods=1).std().reset_index(level=[0, 1], drop=True)
    df['rolling_std_3'] = df['rolling_std_3'].fillna(0)
    
    # Drop rows without lags
    df = df.dropna(subset=['lag1', 'lag2'])
    
    # D. Target Encoding for Commodity and City
    city_target_means = df.groupby('admin2')['price'].mean().to_dict()
    commodity_target_means = df.groupby('commodity')['price'].mean().to_dict()
    
    df['city_target_encoded'] = df['admin2'].map(city_target_means)
    df['commodity_target_encoded'] = df['commodity'].map(commodity_target_means)
    
    # E. Save Mappings for API Integration (CRITICAL FOR MEMBER 3)
    # We also need IDs and coordinates for the API
    city_info = df.groupby('admin2').agg({
        'latitude': 'first',
        'longitude': 'first',
        'city_target_encoded': 'first'
    }).to_dict(orient='index')
    
    commodity_info = df.groupby('commodity').agg({
        'commodity_id': 'first',
        'commodity_target_encoded': 'first'
    }).to_dict(orient='index')
    
    with open('city_mappings.json', 'w') as f:
        json.dump(city_info, f)
    with open('commodity_mappings.json', 'w') as f:
        json.dump(commodity_info, f)
        
    print("Mappings saved: city_mappings.json, commodity_mappings.json")
    
    # Export Feature-Engineered Dataset
    fe_path = 'feature_engineered_dataset.csv'
    df.to_csv(fe_path, index=False)
    print(f"Advanced feature-engineered dataset saved to {fe_path} with {len(df)} rows.")
    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()
