import os
import subprocess
import argparse
import fnmatch
from osgeo import gdal

def clip_raster_with_shapefile(raster_path, shapefile_path, output_path):
    # Use GDAL warp to clip the raster
    subprocess.run([
        'gdalwarp',
        '-cutline', shapefile_path,
        '-crop_to_cutline',
        '-dstalpha',
        raster_path,
        output_path
    ])

def find_shapefiles(directory, pattern="gadm41_*_1.shp"):
    shapefiles = []
    for root, _, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                shapefiles.append(os.path.join(root, file))
    return shapefiles

def find_input_file(input_dir, year):
    pattern = f"LULC_{year}_lccs_class.tiff"
    input_file = os.path.join(input_dir, pattern)
    print(f"Checking for file: {input_file}")  # Added for debugging
    if os.path.exists(input_file):
        print(f"Found raster file for year {year}: {input_file}")  # Added for debugging
        return input_file
    return None

def main(input_directory, shapefile_directory, output_directory, start_year, end_year):
    # Find all shapefiles
    shapefiles = find_shapefiles(shapefile_directory)
    
    if not shapefiles:
        print("No shapefiles found matching the pattern.")
        return
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    for year in range(start_year, end_year + 1):
        raster_path = find_input_file(input_directory, year)
        
        if not raster_path:
            print(f"No raster file found for year {year}.")
            continue
        
        # Create subfolder for the year
        year_output_directory = os.path.join(output_directory, str(year))
        os.makedirs(year_output_directory, exist_ok=True)
        
        raster_name = os.path.splitext(os.path.basename(raster_path))[0]
        
        for shapefile in shapefiles:
            # Generate output filename
            shapefile_name = os.path.basename(shapefile).replace('.shp', '')
            output_path = os.path.join(year_output_directory, f'{raster_name}_{shapefile_name}_clipped.tif')
            
            print(f'Clipping raster {raster_path} with {shapefile}')
            
            # Clip the raster
            clip_raster_with_shapefile(raster_path, shapefile, output_path)
            
            print(f'Saved clipped raster to {output_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clip rasters by shapefiles')
    parser.add_argument('--input', type=str, required=True, help='Directory containing raster files')
    parser.add_argument('--shapefiles', type=str, required=True, help='Directory containing shapefiles')
    parser.add_argument('--output', type=str, required=True, help='Directory to save clipped rasters')
    parser.add_argument('--start_year', type=int, required=True, help='Start year for the rasters')
    parser.add_argument('--end_year', type=int, required=True, help='End year for the rasters')

    args = parser.parse_args()
    
    main(args.input, args.shapefiles, args.output, args.start_year, args.end_year)
