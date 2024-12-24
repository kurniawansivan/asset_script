import logging
import os
from config import *
from one_drive import download_files_from_onedrive
from azure_blob import upload_to_azure_blob
from vusion_rail import get_devices, update_background
from korona_cloud import add_tags

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def terminate_process(message):
    """Terminate the process with an error message."""
    logging.error(message)
    raise SystemExit(message)

def main():
    try:
        # Step 0: Use manually provided OneDrive access token
        logging.info("Step 0: Using manually provided OneDrive access token...")
        access_token = os.getenv("ONEDRIVE_ACCESS_TOKEN")
        if not access_token:
            terminate_process("No OneDrive access token provided in the .env file.")
        logging.info("OneDrive access token loaded successfully.")

        # Step 1: Download files from OneDrive
        logging.info("Step 1: Downloading files from OneDrive...")
        download_path = "./downloads"
        files = download_files_from_onedrive(ONEDRIVE_BASE_URL, download_path, access_token)
        if not files:
            terminate_process("No files were downloaded from OneDrive.")
        logging.info(f"Downloaded {len(files)} files from OneDrive successfully.")

        # Step 2: Upload files to Azure Blob Storage
        logging.info("Step 2: Uploading files to Azure Blob Storage...")
        uploaded_files = []
        for file in files:
            file_path = f"{download_path}/{file}"
            blob_name = file
            try:
                video_url = upload_to_azure_blob(
                    AZURE_STORAGE_ACCOUNT, AZURE_STORAGE_KEY, AZURE_CONTAINER_NAME, file_path, blob_name
                )
                uploaded_files.append({"file": file, "url": video_url})
                logging.info(f"Uploaded file {file} to Azure Blob Storage successfully.")
            except Exception as e:
                terminate_process(f"Failed to upload file {file} to Azure Blob Storage. Error: {e}")

        # Step 3: Get devices from Vusion Rail
        logging.info("Step 3: Fetching devices from Vusion Rail API...")
        try:
            devices = get_devices(VUSION_SUBSCRIPTION_KEY, VUSION_STORE_ID)
            if not devices:
                terminate_process("No devices found in Vusion Rail API.")
            logging.info(f"Retrieved {len(devices)} devices from Vusion Rail API successfully.")
        except Exception as e:
            terminate_process(f"Failed to fetch devices from Vusion Rail API. Error: {e}")

        # Step 4: Update background for each device
        logging.info("Step 4: Updating backgrounds for devices...")
        for uploaded_file in uploaded_files:
            for device in devices:
                try:
                    update_background(
                        VUSION_SUBSCRIPTION_KEY,
                        VUSION_STORE_ID,
                        device["id"],
                        uploaded_file["url"],
                        uploaded_file["file"]
                    )
                    logging.info(f"Background updated for device {device['id']} using file {uploaded_file['file']}.")
                except Exception as e:
                    logging.error(f"Failed to update background for device {device['id']}. Skipping. Error: {e}")

        # Step 5: Add tags to Korona Cloud
        logging.info("Step 5: Adding tags to Korona Cloud API...")
        for uploaded_file in uploaded_files:
            for device in devices:
                try:
                    add_tags(
                        KORONA_ACCOUNT_ID,
                        KORONA_USERNAME,
                        KORONA_PASSWORD,
                        device["id"],
                        uploaded_file["file"]
                    )
                    logging.info(f"Tag added for device {device['id']} with file {uploaded_file['file']} successfully.")
                except Exception as e:
                    logging.error(f"Failed to add tag for device {device['id']} in Korona Cloud. Skipping. Error: {e}")

        logging.info("All steps completed successfully.")

    except Exception as e:
        terminate_process(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
