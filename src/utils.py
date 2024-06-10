import geopandas as gpd
import pandas as pd
import numpy as np
import ee

# Authenticate the Earth Engine API
ee.Authenticate()
ee.Initialize()

# =====================
# Functions for Geemap
# =====================
def feature2ee(file):
    """
    Convert geographic data files into Google Earth Engine (GEE) feature collections.
    Handles shapefiles and CSV files and converts them into corresponding EE geometries.
    """
    try:
        if file.endswith('.shp'):
            gdf = gpd.read_file(file, encoding="utf-8")
            features = []

            for geom in gdf.geometry:
                if geom.geom_type == 'Polygon':
                    coords = np.dstack(geom.exterior.coords.xy).tolist()
                    ee_geom = ee.Geometry.Polygon(coords)
                elif geom.geom_type == 'LineString':
                    coords = np.dstack(geom.coords.xy).tolist()
                    ee_geom = ee.Geometry.LineString(coords[0])  # Flatten the list
                elif geom.geom_type == 'Point':
                    x, y = geom.coords.xy
                    ee_geom = ee.Geometry.Point([x[0], y[0]])
                else:
                    continue  # Skip unsupported geometries

                feature = ee.Feature(ee_geom)
                features.append(feature)

            ee_object = ee.FeatureCollection(features)
            print("Shapefile converted successfully.")
            return ee_object

        elif file.endswith('.csv'):
            df = pd.read_csv(file)

            # Drop rows with NaN values in critical columns
            df = df.dropna(subset=['Longitude', 'Latitude', 'Disaster type'])

            def clean_value(value):
                return value if pd.notna(value) else 'Unknown'

            features = [
                ee.Feature(
                    ee.Geometry.Point([row['Longitude'], row['Latitude']]),
                    {
                        'disaster_type': clean_value(row['Disaster type']),
                        'date': row['Date'],
                        'country': clean_value(row['Country']),
                        'deaths': clean_value(row['Total deaths']),
                        'location': clean_value(row['Location'])
                    }
                )
                for idx, row in df.iterrows()
            ]

            ee_object = ee.FeatureCollection(features)
            print("CSV file converted successfully.")
            return ee_object

        else:
            print("Unsupported file format.")
            return None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None