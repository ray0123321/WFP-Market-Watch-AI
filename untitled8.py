import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_best_ml_pipeline():
    print("Starting Optimized Machine Learning Pipeline...")
    
    # 1. Load the dataset
    file_path = 'feature_engineered_dataset.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return
        
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # 2. Select the technical features for training
    features = [
        'market_id', 'latitude', 'longitude', 'commodity_id', 'usdprice',
        'year', 'month', 'month_sin', 'month_cos', 'implied_exchange_rate',
        'lag1', 'lag2', 'rolling_mean_3', 'rolling_std_3',
        'city_target_encoded', 'commodity_target_encoded'
    ]
    X = df[features]
    y = df['price']
    
    # 3. Chronological Split (80% Train, 20% Test)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    print(f"Data Loaded! Training on {len(X_train)} rows, Testing on {len(X_test)} rows.")
    
    # 4. Hyperparameter Tuning for XGBoost (The Pro Move)
    print("Tuning XGBoost Hyperparameters (this may take a minute)...")
    param_grid = {
        'n_estimators': [500, 1000],
        'learning_rate': [0.01, 0.05, 0.1],
        'max_depth': [3, 5, 7],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0]
    }
    
    # TimeSeriesSplit is essential for time-series data
    tscv = TimeSeriesSplit(n_splits=3)
    
    xgb_base = xgb.XGBRegressor(random_state=42)
    xgb_search = RandomizedSearchCV(
        xgb_base, 
        param_distributions=param_grid, 
        n_iter=10, 
        cv=tscv, 
        scoring='neg_mean_absolute_error', 
        verbose=1, 
        n_jobs=-1, 
        random_state=42
    )
    xgb_search.fit(X_train, y_train)
    
    best_xgb = xgb_search.best_estimator_
    print(f"Best XGBoost Parameters: {xgb_search.best_params_}")
    
    # 5. Train Baseline: Random Forest
    print("Training Random Forest Baseline...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    # 6. Evaluation
    print("Evaluating Models...")
    xgb_preds = best_xgb.predict(X_test)
    rf_preds = rf_model.predict(X_test)
    
    results = {
        "Model": ["Random Forest", "XGBoost (Optimized)"],
        "MAE": [mean_absolute_error(y_test, rf_preds), mean_absolute_error(y_test, xgb_preds)],
        "RMSE": [np.sqrt(mean_squared_error(y_test, rf_preds)), np.sqrt(mean_squared_error(y_test, xgb_preds))]
    }
    
    results_df = pd.DataFrame(results)
    print("\n--- Model Comparison Table ---")
    print(results_df.to_string(index=False))
    
    # 7. Save Visualizations
    sns.set_theme(style="whitegrid")
    
    # A. Feature Importance Plot
    print("Saving Feature Importance Plot...")
    plt.figure(figsize=(10, 8))
    # We use plot_importance from xgb
    xgb.plot_importance(best_xgb, max_num_features=12, importance_type='weight')
    plt.title("Key Factors Driving Food Prices")
    plt.tight_layout()
    plt.savefig('ml_feature_importance.png')
    plt.close()
    
    # B. Actual vs Predicted Plot
    print("Saving Actual vs Predicted Plot...")
    plt.figure(figsize=(12, 6))
    plt.plot(y_test.values[:100], label='Real Price', color='blue', alpha=0.6, linewidth=2)
    plt.plot(xgb_preds[:100], label='Predicted Price', color='red', linestyle='--', linewidth=2)
    plt.title('How Accurate is our Model? (Actual vs Predicted)')
    plt.ylabel('Price (PKR)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('ml_actual_vs_predicted.png')
    plt.close()
    
    # 8. Save the Final Model
    joblib.dump(best_xgb, 'market_watch_model.pkl')
    print("\nFinal Model saved as 'market_watch_model.pkl'!")
    print("Plots saved: 'ml_feature_importance.png', 'ml_actual_vs_predicted.png'")

if __name__ == "__main__":
    run_best_ml_pipeline()