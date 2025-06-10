import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime


df = pd.read_csv('weather_data.csv')

df['Date'] = pd.to_datetime(df['Date']).dt.date

df['Temperature_C'] = df['Temperature_C'].fillna(df['Temperature_C'].mean())

Q1 = df['Temperature_C'].quantile(0.25)
Q3 = df['Temperature_C'].quantile(0.75)
IQR = Q3 - Q1
df = df[~((df['Temperature_C'] < (Q1 - 1.5 * IQR)) | (df['Temperature_C'] > (Q3 + 1.5 * IQR)))]

latest_data = (
    df.sort_values(['City', 'Date'], ascending=[True, False])
    .groupby('City')
    .first()
    .reset_index()
)

cities = latest_data['City']
today = datetime.date.today().strftime('%Y-%m-%d')
city_labels = [f"{city} ({today})" for city in cities]
temperatures = latest_data['Temperature_C']
humidity = latest_data['Humidity_%']
x = np.arange(len(cities))
width = 0.35

plt.figure(figsize=(12, 7))
bar1 = plt.bar(x - width/2, temperatures, width, label='Temperature (°C)', color='orange', edgecolor='black')
bar2 = plt.bar(x + width/2, humidity, width, label='Humidity (%)', color='skyblue', edgecolor='black')

plt.xlabel('City (Today)', fontsize=12)
plt.ylabel('Values', fontsize=12)
plt.title(f"Latest available Temperature and Humidity per City", fontsize=15, fontweight='bold')
plt.xticks(x, city_labels, rotation=30, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.legend(fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.7)

for rect in bar1 + bar2:
    height = rect.get_height()
    plt.annotate(f'{height:.1f}',
                 xy=(rect.get_x() + rect.get_width() / 2, height),
                 xytext=(0, 3),  # 3 points vertical offset
                 textcoords="offset points",
                 ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(df['Temperature_C'], bins=15, color='orange', edgecolor='black', alpha=0.8)
plt.xlabel('Temperature (°C)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Temperature Distribution (All Cities, Cleaned Data)', fontsize=15, fontweight='bold')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
