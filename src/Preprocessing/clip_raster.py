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

def main(raster_path, input_directory, output_directory):
    # Find all shapefiles
    shapefiles = find_shapefiles(input_directory)
    
    if not shapefiles:
        print("No shapefiles found matching the pattern.")
        return
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    raster_name = os.path.splitext(os.path.basename(raster_path))[0]
    
    for shapefile in shapefiles:
        # Generate output filename
        shapefile_name = os.path.basename(shapefile).replace('.shp', '')
        output_path = os.path.join(output_directory, f'{raster_name}_{shapefile_name}_clipped.tif')
        
        print(f'Clipping raster with {shapefile}')
        
        # Clip the raster
        clip_raster_with_shapefile(raster_path, shapefile, output_path)
        
        print(f'Saved clipped raster to {output_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clip raster by shapefiles')
    parser.add_argument('--rpath', type=str, required=True, help='Path to the input raster file')
    parser.add_argument('--input', type=str, required=True, help='Directory containing shapefiles')
    parser.add_argument('--output', type=str, required=True, help='Directory to save clipped rasters')

    args = parser.parse_args()
    
    main(args.rpath, args.input, args.output)
