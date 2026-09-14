import sqlite3
import pandas as pd
import streamlit as st

# Configure the Streamlit page
st.set_page_config(
    page_title="Global Weather Dashboard",
    page_icon="🌦️",
    layout="wide"
)

# Load cleaned weather data from the SQLite database
@st.cache_data
def load_data():
    with sqlite3.connect("weather_data.db") as conn:
        weather_data = pd.read_sql_query(
            "SELECT * FROM clean_weather;",
            conn
        )
    return weather_data


weather_data = load_data()

# Dashboard title and description
st.title("🌦️ Global Weather Dashboard")

st.write(
    "Explore current weather conditions and temperatures for cities "
    "included in the scraped weather dataset."
)





# Interactive filters
st.sidebar.header("Weather Filters")

selected_cities = st.sidebar.multiselect(
    "Select cities",
    options=weather_data["City"].tolist(),
    default=weather_data["City"].tolist()
)

min_temp = int(weather_data["Temperature"].min())
max_temp = int(weather_data["Temperature"].max())

temperature_range = st.sidebar.slider(
    "Temperature range (°F)",
    min_value=min_temp,
    max_value=max_temp,
    value=(min_temp, max_temp)
)

# Apply the filters
filtered_data = weather_data[
    (weather_data["City"].isin(selected_cities))
    & (weather_data["Temperature"] >= temperature_range[0])
    & (weather_data["Temperature"] <= temperature_range[1])
]

# Display filtered weather data
st.subheader("Filtered Weather Data")
st.dataframe(filtered_data, use_container_width=True)

# Visualization 1: Temperature by city
st.subheader("Temperature by City")

if not filtered_data.empty:
    temperature_chart = filtered_data.set_index("City")["Temperature"]

    st.bar_chart(
        temperature_chart,
        x_label="City",
        y_label="Temperature (°F)"
    )
else:
    st.warning("No cities match the selected filters.")

# Visualization 2: Weather condition distribution
st.subheader("Weather Conditions")

if not filtered_data.empty:
    condition_counts = (
        filtered_data["Condition"]
        .value_counts()
        .rename_axis("Condition")
        .reset_index(name="Number of Cities")
    )

    st.bar_chart(
        condition_counts,
        x="Condition",
        y="Number of Cities",
        x_label="Weather Condition",
        y_label="Number of Cities"
    )

# Visualization 3: Weather summary metrics
st.subheader("Weather Summary")

if not filtered_data.empty:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average Temperature",
            f"{filtered_data['Temperature'].mean():.1f} °F"
        )

    with col2:
        st.metric(
            "Highest Temperature",
            f"{filtered_data['Temperature'].max()} °F"
        )

    with col3:
        st.metric(
            "Lowest Temperature",
            f"{filtered_data['Temperature'].min()} °F"
        )

    st.write(
            f"The current filters include {len(filtered_data)} cities. "
            f"Temperatures range from {filtered_data['Temperature'].min()} °F "
            f"to {filtered_data['Temperature'].max()} °F, with an average "
            f"temperature of {filtered_data['Temperature'].mean():.1f} °F."
        )

