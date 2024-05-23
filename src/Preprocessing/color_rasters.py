import os
from osgeo import gdal, gdalconst

def apply_color_table(input_file, output_file, color_table_file):
    # Open the input raster file
    input_dataset = gdal.Open(input_file, gdalconst.GA_ReadOnly)
    if input_dataset is None:
        print(f"Error: Unable to open input raster file {input_file}.")
        return
    
    # Read the color table from the .clr file
    color_table = gdal.ColorTable()
    color_table_file = open(color_table_file, 'r')
    for line in color_table_file:
        parts = line.strip().split()
        color_table.SetColorEntry(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))
    color_table_file.close()

    # Get raster band
    input_band = input_dataset.GetRasterBand(1)

    # Define output raster parameters
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_file, input_dataset.RasterXSize, input_dataset.RasterYSize, 1, gdalconst.GDT_Byte)
    output_dataset.SetProjection(input_dataset.GetProjection())
    output_dataset.SetGeoTransform(input_dataset.GetGeoTransform())
    output_band = output_dataset.GetRasterBand(1)

    # Set color table to the output band
    output_band.SetRasterColorTable(color_table)

    # Read and write each line
    for y in range(input_dataset.RasterYSize):
        scanline = input_band.ReadAsArray(0, y, input_dataset.RasterXSize, 1)
        output_band.WriteArray(scanline, 0, y)

    # Close datasets
    output_band.FlushCache()
    output_dataset = None
    input_dataset = None

def process_folder(input_folder, output_folder, color_table_file):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.tif') or filename.endswith('.tiff'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            apply_color_table(input_file, output_file, color_table_file)
            print(f"Processed: {input_file} -> {output_file}")

# Define the input and output directories
input_folder = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff_files_with_shapefile"
output_folder = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff_colored"
color_map = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\Color_palette.clr"
apply_color_table(input_folder, output_folder, color_map)

