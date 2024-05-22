import os
import subprocess
import argparse

def main(start_year, end_year):
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
        input_file = os.path.join(input_dir, f"ESACCI-LC-L4-LCCS-Map-300m-P1Y-{year}-v2.0.7cds.nc")
        output_file = os.path.join(output_dir, f"LULC_{year}.tiff")

        # GDAL translate command with CRS definition
        cmd_translate = [
            "gdal_translate",
            "-of", "GTiff",
            "-a_srs", crs,
            f'NETCDF:"{input_file}":lccs_class',
            output_file
        ]

        # Execute the translate command
        subprocess.run(cmd_translate, check=True)

        print(f"Successfully converted {year}.cs to {year}.tiff with CRS {crs}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert NetCDF to GeoTIFF with specified year range.')
    parser.add_argument('--year', type=int, nargs=2, required=True, help='Start and end year (inclusive).')

    args = parser.parse_args()
    start_year, end_year = args.year

    main(start_year, end_year)