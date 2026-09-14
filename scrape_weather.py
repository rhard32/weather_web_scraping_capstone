
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import sqlite3

# Configure browser user agent

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/152.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=service,
    options=options
)



driver.get("https://www.timeanddate.com/weather/")


weather_table = driver.find_element(
     By.CSS_SELECTOR,
     "table.zebra.fw.tb-theme"
)
print("Weather table found")

rows = weather_table.find_elements(By.TAG_NAME, "tr")

print("Number of rows found:", len(rows))


weather_data = []

for row in rows[1:]:
    row_cells = row.find_elements(By.TAG_NAME, "td")

    for i in range(0, len(row_cells), 4):
        city = row_cells[i].text
        local_time = row_cells[i + 1].text

        weather_imgs = row_cells[i + 2].find_elements(By.TAG_NAME, "img")

        if weather_imgs:
            condition = weather_imgs[0].get_attribute("alt")
        else:
            condition = "Unknown"
            

        temperature = row_cells[i + 3].text

        weather_data.append({
            "City": city,
            "Local Time": local_time,
            "Condition": condition,
            "Temperature": temperature
        })

        if len(weather_data) >= 15:
          break
        

    if len(weather_data) >= 15:
        break

print("Number of cities scraped:", len(weather_data))


raw_df = pd.DataFrame(weather_data)

raw_df.to_csv("weather_data_raw.csv", index=False)

df = raw_df.copy()


print("\nBefore Cleaning")
print(df.head())

df.info()
print("Duplicate rows:", df.duplicated().sum())
print(df[df.duplicated(keep=False)])
df = df[df["City"].str.strip() !=""].reset_index(drop=True)

print("Rows after removing empty cities:", len(df))

df["City"] = df["City"].str.replace("*", "", regex=False).str.strip()
print(df["City"].head())

df["Temperature"] = (
        df["Temperature"]
    .str.replace("°F", "", regex=False)
    .str.strip()
    .astype(int)
)

print(df["Temperature"].head())
print(df["Temperature"].dtype)

print("\nAfter cleaning:")
print(df.head())

average_temperature = df["Temperature"].mean()

print(f"Average temperature: {average_temperature:.1f} °F")

hottest_city = df.loc[df["Temperature"].idxmax()]
coolest_city = df.loc[df["Temperature"].idxmin()]

print(f"Hottest city: {hottest_city['City']} at {hottest_city['Temperature']} °F")
print(f"Coolest city: {coolest_city['City']} at {coolest_city['Temperature']} °F")



df.to_csv("weather_data_clean.csv", index=False)

print("Cleaned weather data saved to weather_data_clean.csv")

conn = sqlite3.connect("weather_data.db")
raw_df.to_sql("raw_weather", conn, if_exists="replace", index=False)

df.to_sql("clean_weather", conn, if_exists="replace", index=False)
conn.close()

print("Raw and cleaned weather data saved to weather_data.db")

driver.quit()