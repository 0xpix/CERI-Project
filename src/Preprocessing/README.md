# Geospatial Data Processing and Cleaning

This repository contains various scripts to manage, process, and clean geospatial data, including tasks such as unzipping files, clipping rasters using shapefiles, converting NetCDF files to GeoTIFF with color palettes, and cleaning data for analysis. Below is a detailed explanation of each script and how to run them.

## Installation and Setup
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Scripts
Each script can be run from the command line with appropriate arguments as shown in the usage sections above. Ensure all necessary files and directories are in place before running the scripts.

## Dependencies
- Python 3.x
- GDAL
- pandas
- requests
- argparse
- os
- subprocess
- fnmatch

## Raster's scripts

### 1. `convert_nc_to_colored_tiff.py`
This script converts NetCDF files to GeoTIFF format, applies a color palette, and organizes the output files by year.

#### Functions:
- `find_input_file(input_dir, year)`: Finds the input NetCDF file for a specific year.
- `apply_color_palette(input_tiff, clr_file, output_tiff)`: Applies a color palette to the TIFF file using GDAL.

#### Usage:
```sh
python convert_nc_to_colored_tiff.py --subdataset <subdataset> --year <start_year> <end_year> --clr_file <path_to_clr_file>
```

### 2. `unzip_and_organize.py`
This script unzips files in a given folder and organizes them into subfolders named after the country name, extracted from the zip file's name.

#### Functions:
- `extract_country_code(zip_filename)`: Extracts the country code from the zip file's name.
- `get_country_name(country_code)`: Fetches the country name using the `restcountries.com` API.
- `unzip_files_in_folder(zip_folder_path, output_folder_path)`: Unzips all files in the specified folder and organizes them by country name.

#### Usage:
```sh
python unzip_and_organize.py --input <path_to_zip_files> --output <path_to_output_folder>
```

### 3. `clip_raster.py`
This script clips raster files using specified shapefiles and organizes the output files by year.

#### Functions:
- `clip_raster_with_shapefile(raster_path, shapefile_path, output_path)`: Clips the raster using GDAL.
- `find_shapefiles(directory, pattern)`: Finds shapefiles matching a specified pattern.
- `find_input_file(input_dir, year)`: Finds the input raster file for a specific year.

#### Usage:
```sh
python clip_raster.py --input <raster_files_directory> --shapefiles <shapefiles_directory> --output <output_directory> --start_year <start_year> --end_year <end_year>
```


## EDA

### 1. `cleaning.py`
This script provides functions to clean and preprocess a dataset, including selecting and renaming columns, filtering for African countries and years, and correcting date formats.

#### Functions:
- `select_and_rename_columns(data, selected_columns, new_column_names)`: Selects and optionally renames specific columns from a DataFrame.
- `filter_african_disasters(data, years_range, capitalize)`: Filters the dataset for African countries and specified years, and optionally capitalizes disaster types.
- `correct_date_format(date_str)`: Ensures dates are in `yyyy-mm-dd` format with leading zeros.

#### Example Usage in a Python script:
```python
import pandas as pd
from cleaning import select_and_rename_columns, filter_african_disasters, correct_date_format

# Load data
data = pd.read_csv('path_to_data.csv')

# Select and rename columns
selected_data = select_and_rename_columns(data, ['Country', 'Year', 'Disaster type'], ['Country', 'Year', 'Type'])

# Filter for African disasters in specific years
filtered_data = filter_african_disasters(selected_data, range(2000, 2020), capitalize=True)

# Correct date format
filtered_data['Date'] = filtered_data['Date'].apply(correct_date_format)
```
