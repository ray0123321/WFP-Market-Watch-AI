from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="WFP Market Watch API")

# Enable CORS for Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Variables for Resources
MODEL = None
CITY_MAP = None
COMMODITY_MAP = None
LATEST_CONTEXT = None

@app.on_event("startup")
async def load_resources():
    global MODEL, CITY_MAP, COMMODITY_MAP, LATEST_CONTEXT
    try:
        MODEL = joblib.load('market_watch_model.pkl')
        with open('city_mappings.json', 'r') as f:
            CITY_MAP = json.load(f)
        with open('commodity_mappings.json', 'r') as f:
            COMMODITY_MAP = json.load(f)
        
        df = pd.read_csv('feature_engineered_dataset.csv')
        df['date'] = pd.to_datetime(df['date'])
        LATEST_CONTEXT = df.sort_values('date').groupby(['admin2', 'commodity']).tail(1)
        print("Backend Resources Loaded Successfully")
    except Exception as e:
        print(f"Error loading resources: {e}")

class PredictionRequest(BaseModel):
    city: str
    commodity: str
    year: int
    month: int

@app.get("/metadata")
async def get_metadata():
    if CITY_MAP is None:
        raise HTTPException(status_code=503, detail="Resources not loaded")
    return {
        "cities": sorted(list(CITY_MAP.keys())),
        "commodities": sorted(list(COMMODITY_MAP.keys()))
    }

@app.post("/predict")
async def predict(req: PredictionRequest):
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # 1. Get Historical Context
    context = LATEST_CONTEXT[(LATEST_CONTEXT['admin2'] == req.city) & 
                            (LATEST_CONTEXT['commodity'] == req.commodity)]
    
    if context.empty:
        # Fallbacks
        lag1, lag2, rolling_mean, rolling_std, usdprice = 200.0, 200.0, 200.0, 10.0, 0.7
    else:
        lag1 = context['price'].iloc[0]
        lag2 = context['lag1'].iloc[0]
        rolling_mean = context['rolling_mean_3'].iloc[0]
        rolling_std = context['rolling_std_3'].iloc[0]
        usdprice = context['usdprice'].iloc[0]

    # 2. Feature Preparation
    month_sin = np.sin(2 * np.pi * req.month / 12.0)
    month_cos = np.cos(2 * np.pi * req.month / 12.0)
    city_info = CITY_MAP[req.city]
    comm_info = COMMODITY_MAP[req.commodity]
    
    features = pd.DataFrame([{
        'market_id': 0,
        'latitude': city_info['latitude'],
        'longitude': city_info['longitude'],
        'commodity_id': comm_info['commodity_id'],
        'usdprice': usdprice,
        'year': req.year,
        'month': req.month,
        'month_sin': month_sin,
        'month_cos': month_cos,
        'implied_exchange_rate': lag1 / (usdprice + 1e-9),
        'lag1': lag1,
        'lag2': lag2,
        'rolling_mean_3': rolling_mean,
        'rolling_std_3': rolling_std,
        'city_target_encoded': city_info['city_target_encoded'],
        'commodity_target_encoded': comm_info['commodity_target_encoded']
    }])

    # 3. Inference
    prediction = MODEL.predict(features)[0]
    
    return {
        "city": req.city,
        "commodity": req.commodity,
        "predicted_price": float(round(prediction, 2)),
        "currency": "PKR",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
