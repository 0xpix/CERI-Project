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
            return input_file
    
    return None

def fix_shapefile_geometry(input_shapefile, output_shapefile):
    cmd_fix = [
        "ogr2ogr",
        "-f", "ESRI Shapefile",
        output_shapefile,
        input_shapefile,
        "-nlt", "POLYGON",
        "-lco", "ENCODING=UTF-8",
        "-t_srs", "EPSG:4326",
        "-makevalid",
        "-skipfailures"
    ]
    subprocess.run(cmd_fix, check=True)

def main(start_year, end_year, subdataset, shapefile):
    input_dir = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\nc"
    output_dir = rf"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff_{subdataset}"
    os.makedirs(output_dir, exist_ok=True)
    crs = "EPSG:4326"  # Example for WGS 84

    fixed_shapefile = os.path.join(output_dir, "fixed_shapefile.shp")
    fix_shapefile_geometry(shapefile, fixed_shapefile)

    for year in range(start_year, end_year + 1):
        input_file = find_input_file(input_dir, year)
        if input_file is None:
            print(f"Warning: No file found for year {year}")
            continue
        
        intermediate_file = os.path.join(output_dir, f"LULC_{year}_{subdataset}_intermediate.tiff")
        output_file = os.path.join(output_dir, f"LULC_{year}_{subdataset}.tiff")

        # GDAL translate command with CRS definition
        cmd_translate = [
            "gdal_translate",
            "-of", "GTiff",
            "-a_srs", crs,
            f'NETCDF:"{input_file}":{subdataset}',
            intermediate_file
        ]

        try:
            # Execute the translate command
            subprocess.run(cmd_translate, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during gdal_translate for year {year}: {e}")
            continue
        
        # GDAL warp command to clip the raster using the shapefile
        cmd_warp = [
            "gdalwarp",
            "-cutline", fixed_shapefile,
            "-crop_to_cutline",
            "-of", "GTiff",
            intermediate_file,
            output_file,
            "-skipfailures"  # Skip failures to ignore overlapping issues
        ]

        try:
            # Execute the warp command
            subprocess.run(cmd_warp, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during gdalwarp for year {year}: {e}")
            os.remove(intermediate_file)
            continue

        # Remove intermediate file
        os.remove(intermediate_file)

        print(f"Successfully converted and clipped for the year {year} with CRS {crs}, subdataset {subdataset}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert NetCDF to GeoTIFF with specified year range and subdataset, and clip using a shapefile.')
    parser.add_argument('--subdataset', type=str, required=True, help='Subdataset to extract (e.g., lccs_class).')
    parser.add_argument('--year', type=int, nargs=2, required=True, help='Start and end year (inclusive).')
    parser.add_argument('--shapefile', type=str, required=True, help='Path to the shapefile for clipping.')

    args = parser.parse_args()
    subdataset = args.subdataset
    start_year, end_year = args.year
    shapefile = args.shapefile

    main(start_year, end_year, subdataset, shapefile)
