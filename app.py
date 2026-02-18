import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from utils import (
    get_current_weather,
    get_historical_weather,
    get_forecast_weather,
    clean_current_weather,
    clean_historical_weather,
    clean_forecast_weather
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# ---------------- CACHE FUNCTIONS ----------------
@st.cache_data(ttl=600)
def cached_current_weather(city):
    return get_current_weather(city)

@st.cache_data(ttl=3600)
def cached_historical_weather(city, start_date, end_date):
    return get_historical_weather(city, start_date, end_date)

@st.cache_data(ttl=1800)
def cached_forecast_weather(city):
    return get_forecast_weather(city)

# ---------------- MAIN APP ----------------
st.title("🌍 Weather Analytics Dashboard")
st.caption("📌 Built using OpenWeather API + VisualCrossing API | Professional Weather Monitoring System")

os.makedirs("data", exist_ok=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙ Dashboard Controls")

city = st.sidebar.text_input("🌍 Enter City Name")
safe_city = city.replace(" ", "_").lower() if city else ""

refresh = st.sidebar.button("🔄 Refresh Data")

if refresh:
    st.cache_data.clear()
    st.sidebar.success("Cache cleared successfully!")

st.sidebar.markdown("---")
st.sidebar.info("💡 Example: Bengaluru, Chennai, Delhi, Mumbai")

# ---------------- TABS UI ----------------
tab1, tab2, tab3 = st.tabs(["📍 Current Weather", "📅 Historical Weather", "⛅ Forecast Weather"])


# ==========================================================
# 📍 CURRENT WEATHER TAB
# ==========================================================
with tab1:
    st.subheader("📍 Current Weather Overview")

    if st.button("✅ Fetch Current Weather"):
        if city == "":
            st.warning("⚠ Please enter a city name in sidebar.")
        else:
            data = cached_current_weather(city)
            weather = clean_current_weather(data)

            if "error" in weather:
                st.error(weather["error"])
            else:
                st.success(f"🌍 Live Weather Report for {weather['city']}")

                # Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("🌡 Temperature (°C)", weather["temp"])
                col2.metric("💧 Humidity (%)", weather["humidity"])
                col3.metric("☁ Condition", weather["condition"].title())

                st.markdown("---")

                # Visualisation using bar chart
                st.markdown("### 📊 Weather Summary Chart")
                chart_df = pd.DataFrame({
                    "Category": ["Temperature", "Humidity"],
                    "Value": [weather["temp"], weather["humidity"]]
                })

                st.bar_chart(chart_df.set_index("Category"))

                st.markdown("---")

                # Download section
                st.markdown("### 📥 Download Current Weather Data")
                colA, colB = st.columns(2)

                with colA:
                    st.download_button(
                        "⬇ Download JSON",
                        json.dumps(weather, indent=4),
                        file_name=f"{safe_city}_current_weather.json",
                        mime="application/json"
                    )

                with colB:
                    st.write("📌 Data will also be saved automatically in your folder.")

                # Save JSON
                filename = f"data/{safe_city}_current_weather.json"
                with open(filename, "w") as file:
                    json.dump(weather, file, indent=4)

                st.info(f"✅ Saved in: {filename}")

                # Raw JSON view
                with st.expander("📂 View Raw API JSON Response"):
                    st.json(data)


# ==========================================================
# 📅 HISTORICAL WEATHER TAB
# ==========================================================
with tab2:
    st.subheader("📅 Historical Weather Analysis")

    col1, col2 = st.columns(2)
    start_date = col1.date_input("📌 Start Date")
    end_date = col2.date_input("📌 End Date")

    if st.button("✅ Fetch Historical Weather"):
        if city == "":
            st.warning("⚠ Please enter a city name in sidebar.")

        elif start_date > end_date:
            st.error("❌ Start date must be before End date.")

        else:
            history_data = cached_historical_weather(city, start_date, end_date)
            cleaned_history = clean_historical_weather(history_data)

            if "error" in cleaned_history:
                st.error(cleaned_history["error"])
                st.write(history_data)

            else:
                st.success(f"📅 Historical Weather Data for {city}")

                df = pd.DataFrame(cleaned_history)

                st.markdown("### 📋 Historical Weather Table")
                st.dataframe(df, use_container_width=True)

                st.markdown("---")

                st.markdown("### 📈 Temperature Trend (Line Chart)")
                st.line_chart(df.set_index("date")["temp"])

                st.markdown("### 📉 Humidity Trend (Area Chart)")
                st.area_chart(df.set_index("date")["humidity"])

                st.markdown("---")

                st.markdown("### 📊 Temperature vs Humidity Comparison")
                compare_df = df[["date", "temp", "humidity"]].set_index("date")
                st.bar_chart(compare_df)

                st.markdown("---")

                # Downloads
                st.markdown("### 📥 Download Historical Weather Data")

                colA, colB = st.columns(2)

                with colA:
                    st.download_button(
                        "⬇ Download Historical JSON",
                        json.dumps(cleaned_history, indent=4),
                        file_name=f"{safe_city}_historical_weather.json",
                        mime="application/json"
                    )

                with colB:
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "⬇ Download Historical CSV",
                        csv,
                        file_name=f"{safe_city}_historical_weather.csv",
                        mime="text/csv"
                    )

                # Save JSON
                filename = f"data/{safe_city}_historical_weather.json"
                with open(filename, "w") as file:
                    json.dump(cleaned_history, file, indent=4)

                st.info(f"✅ Saved in: {filename}")

                with st.expander("📂 View Raw API JSON Response"):
                    st.json(history_data)


# ==========================================================
# ⛅ FORECAST WEATHER TAB
# ==========================================================
with tab3:
    st.subheader("⛅ Forecast Weather Prediction")

    if st.button("✅ Fetch Forecast Weather"):
        if city == "":
            st.warning("⚠ Please enter a city name in sidebar.")
        else:
            forecast_data = cached_forecast_weather(city)
            cleaned_forecast = clean_forecast_weather(forecast_data)

            if "error" in cleaned_forecast:
                st.error(cleaned_forecast["error"])
                st.write(forecast_data)

            else:
                st.success(f"⛅ Forecast Weather for {city}")

                df_forecast = pd.DataFrame(cleaned_forecast)

                st.markdown("### 📋 Forecast Table")
                st.dataframe(df_forecast, use_container_width=True)

                st.markdown("---")

                st.markdown("### 📈 Forecast Temperature Trend")
                st.line_chart(df_forecast.set_index("datetime")["temp"])

                st.markdown("### 📉 Forecast Humidity Trend")
                st.area_chart(df_forecast.set_index("datetime")["humidity"])

                st.markdown("---")

                st.markdown("### 📊 Forecast Comparison Chart")
                compare_forecast_df = df_forecast[["datetime", "temp", "humidity"]].set_index("datetime")
                st.bar_chart(compare_forecast_df)

                st.markdown("---")

                st.markdown("### 📥 Download Forecast Data")

                st.download_button(
                    "⬇ Download Forecast JSON",
                    json.dumps(cleaned_forecast, indent=4),
                    file_name=f"{safe_city}_forecast_weather.json",
                    mime="application/json"
                )

                # Save JSON
                filename = f"data/{safe_city}_forecast_weather.json"
                with open(filename, "w") as file:
                    json.dump(cleaned_forecast, file, indent=4)

                st.info(f"✅ Saved in: {filename}")

                with st.expander("📂 View Raw API JSON Response"):
                    st.json(forecast_data)
