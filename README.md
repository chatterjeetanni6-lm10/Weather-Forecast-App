# Weather Forecast Dashboard

A real-time weather forecasting application built with Python, Streamlit, and the Open-Meteo API.

## 🚀 Live Demo
**[Try the app here](https://weather-forecast-app-YOUR-USERNAME.streamlit.app/)**

## 📊 Project Overview
This project analyzes and visualizes weather patterns using real-time weather data. It provides 7-day forecasts, temperature statistics, and interactive visualizations for any city worldwide.

## ✨ Features
✅ Real-time weather forecasts (7 days)  
✅ Temperature statistics (mean, median, correlation)  
✅ Weather condition distribution analysis  
✅ Interactive Matplotlib visualizations  
✅ City search with geolocation  
✅ Detailed forecast tables  

## 🛠️ Technologies Used
- **Python 3** - Core language
- **Streamlit** - Web app framework
- **Requests** - API integration
- **Matplotlib** - Data visualization
- **NumPy** - Numerical analysis
- **Open-Meteo API** - Weather data source

## 📁 Files in Repository
- `weather_app.py` - Streamlit application (deployed)
- `Weather_Forecast_Using_Python.ipynb` - Original Jupyter notebook with full analysis
- `WEATHER_FORECAST_USING_PYTHON_AND_OPEN_METEO_API_2_.pdf` - Research presentation
- `requirements.txt` - Python dependencies
- `README.md` - This file

## 📈 How It Works
1. User enters a city name in the sidebar
2. App fetches coordinates using geocoding API
3. Retrieves 7-day weather forecast from Open-Meteo
4. Calculates temperature statistics and correlations
5. Displays interactive graphs and data tables

## 💡 Key Insights from Analysis
- Temperature mean/median calculations across forecast period
- Correlation analysis between max and min temperatures
- Weather condition frequency distribution
- Multi-city comparative analysis (extended research)
- Power BI dashboard for 30+ Indian cities

## 🔧 How to Run Locally
```bash
pip install -r requirements.txt
streamlit run weather_app.py
```

Then open: `http://localhost:8501`

## 📚 Research & Methodology
See the included PDF presentation for:
- Extended analysis methodology
- Statistical findings from 30+ cities
- Power BI dashboard insights
- Temperature trends and patterns
- Weather condition distributions

---

**Built by Sreshtha Chatterjee | St. Xavier's College, Kolkata | September 2026**
