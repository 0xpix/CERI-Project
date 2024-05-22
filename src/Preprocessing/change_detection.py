import os
import subprocess
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from scipy.ndimage import binary_opening

def align_tiff(input_tif1, input_tif2, output_tif1, output_tif2):
    """Align two TIFF files to have the same resolution, extent, and projection."""
    with rasterio.open(input_tif1) as src1:
        transform, width, height = calculate_default_transform(
            src1.crs, src1.crs, src1.width, src1.height, *src1.bounds)
        kwargs = src1.meta.copy()
        kwargs.update({
            'crs': src1.crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        
        with rasterio.open(output_tif1, 'w', **kwargs) as dst1:
            for i in range(1, src1.count + 1):
                reproject(
                    source=rasterio.band(src1, i),
                    destination=rasterio.band(dst1, i),
                    src_transform=src1.transform,
                    src_crs=src1.crs,
                    dst_transform=transform,
                    dst_crs=src1.crs,
                    resampling=Resampling.nearest
                )
    
    with rasterio.open(input_tif2) as src2:
        with rasterio.open(output_tif2, 'w', **kwargs) as dst2:
            for i in range(1, src2.count + 1):
                reproject(
                    source=rasterio.band(src2, i),
                    destination=rasterio.band(dst2, i),
                    src_transform=src2.transform,
                    src_crs=src2.crs,
                    dst_transform=transform,
                    dst_crs=src2.crs,
                    resampling=Resampling.nearest
                )

def compute_difference(tif1, tif2, diff_tif):
    """Compute the difference between two aligned TIFF files."""
    with rasterio.open(tif1) as src1, rasterio.open(tif2) as src2:
        diff = src1.read(1) - src2.read(1)
        profile = src1.profile
        profile.update(dtype=rasterio.float32)
        
        with rasterio.open(diff_tif, 'w', **profile) as dst:
            dst.write(diff.astype(rasterio.float32), 1)

def classify_changes(diff_tif, classified_tif, threshold):
    """Classify changes based on a threshold."""
    with rasterio.open(diff_tif) as src:
        diff = src.read(1)
        changes = np.where(abs(diff) > threshold, 1, 0)
        profile = src.profile
        profile.update(dtype=rasterio.uint8)
        
        with rasterio.open(classified_tif, 'w', **profile) as dst:
            dst.write(changes.astype(rasterio.uint8), 1)

# Define file paths
input_tif1 = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff\LULC_2000.tiff"
input_tif2 = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff\LULC_2001.tiff"
aligned_tif1 = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff\aligned_2000.tiff"
aligned_tif2 = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff\aligned_2001.tiff"
diff_tif = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff\diff_2000_2001.tiff"
classified_tif = r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\Dataset\LULC_2000_2018\tiff\classified_2000_2001.tiff"

# Step 1: Align the TIFF files
align_tiff(input_tif1, input_tif2, aligned_tif1, aligned_tif2)

# Step 2: Compute the difference
compute_difference(aligned_tif1, aligned_tif2, diff_tif)

# Step 3: Classify changes (optional)
threshold = 10  # Define your threshold value
classify_changes(diff_tif, classified_tif, threshold)

print("Processing completed.")