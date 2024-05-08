# ================================
# Importing Libraries
# ================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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