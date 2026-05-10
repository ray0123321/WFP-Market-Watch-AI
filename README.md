# 🌾 WFP Market Watch: AI Food Price Predictor (Pakistan)

[![SDG 2: Zero Hunger](https://img.shields.io/badge/SDG-2:%20Zero%20Hunger-orange)](https://sdgs.un.org/goals/goal2)
[![Python](https://img.shields.io/badge/Backend-Python%20%7C%20FastAPI-blue)](https://fastapi.tiangolo.com/)
[![Flutter](https://img.shields.io/badge/Frontend-Flutter-cyan)](https://flutter.dev/)

A professional-grade Data Science project.
This system monitors and predicts food prices across major markets in Pakistan to support the UN Sustainable Development Goal (SDG) 2: **Zero Hunger**.

---

## 🌐 Live Demos
Experience the system live on the internet:
- **📱 Mobile App (Flutter)**: [Launch App](https://huggingface.co/spaces/RayRay333/wfp-market-app)
- **📊 Data Dashboard (Streamlit)**: [Launch Dashboard](https://huggingface.co/spaces/RayRay333/wfp-market-dashboard)

---

## 🚀 Key Features
- **AI-Powered Predictions**: Uses an **XGBoost** model with **99.18% accuracy** to forecast future prices of essential commodities.
- **Dual Frontend Experience**:
  - **Premium Mobile App**: Built with Flutter for a cute, responsive, and modern user experience.
  - **Data Dashboard**: Built with Streamlit for deep exploratory data analysis (EDA).
- **Market Context**: Real-time insights into regional price trends across Karachi, Lahore, Quetta, Peshawar, and more.
- **Robust Backend**: A FastAPI server that handles model inference and data lookups.

---

## 📊 Model Performance
Our model was trained on the official **World Food Programme (WFP)** dataset.
- **R-Squared Accuracy**: 99.18%
- **Mean Absolute Error (MAE)**: PKR 6.37
- **Root Mean Squared Error (RMSE)**: PKR 19.47

---

## 🛠️ Technology Stack
- **Languages**: Python (Logic), Dart (Mobile), HTML/CSS (Web)
- **ML Frameworks**: XGBoost, Scikit-Learn, Pandas, NumPy
- **Application Layer**: FastAPI (API), Streamlit (Dashboard), Flutter (Mobile UI)
- **Visualization**: Matplotlib, Seaborn

---

## 📂 Project Structure
```text
├── app.py                      # Main Streamlit Dashboard
├── main.py                     # FastAPI Backend Server
├── mobile_app/                 # Full Flutter Mobile Project
├── market_watch_model.pkl      # Trained XGBoost Model
├── city_mappings.json          # Target Encoding for Cities
├── commodity_mappings.json     # Target Encoding for Commodities
└── feature_engineered_dataset.csv # Processed Data Source
```

---

## 💻 How to Run

### 1. Setup Environment
```bash
pip install streamlit pandas joblib xgboost fastapi uvicorn
```

### 2. Run the Streamlit Dashboard
```bash
streamlit run app.py
```

### 3. Run the Flutter Mobile App (via Chrome)
First, start the Backend Server:
```bash
python main.py
```
Then, launch the app:
```bash
cd mobile_app
flutter run -d chrome
```

---

---
*Developed with ❤️ for a Hunger-Free Pakistan.*
