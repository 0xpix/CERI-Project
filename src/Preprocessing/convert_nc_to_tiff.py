import os
import subprocess
import argparse

def find_input_file(input_dir, year):
    # List of possible file name patterns
    patterns = [
        f"ESACCI-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.0.7cds.nc",
        f"C3S-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.1.1.nc"
    ]
    
    for pattern in patterns:
        input_file = os.path.join(input_dir, pattern)
        if os.path.exists(input_file):
            return input_file
    
    return None

def main(start_year, end_year, subdataset):
    # Directory containing the NetCDF files
    input_dir = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\nc"
    # Directory to save the output GeoTIFF files
    output_dir = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the CRS you want to assign. Replace 'EPSG:XXXX' with the correct EPSG code.
    crs = "EPSG:4326"  # Example for WGS 84

    # Iterate over each year and process the corresponding NetCDF file
    for year in range(start_year, end_year + 1):
        input_file = find_input_file(input_dir, year)
        if input_file is None:
            print(f"Warning: No file found for year {year}")
            continue
        
        output_file = os.path.join(output_dir, f"LULC_{year}_{subdataset}.tiff")

        # GDAL translate command with CRS definition
        cmd_translate = [
            "gdal_translate",
            "-of", "GTiff",
            "-a_srs", crs,
            f'NETCDF:"{input_file}":{subdataset}',
            output_file
        ]

        # Execute the translate command
        subprocess.run(cmd_translate, check=True)

        print(f"Successfully converted for the {year} with CRS {crs} and subdataset {subdataset}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert NetCDF to GeoTIFF with specified year range and subdataset.')
    parser.add_argument('--subdataset', type=str, required=True, help='Subdataset to extract (e.g., lccs_class).')
    parser.add_argument('--year', type=int, nargs=2, required=True, help='Start and end year (inclusive).')

    args = parser.parse_args()
    subdataset = args.subdataset
    start_year, end_year = args.year

    main(start_year, end_year, subdataset)