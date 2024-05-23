# LULC Data Processing Scripts

This repository contains various scripts for processing Land Use and Land Cover (LULC) data, including clipping rasters with shapefiles, converting NetCDF to GeoTIFF, applying color tables to rasters, detecting LULC changes, and unzipping and organizing files.

## Table of Contents

- [clip_raster.py](#clip_rasterpy)
- [color_rasters.py](#color_rasterspy)
- [convert_nc_to_tiff.py](#convert_nc_to_tiffpy)
- [lulc_change_detection.py](#lulc_change_detectionpy)
- [unzip_and_organize.py](#unzip_and_organizepy)

### clip_raster.py

This script clips a raster file using multiple shapefiles found in a specified directory and its subdirectories. The output clipped rasters are saved in a specified output directory.

#### Usage

```sh
python clip_raster.py --rpath <raster_path> --input <input_directory> --output <output_directory>
```

#### Arguments

- `--rpath`: Path to the input raster file.
- `--input`: Directory containing shapefiles.
- `--output`: Directory to save clipped rasters.

#### Example

```sh
python clip_raster.py --rpath "path/to/lulc_map.tif" --input "path/to/shapefiles" --output "path/to/output"
```

### color_rasters.py

This script applies a color table to all TIFF raster files in a specified directory and saves the colored rasters in an output directory.

#### Usage

```sh
python color_rasters.py
```

#### Configuration

- `input_folder`: Directory containing the input TIFF files.
- `output_folder`: Directory to save the colored TIFF files.
- `color_map`: Path to the color table file (.clr).

#### Example

```sh
python color_rasters.py
```

Ensure you have set the correct paths for `input_folder`, `output_folder`, and `color_map` within the script before running it.

### convert_nc_to_tiff.py

This script converts NetCDF files to GeoTIFF format for a specified range of years and subdataset, then clips the GeoTIFF files using a specified shapefile.

#### Usage

```sh
python convert_nc_to_tiff.py --subdataset <subdataset> --year <start_year> <end_year> --shapefile <shapefile>
```

#### Arguments

- `--subdataset`: Subdataset to extract (e.g., lccs_class).
- `--year`: Start and end year (inclusive).
- `--shapefile`: Path to the shapefile for clipping.

#### Example

```sh
python convert_nc_to_tiff.py --subdataset lccs_class --year 2000 2018 --shapefile "path/to/shapefile.shp"
```

### lulc_change_detection.py

This script performs LULC change detection and calculates year-on-year percentage change for the specified range of years.

#### Usage

```sh
python lulc_change_detection.py --year <start_year> <end_year>
```

#### Arguments

- `--year`: Start and end year (inclusive).

#### Example

```sh
python lulc_change_detection.py --year 2000 2018
```

### unzip_and_organize.py

This script unzips all ZIP files in a specified directory and organizes the extracted files into subdirectories based on country names.

#### Usage

```sh
python unzip_and_organize.py --input <input_directory> --output <output_directory>
```

#### Arguments

- `--input`: Path to the folder containing ZIP files.
- `--output`: Path to the output folder where subfolders will be created.

#### Example

```sh
python unzip_and_organize.py --input "path/to/zip_files" --output "path/to/output"
```

---

Make sure to install any required dependencies (e.g., GDAL, numpy, pandas, requests) before running these scripts. You can install them using pip:

```sh
pip install gdal numpy pandas requests
```
