# weather_web_scraping_capstone
# Weather Web Scraping Capstone

A web scraping capstone project using Selenium, Pandas, SQLite, and Streamlit to analyze weather data from the Time and Date "Weather Around the World" website.

## Current Project Stage

This stage of the project uses Selenium to scrape weather data from the website and Pandas to clean and transform the collected data.

The scraper collects weather information for 15 cities, including:

- City
- Local time
- Weather condition
- Temperature

The project saves both the original scraped data and the cleaned data as CSV files and stores both datasets in a SQLite database.

## Files

- `scrape_weather.py` - Scrapes and cleans the weather data.
- `weather_data_raw.csv` - Raw data collected from the website.
- `weather_data_clean.csv` - Cleaned and transformed weather data.
- `requirements.txt` - Python dependencies required to run the project.
- `weather_data.db` - SQLite database containing separate tables for the raw and cleaned weather data.

## Setup

Create and activate a Python virtual environment.

Install the required dependencies:

```bash
pip install -r requirements.txt

## Future Development

A later stage of the capstone will use Streamlit to create an interactive weather dashboard.