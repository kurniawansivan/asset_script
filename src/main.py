import logging
import os
import time
from config import *
from one_drive import download_files_from_onedrive
from azure_blob import upload_to_azure_blob
from vusion_rail import get_devices, update_background
from korona_cloud import add_tags  # Ensure this file/function exist

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
            file_path = os.path.join(download_path, file)
            blob_name = file
            try:
                video_url = upload_to_azure_blob(
                    AZURE_STORAGE_ACCOUNT,
                    AZURE_STORAGE_KEY,
                    AZURE_CONTAINER_NAME,
                    file_path,
                    blob_name
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

        # Step 4: Update background for ALL devices with ALL files
        logging.info("Step 4: Updating backgrounds for every file on every device...")

        for uploaded_file in uploaded_files:
            file_name = uploaded_file["file"]             # e.g. "upload_1_00001.mp4" or "suggest_middle.mp4"
            cache_id = os.path.splitext(file_name)[0]     # e.g. "upload_1_00001" or "suggest_middle"
            video_url = uploaded_file["url"]              # Azure URL

            logging.info(
                f"Uploading asset '{file_name}' (cacheId='{cache_id}') with url='{video_url}' to ALL devices..."
            )

            for device in devices:
                device_id = device["id"]
                try:
                    logging.info(
                        f"Device {device_id}: updating background with file={file_name}, "
                        f"cacheId={cache_id}, url={video_url}"
                    )
                    update_background(
                        VUSION_SUBSCRIPTION_KEY,
                        VUSION_STORE_ID,
                        device_id,
                        video_url,
                        cache_id
                    )
                    logging.info(f"Device {device_id}: background updated successfully.")

                    # Delay 10 seconds so we don't overwhelm the API
                    logging.info("Sleeping 10s before next update...")
                    time.sleep(10)

                except Exception as e:
                    logging.error(f"Failed to update background for device {device_id}. Skipping. Error: {e}")

        # Step 5: Create and post tags for Korona Cloud API
        logging.info("Step 5: Creating and posting tags for Korona Cloud API...")
        tags = []

        for uploaded_file in uploaded_files:
            file_name_no_ext = os.path.splitext(uploaded_file["file"])[0]
            matched_any_device = False

            # Check if filename includes a device's ID:
            for device in devices:
                device_id = device["id"]  # e.g. "00001"
                if device_id in file_name_no_ext:
                    # Found a device-specific file
                    tag = {
                        "name": f'{{"deviceId": "{device_id}", "cacheId": "{file_name_no_ext}"}}'
                    }
                    tags.append(tag)
                    logging.info(
                        f"Matched device {device_id} to file '{file_name_no_ext}'. Tag created: {tag}"
                    )
                    matched_any_device = True
                    break

            # If no specific device ID is in the filename, create a tag for every device:
            if not matched_any_device:
                for device in devices:
                    device_id = device["id"]
                    tag = {
                        "name": f'{{"deviceId": "{device_id}", "cacheId": "{file_name_no_ext}"}}'
                    }
                    tags.append(tag)
                    logging.info(
                        f"Filename '{file_name_no_ext}' does not include a specific device ID, "
                        f"so creating tag for device {device_id}: {tag}"
                    )

        # Log summary of tags
        if tags:
            logging.info(f"Total tags prepared: {len(tags)}")
            for tag in tags:
                logging.info(f"Tag prepared for Korona Cloud: {tag}")
        else:
            logging.warning("No tags prepared for upload.")

        # Automatically send the tags to Korona Cloud
        if tags:
            try:
                logging.info("Posting tags to Korona Cloud...")
                add_tags(KORONA_ACCOUNT_ID, KORONA_USERNAME, KORONA_PASSWORD, tags)
                logging.info("Tags successfully sent to Korona Cloud.")
            except Exception as e:
                logging.error(f"Failed to send tags to Korona Cloud. Error: {e}")
        else:
            logging.info("No tags found to send to Korona Cloud.")

        logging.info("Script completed successfully.")

    except Exception as e:
        terminate_process(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
