import pandas as pd
# ==================
# Cleaning the data
# ==================

def select_and_rename_columns(data, selected_columns, new_column_names=None):
    """
    Selects specific columns from a DataFrame and renames them if new names are provided.
    
    Args:
        data (pd.DataFrame): The original DataFrame.
        selected_columns (list): A list of column names to select. These must exist in the DataFrame.
        new_column_names (list, optional): A list of new names for the selected columns. Must have the same length as selected_columns if provided.
    
    Returns:
        pd.DataFrame: A DataFrame containing only the selected columns, possibly renamed.
    
    Raises:
        ValueError: If the lengths of selected_columns and new_column_names do not match.
        KeyError: If any of the selected columns are not present in the data.
    """
    # Validate that all selected columns exist in the DataFrame
    if not all(column in data.columns for column in selected_columns):
        missing_columns = [column for column in selected_columns if column not in data.columns]
        raise KeyError(f"The following columns are missing from the DataFrame: {missing_columns}")
    
    # Select the relevant columns
    data_with_selected_columns = data[selected_columns]
    
    # Rename the columns if new names are provided
    if new_column_names:
        if len(selected_columns) != len(new_column_names):
            raise ValueError("The length of 'selected_columns' and 'new_column_names' must be the same.")
        data_with_selected_columns.columns = new_column_names
    
    return data_with_selected_columns


import pandas as pd

def filter_african_disasters(data, years_range=None, capitalize=False):
    """
    Filters a DataFrame for African countries and specific years, adjusts disaster type casing,
    and ensures robust error handling.

    Args:
        data (pd.DataFrame): The original DataFrame with disaster data.
        years_range (list, range, or None): List or range of years for which data is to be filtered.
        capitalize (bool): If True, capitalizes the first letter of each disaster type.

    Returns:
        pd.DataFrame: A DataFrame filtered by African countries and specified years,
                      with the 'Disaster type' column formatted to start with a capital letter if specified.

    Raises:
        ValueError: If 'data' is not a DataFrame, 'years_range' is not a list or range of integers, or contains non-integer elements.
    """
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The 'data' argument must be a pandas DataFrame.")
    
    if years_range is not None:
        if not isinstance(years_range, (list, range)):
            raise ValueError("The 'years_range' argument must be a list or range.")
        if not all(isinstance(year, int) for year in years_range):
            raise ValueError("All elements in 'years_range' must be integers.")

    # List of African countries
    africa = (
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
        "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
        "Ivory Coast", "Djibouti", "Democratic Republic of the Congo", "Egypt",
        "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia",
        "Ghana", "Guinea", "Guinea-Bissau", "Kenya", "Lesotho", "Liberia", "Libya",
        "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique",
        "Namibia", "Niger", "Nigeria", "Republic of the Congo", "Rwanda", "Sao Tome & Principe",
        "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan",
        "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"
    )

    # Filter the data for African countries
    african_data = data[data['Country'].isin(africa)]

    # Filter data by specified years if provided
    if years_range:
        african_data = african_data[african_data['Year'].isin(years_range)]

    # Capitalize the first letter of each disaster type if specified
    if capitalize:
        african_data['Disaster type'] = african_data['Disaster type'].str.capitalize()

    return african_data.reset_index(drop=True)