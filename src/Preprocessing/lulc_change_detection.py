import os
import numpy as np
from osgeo import gdal
import pandas as pd
import argparse
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Explicitly enable GDAL exceptions
gdal.UseExceptions()

def calculate_class_areas(file_path):
    dataset = gdal.Open(file_path)
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()
    
    unique, counts = np.unique(array, return_counts=True)
    class_areas = dict(zip(unique, counts))
    
    return class_areas

def calculate_percentage_change(current, previous):
    changes = {}
    for key in current:
        if key in previous:
            changes[key] = ((current[key] - previous[key]) / previous[key]) * 100
        else:
            changes[key] = 100.0  # Assuming a 100% increase if the class was not present before
    return changes

def main(start_year, end_year):
    # Directory containing the GeoTIFF files
    input_dir = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff"
    
    # List of years for which you have GeoTIFF files
    years = range(start_year, end_year + 1)

    # Dictionary to store areas for each class per year
    yearly_class_areas = {}

    for year in years:
        input_file = os.path.join(input_dir, f"LULC_{year}.tiff")
        class_areas = calculate_class_areas(input_file)
        yearly_class_areas[year] = class_areas

    # List to store percentage changes
    change_records = []

    for i in range(1, len(years)):
        current_year = years[i]
        previous_year = years[i - 1]

        current_areas = yearly_class_areas[current_year]
        previous_areas = yearly_class_areas[previous_year]

        percentage_changes = calculate_percentage_change(current_areas, previous_areas)
        for class_label, change in percentage_changes.items():
            change_records.append({'Year': current_year, 'Class': class_label, 'Percentage Change': change})

    # Convert the list to a DataFrame
    change_df = pd.DataFrame(change_records)

    # Specifically look for changes in urban class (assuming urban class label is known, e.g., 1)
    urban_changes = change_df[change_df['Class'] == 190]
    print("Urban class changes year-on-year:")
    print(urban_changes)

    # Save the DataFrame to a CSV file
    change_df.to_csv(os.path.join(input_dir, 'lulc_changes.csv'), index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform LULC change detection and calculate year-on-year percentage change.')
    parser.add_argument('--year', type=int, nargs=2, required=True, help='Start and end year (inclusive).')

    args = parser.parse_args()
    start_year, end_year = args.year

    main(start_year, end_year)