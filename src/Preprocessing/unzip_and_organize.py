import os
import zipfile
import re
import argparse
import requests

def extract_country_code(zip_filename):
    """Extract the country code (letters) from the zip filename."""
    match = re.search(r'[A-Z]{3}', zip_filename)
    return match.group(0) if match else None

def get_country_name(country_code):
    """Get the country name from the country code using the restcountries.com API."""
    try:
        response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
        response.raise_for_status()
        data = response.json()
        return data[0]['name']['common']
    except requests.RequestException as e:
        print(f"Error fetching country name for code {country_code}: {e}")
        return None

def unzip_files_in_folder(zip_folder_path, output_folder_path):
    """Unzip all zip files in the specified folder and extract to subfolders based on country name."""
    for item in os.listdir(zip_folder_path):
        if item.endswith('.zip'):
            zip_filepath = os.path.join(zip_folder_path, item)
            country_code = extract_country_code(item)
            if country_code:
                country_name = get_country_name(country_code)
                if country_name:
                    subfolder_path = os.path.join(output_folder_path, country_name)
                    os.makedirs(subfolder_path, exist_ok=True)
                    
                    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                        zip_ref.extractall(subfolder_path)
                    
                    print(f"Extracted {item} to {country_name}/{country_code}")
                else:
                    print(f"Could not fetch country name for code {country_code}")
            else:
                print(f"Could not extract country code from {item}")

def main():
    parser = argparse.ArgumentParser(description='Unzip files and organize them into subfolders.')
    parser.add_argument('--input', type=str, required=True, help='Path to the folder containing zip files.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output folder where subfolders will be created.')
    
    args = parser.parse_args()
    unzip_files_in_folder(args.input, args.output)

if __name__ == "__main__":
    main()
