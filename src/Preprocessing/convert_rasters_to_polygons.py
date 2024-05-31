import os
import argparse
from osgeo import gdal, ogr, osr

def convert_raster_to_polygon(input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    tiff_files = [f for f in os.listdir(input_path) if f.endswith('.tif')]
    
    for tiff_file in tiff_files:
        tiff_path = os.path.join(input_path, tiff_file)
        output_shapefile = os.path.join(output_path, os.path.splitext(tiff_file)[0] + '.shp')
        
        # Open the source file
        src_ds = gdal.Open(tiff_path)
        if src_ds is None:
            print(f"Unable to open {tiff_path}")
            continue

        srcband = src_ds.GetRasterBand(1)
        
        # Create output shapefile
        drv = ogr.GetDriverByName("ESRI Shapefile")
        dst_ds = drv.CreateDataSource(output_shapefile)
        dst_layer = dst_ds.CreateLayer(output_shapefile, srs = None)
        gdal.Polygonize(srcband, srcband, dst_layer, -1, [], callback=None)

        dst_ds.Destroy()
        src_ds = None
        
        print(f"Converted {tiff_file} to {output_shapefile}")

def main():
    parser = argparse.ArgumentParser(description='Convert raster TIFF files to polygon shapefiles.')
    parser.add_argument('--input', type=str, required=True, help='Path to the directory containing TIFF files.')
    parser.add_argument('--output', type=str, required=True, help='Path to the directory to save polygon shapefiles.')
    
    args = parser.parse_args()
    
    convert_raster_to_polygon(args.input, args.output)

if __name__ == "__main__":
    main()
