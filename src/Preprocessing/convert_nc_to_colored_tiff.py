import os
import subprocess
import argparse

def find_input_file(input_dir, year):
    patterns = [
        f"ESACCI-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.0.7cds.nc",
        f"C3S-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.1.1.nc"
    ]
    
    for pattern in patterns:
        input_file = os.path.join(input_dir, pattern)
        if os.path.exists(input_file):
            print(f"Input file found for year {year}")
            return input_file
    
    print(f"No input file found for year {year}.")
    return None

def main(start_year, end_year, subdataset):
    input_dir = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\nc"
    output_dir = rf"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff_{subdataset}"
    os.makedirs(output_dir, exist_ok=True)
    crs = "EPSG:4326"  # Example for WGS 84

    for year in range(start_year, end_year + 1):
        print(f"\nProcessing data for the year {year}...")
        input_file = find_input_file(input_dir, year)
        if input_file is None:
            print(f"Skipping year {year} due to missing input file.")
            continue
        
        output_file = os.path.join(output_dir, f"LULC_{year}_{subdataset}.tiff")
        if os.path.exists(output_file):
            print(f"Output file for year {year} already exists. Skipping conversion.")
            continue

        # GDAL translate command with CRS definition
        cmd_translate = [
            "gdal_translate",
            "-of", "GTiff",
            "-a_srs", crs,
            f'NETCDF:"{input_file}":{subdataset}',
            output_file
        ]

        try:
            # Execute the translate command
            print(f"Converting .nc file to .tiff file.")
            subprocess.run(cmd_translate, check=True)
            print(f"Successfully converted.")
        except subprocess.CalledProcessError as e:
            print(f"Error during gdal_translate for year {year}: {e}")
            continue
                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert NetCDF to GeoTIFF with specified year range and subdataset, and apply color palette.')
    parser.add_argument('--subdataset', type=str, required=True, help='Subdataset to extract (e.g., lccs_class).')
    parser.add_argument('--year', type=int, nargs=2, required=True, help='Start and end year (inclusive).')
    
    args = parser.parse_args()
    subdataset = args.subdataset
    start_year, end_year = args.year

    print(f"Starting processing from year {start_year} to {end_year} for subdataset {subdataset}.")
    main(start_year, end_year, subdataset)
    print("Processing completed.")
