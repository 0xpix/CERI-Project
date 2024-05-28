import os
import argparse
import gdown
import zipfile
from tqdm import tqdm

# Define the files to download for raw and processed data
files_to_download = {
    "raw": {
        "10HzjjBEpCCj1pd9XrqHBLWMihV8h_EP2": "data/external/Landscan_data/raw/Landscan_raw.zip",
        # Add more file IDs and paths as needed
    },
    "processed": {
        "17GVeNmIU-TYyuN-MtDeci1V64KHul_KA": "data/external/Landscan_data/processed/Landscan_clipped_Africa.zip",
        "1_jjy2QOnTL7Bl8wVukgcOZbHS2I-7wNZ": "data/external/Landscan_data/processed/Landscan_clipped_country_level.zip",
        # Add more file IDs and paths as needed
    }
}

# Create the data directory if it doesn't exist
os.makedirs("data/external/Landscan_data/raw", exist_ok=True)
os.makedirs("data/external/Landscan_data/processed", exist_ok=True)

def download_files(file_ids_paths):
    # Download each file
    for file_id, dest_path in file_ids_paths.items():
        gdown.download(id=file_id, output=dest_path, quiet=False)

def unzip_with_progress(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_files = len(zip_ref.infolist())
        with tqdm(total=total_files, desc="Unzipping", unit="file") as pbar:
            for file in zip_ref.infolist():
                zip_ref.extract(file, extract_to)
                pbar.update(1)
    os.remove(zip_path)  # Delete the zip file after unzipping

def main(data_type):
    if data_type not in files_to_download:
        print(f"Invalid data type: {data_type}. Choose 'raw' or 'processed'.")
        return
    
    download_files(files_to_download[data_type])

    for dest_path in files_to_download[data_type].values():
        extract_to = os.path.dirname(dest_path)
        unzip_with_progress(dest_path, extract_to)

    print("All files have been downloaded, extracted, and zip files deleted successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and extract data.")
    parser.add_argument("--type", type=str, required=True, help="Type of data to download: 'raw' or 'processed'")
    args = parser.parse_args()

    main(args.type)
