# ================================
# Importing Libraries
# ================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from bs4 import BeautifulSoup


# ==============================
# Data Preprocessing Functions
# ==============================
def plot_disaster_frequency(data, disaster_filter):
    # Extract year from date if there is no column Year
    if 'Year' not in data.columns:
        # Check for both cases: YYYY/MM and YYYY/MM/DD
        if data['Date'].str.contains('/').any():
            data['Year'] = pd.to_datetime(data['Date'], format='%Y/%m').dt.year
        else:
            data['Year'] = pd.to_datetime(data['Date'], format='%Y').dt.year

    # Group by Year and Disaster Type and count frequency
    disaster_counts = data.groupby(['Year', 'Disaster type']).size().reset_index(name='Frequency')

    # Filter the data
    filtered_data = disaster_counts[disaster_counts['Disaster type'] == disaster_filter].reset_index(drop=True)

    plt.figure(figsize=(16, 6))
    # Create a bar plot for the filtered disaster
    plt.bar(filtered_data['Year'].astype(str), filtered_data['Frequency'], color='skyblue', align='center')
    plt.xlabel('Year')
    plt.ylabel('Frequency of Disasters')
    plt.title(f'{disaster_filter} Frequency Over the Years')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.show()
    
def compare_disaster_frequency(data1, data2, disaster_filter):
    # Extract year from date if there is no column Year in data1
    if 'Year' not in data1.columns:
        # Check for both cases: YYYY/MM and YYYY/MM/DD
        if data1['Date'].str.contains('/').any():
            data1['Year'] = pd.to_datetime(data1['Date'], format='%Y/%m').dt.year
        else:
            data1['Year'] = pd.to_datetime(data1['Date'], format='%Y').dt.year

    # Extract year from date if there is no column Year in data2
    if 'Year' not in data2.columns:
        # Check for both cases: YYYY/MM and YYYY/MM/DD
        if data2['Date'].str.contains('/').any():
            data2['Year'] = pd.to_datetime(data2['Date'], format='%Y/%m').dt.year
        else:
            data2['Year'] = pd.to_datetime(data2['Date'], format='%Y').dt.year

    # Group by Year and Disaster Type and count frequency for data1
    disaster_counts1 = data1.groupby(['Year', 'Disaster type']).size().reset_index(name='Frequency')

    # Group by Year and Disaster Type and count frequency for data2
    disaster_counts2 = data2.groupby(['Year', 'Disaster type']).size().reset_index(name='Frequency')

    # Filter the data for data1
    filtered_data1 = disaster_counts1[disaster_counts1['Disaster type'] == disaster_filter].reset_index(drop=True)

    # Filter the data for data2
    filtered_data2 = disaster_counts2[disaster_counts2['Disaster type'] == disaster_filter].reset_index(drop=True)

    plt.figure(figsize=(16, 6))
    # Create a bar plot for data1
    plt.bar(filtered_data1['Year'].astype(str), filtered_data1['Frequency'], color='skyblue', align='center', label='Data 1')
    # Create a bar plot for data2
    plt.bar(filtered_data2['Year'].astype(str), filtered_data2['Frequency'], color='orange', align='center', label='Data 2')
    plt.xlabel('Year')
    plt.ylabel('Frequency of Disasters')
    plt.title(f'{disaster_filter} Frequency Comparison')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.legend()
    plt.show()

# Function to set color for each feature based on disaster type
def set_color(feature):
    key = feature.get(feature_column)
    color = color_palette.get(key, "black")  # default to black if type not found
    return feature.set('color', color)
        


