# @title Change detection functions
def create_disaster_map(country_name, disaster_year, type, df):
    # Create the map
    Map_africa = geemap.Map(**map_config)
    if type == 'Drought':
        year_before = disaster_year - 1
        year_after = disaster_year + 5
    else:
        year_before = disaster_year - 1
        year_after = disaster_year + 1

    # Center the map on the coordinates of the first disaster location
    filtered_df = df[(df['Country'] == country_name) & (df['Year'] == disaster_year)]
    if not filtered_df.empty:
        first_location = filtered_df.iloc[0]
        longitude_list = first_location['Longitude']
        latitude_list = first_location['Latitude']
        disaster_type = first_location['Disaster type']

        # Debugging: Print the longitude and latitude to understand their format
        print("Longitude List:", longitude_list)
        print("Latitude List:", latitude_list)

        # Check if longitude_list and latitude_list are lists; if not, convert them
        if isinstance(longitude_list, str):
            longitude_list = eval(longitude_list)
        elif isinstance(longitude_list, float):
            longitude_list = [longitude_list]

        if isinstance(latitude_list, str):
            latitude_list = eval(latitude_list)
        elif isinstance(latitude_list, float):
            latitude_list = [latitude_list]

        # Debugging: Print the lists after conversion
        print("Converted Longitude List:", longitude_list)
        print("Converted Latitude List:", latitude_list)
    else:
        raise ValueError("No disaster data found for the specified country and year.")

    # Calculate the population change
    pop_change_img = calculate_population_change(country_name, year_before, year_after)

    disaster_colors = {
        "Flood": "#80B1D3",
        "Storm": "#BEBADA",
        "Drought": "#FFFFB3",
        "Earthquake": "#8DD3C7",
        "Volcanic activity": "#FB8072"
    }

    Map_africa.addLayer(pop_change_img, vis_params, f'Population change from {year_before} to {year_after}')
    Map_africa.addLayer(filter_countries(country_name), {'opacity': 0.3}, 'Country Boundary')

    # Iterate over each disaster in the filtered DataFrame
    for index, row in filtered_df.iterrows():
        longitude_list = row['Longitude']
        latitude_list = row['Latitude']
        disaster_type = row['Disaster type']  # Assuming the disaster type is in this column

        point_color = disaster_colors.get(disaster_type, 'black')  # Default to black if disaster type not found

        # Add multiple points to the map for each disaster
        for i, (lon, lat) in enumerate(zip(longitude_list, latitude_list), start=1):
            point = ee.Geometry.Point([lon, lat])
            print(f"Adding point at longitude: {lon}, latitude: {lat}, color: {point_color}")  # Debugging: print each point being added
            Map_africa.addLayer(point, {'color': point_color}, f'{disaster_type} Location {index+1}-{i}')

    # Add legend to the map
    Map_africa.addLayerControl()
    Map_africa.add_legend(title='Population Count Estimate', legend_dict=legend_dict)

    # Center the map on the selected country
    filtered_country = filter_countries(country_name)
    country_geom = filtered_country.geometry()
    Map_africa.centerObject(country_geom, zoom=6)

    # Display the map
    return Map_africa

# Land use land cover change detection
def create_class_change_map(country_name, disaster_year, target_class, class_names, classes, palette, africa_map_config):
    year1 = disaster_year - 1
    year2 = disaster_year + 1

    # Load the GLC_FCS30D annual dataset
    annual = ee.ImageCollection("projects/sat-io/open-datasets/GLC-FCS30D/annual")
    annual_before = annual.mosaic().select(f'b{year1 - 1999}')
    annual_after = annual.mosaic().select(f'b{year2 - 1999}')

    Map = geemap.Map(**map_config)

    for class_name in target_class:
        class_index = class_names.index(class_name)
        class_value = classes[class_index]

        # Define the visualization parameters
        vis_params = {
            'min': 0,
            'max': 1,
            'palette': ['000000', palette[class_index]]
        }

        change_vis_params = {
            'min': -1,
            'max': 1,
            'palette': ['red', 'green']
        }

        classified_area_before = annual_before.eq(class_value)
        classified_area_before_masked = classified_area_before.updateMask(classified_area_before)
        classified_area_after = annual_after.eq(class_value)
        classified_area_after_masked = classified_area_after.updateMask(classified_area_after)

        # Calculate the change: 1 for gain, -1 for loss, 0 for no change.
        change = classified_area_after.subtract(classified_area_before)

        # Mask the change to only show areas where change occurred.
        change_masked = change.updateMask(change.neq(0))

        # Add the urban areas to the map
        Map.add_layer(classified_area_before_masked.clip(geometry), vis_params, f"{class_name} Before")
        Map.add_layer(classified_area_after_masked.clip(geometry), vis_params, f"{class_name} After")
        Map.add_layer(change_masked.clip(geometry), change_vis_params, f"{class_name} Change")

    # Filter the DataFrame for the specified country and year
    filtered_df = grouped_df[(grouped_df['Country'] == country_name) & (grouped_df['Year'] == disaster_year)]
    if filtered_df.empty:
        raise ValueError("No disaster data found for the specified country and year.")

    # Iterate over each disaster in the filtered DataFrame
    for index, row in filtered_df.iterrows():
        longitude_list = row['Longitude']
        latitude_list = row['Latitude']
        disaster_type = row['Disaster type']  # Assuming the disaster type is in this column

        point_color = disaster_colors.get(disaster_type, 'black')  # Default to black if disaster type not found

        # Add multiple points to the map for each disaster
        for i, (lon, lat) in enumerate(zip(longitude_list, latitude_list), start=1):
            point = ee.Geometry.Point([lon, lat])
            print(f"Adding point at longitude: {lon}, latitude: {lat}, color: {point_color}")  # Debugging: print each point being added
            Map.addLayer(point, {'color': point_color}, f'{disaster_type} Location {index+1}-{i}')

    # Display the map
    country_geom = geometry.geometry()
    Map.centerObject(country_geom, zoom=6)
    Map.addLayerControl()
    return Map