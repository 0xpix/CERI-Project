import os
import sys
import zipfile
import re
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), r"C:\Users\nschl\Documents\AIMS_MSc_Project_CERI\GitHub\CERI-Project\src\data"))
from country_code import country_code_dict

def extract_country_code(zip_filename):
    """Extract the country code (letters) from the zip filename."""
    match = re.search(r'[A-Z]{3}', zip_filename)
    return match.group(0) if match else None

def get_country_name(country_code):
    """Get the country name from the country code using the local dictionary."""
    return country_code_dict.get(country_code, None)

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
