import pandas as pd
import json

# Load the Excel file
file_path = 'C:/Users/nschl/Documents/AIMS_MSc_Project_CERI/GitHub/CERI-Project/data/processed/Disasters_in_africa_2000_2018_processed.xlsx'
df = pd.read_excel(file_path)

# Ensure the columns for year and country are named correctly in the Excel file
year_column = 'Year'
country_column = 'Country'

# Group by year and get unique countries for each year
disasters_by_year = df.groupby(year_column)[country_column].apply(lambda x: list(set(x))).to_dict()

# Save the result to a JSON file
output_file = 'disasters_by_year.json'
with open(output_file, 'w') as f:
    json.dump(disasters_by_year, f, indent=4)

print(f"JSON file saved to {output_file}")
