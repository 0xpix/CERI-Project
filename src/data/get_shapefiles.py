import pandas as pd
import requests
import os
from tqdm import tqdm

# Function to get country codes from the REST Countries API
def get_country_codes():
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        country_codes = {country['name']['common']: country['cca3'] for country in data}
        print("Country codes fetched successfully.")
        return country_codes
    else:
        print(f"Failed to retrieve country codes. HTTP Status Code: {response.status_code}")
        return {}

# Function to download a file with progress bar
def download_file(url, file_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024 * 100  
    t = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(file_path, 'wb') as file:
        for data in response.iter_content(block_size):
            t.update(len(data))
            file.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR: Something went wrong during the download")
    else:
        print(f"Downloaded successfully.")

# Load the Excel file and get the list of unique countries
file_path = r'C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\GitHub\CERI-Project\data\processed\Disasters_in_africa_2000_2018_processed.xlsx'
df = pd.read_excel(file_path)
print("Excel file loaded successfully.")

# Ensure the column for country is named correctly in the Excel file
country_column = 'Country'
countries = df[country_column].unique().tolist()

# Get country codes from the API
country_codes = get_country_codes()

# Directory to save the downloaded shapefiles
output_dir = r'C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\GitHub\CERI-Project\data\shapefile\countries_shapefile'
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory created/exists.")

# Base URL for downloading shapefiles
base_url = 'https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_{country_code}_shp.zip'

for country in countries:
    country_code = country_codes.get(country)
    if country_code:
        url = base_url.format(country_code=country_code)
        file_path = os.path.join(output_dir, f'gadm41_{country_code}_shp.zip')
        print(f"\nStarting download for {country} ({country_code})...\n")
        download_file(url, file_path)
    else:
        print(f"\nCountry code for {country} not found in the dictionary.\n")
