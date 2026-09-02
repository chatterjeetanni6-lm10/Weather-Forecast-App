import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import statistics
from collections import Counter

st.set_page_config(page_title="Weather Forecast Dashboard", layout="wide")

weather_descriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

def get_coordinates(city):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "results" not in data or not data["results"]:
            return None
        
        location = data["results"][0]
        return {
            "latitude": location.get("latitude"),
            "longitude": location.get("longitude"),
            "name": location.get("name"),
            "country": location.get("country")
        }
    except Exception as e:
        st.error(f"Error fetching coordinates: {e}")
        return None

def get_weather_forecast(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if "daily" not in data:
            return None
        
        daily = data["daily"]
        return {
            "dates": daily.get("time", []),
            "max_temps": daily.get("temperature_2m_max", []),
            "min_temps": daily.get("temperature_2m_min", []),
            "weather_codes": daily.get("weathercode", [])
        }
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def plot_temperature_graph(dates, max_temps, min_temps):
    fig, ax = plt.subplots(figsize=(12, 5))
    
    date_objs = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    
    ax.plot(date_objs, max_temps, marker='o', label='Max Temp (°C)', color='#FF6B6B', linewidth=2, markersize=8)
    ax.plot(date_objs, min_temps, marker='o', label='Min Temp (°C)', color='#4ECDC4', linewidth=2, markersize=8)
    
    ax.fill_between(date_objs, max_temps, min_temps, alpha=0.2, color='#95E1D3')
    
    ax.set_title('Temperature Forecast', fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Temperature (°C)', fontsize=12)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

def plot_weather_conditions(weather_codes):
    descriptions = [weather_descriptions.get(code, "Unknown") for code in weather_codes]
    condition_counts = Counter(descriptions)
    
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2']
    
    wedges, texts, autotexts = ax.pie(
        condition_counts.values(),
        labels=condition_counts.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=colors[:len(condition_counts)]
    )
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Weather Condition Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig

def calculate_stats(max_temps, min_temps, weather_codes):
    stats = {
        "max_mean": round(statistics.mean(max_temps), 2),
        "max_median": round(statistics.median(max_temps), 2),
        "min_mean": round(statistics.mean(min_temps), 2),
        "min_median": round(statistics.median(min_temps), 2),
        "correlation": round(np.corrcoef(max_temps, min_temps)[0, 1], 3)
    }
    return stats

st.title("🌤️ Weather Forecast Dashboard")
st.markdown("Get real-time weather forecasts for any city worldwide using Open-Meteo API")

with st.sidebar:
    st.header("Search Location")
    city_input = st.text_input("Enter city name:", placeholder="e.g., Kolkata, Delhi, Mumbai")
    search_button = st.button("Get Weather", use_container_width=True)

if search_button and city_input:
    with st.spinner(f"Fetching weather data for {city_input}..."):
        location = get_coordinates(city_input)
        
        if location:
            lat, lon = location["latitude"], location["longitude"]
            city_name = location["name"]
            country = location["country"]
            
            st.success(f"✅ Location found: **{city_name}, {country}**")
            
            forecast = get_weather_forecast(lat, lon)
            
            if forecast:
                dates = forecast["dates"]
                max_temps = forecast["max_temps"]
                min_temps = forecast["min_temps"]
                weather_codes = forecast["weather_codes"]
                
                st.subheader("📋 Next 2 Days Forecast")
                col1, col2 = st.columns(2)
                
                for idx in range(min(2, len(dates))):
                    with col1 if idx == 0 else col2:
                        date_str = datetime.strptime(dates[idx], "%Y-%m-%d").strftime("%A, %b %d")
                        condition = weather_descriptions.get(weather_codes[idx], "Unknown")
                        
                        st.metric(
                            label=f"📅 {date_str}",
                            value=f"{max_temps[idx]}°C",
                            delta=f"Min: {min_temps[idx]}°C"
                        )
                        st.info(f"**Condition:** {condition}")
                
                st.subheader("📊 Temperature Statistics")
                stats = calculate_stats(max_temps, min_temps, weather_codes)
                
                stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)
                
                with stat_col1:
                    st.metric("Max Temp Mean", f"{stats['max_mean']}°C")
                with stat_col2:
                    st.metric("Max Temp Median", f"{stats['max_median']}°C")
                with stat_col3:
                    st.metric("Min Temp Mean", f"{stats['min_mean']}°C")
                with stat_col4:
                    st.metric("Min Temp Median", f"{stats['min_median']}°C")
                with stat_col5:
                    st.metric("Correlation", f"{stats['correlation']}")
                
                st.subheader("📈 Visualizations")
                chart_col1, chart_col2 = st.columns([2, 1])
                
                with chart_col1:
                    st.pyplot(plot_temperature_graph(dates, max_temps, min_temps))
                
                with chart_col2:
                    st.pyplot(plot_weather_conditions(weather_codes))
                
                st.subheader("📅 Detailed Forecast")
                forecast_data = {
                    "Date": [datetime.strptime(d, "%Y-%m-%d").strftime("%Y-%m-%d") for d in dates],
                    "Max Temp (°C)": max_temps,
                    "Min Temp (°C)": min_temps,
                    "Condition": [weather_descriptions.get(code, "Unknown") for code in weather_codes]
                }
                st.dataframe(forecast_data, use_container_width=True, hide_index=True)
        else:
            st.error(f"❌ City '{city_input}' not found. Please try another city.")
elif not search_button:
    st.info("👈 Enter a city name in the sidebar and click 'Get Weather' to start!")
    st.markdown("""
    ### 🌍 Try these example cities:
    - Kolkata, India
    - Delhi, India
    - Mumbai, India
    - New York, USA
    - London, UK
    - Tokyo, Japan
    """)

# Set page config
st.set_page_config(page_title="Weather Forecast Dashboard", layout="wide", initial_sidebar_state="expanded")
    st.markdown("""
    ### 🌍 Try these example cities:
    - Kolkata, India
    - Delhi, India
    - Mumbai, India
    - New York, USA
    - London, UK
    - Tokyo, Japan
    """)
