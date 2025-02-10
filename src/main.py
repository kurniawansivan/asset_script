import logging
import os
import time
from config import *
from one_drive import download_files_from_onedrive
from azure_blob import upload_to_azure_blob
from vusion_rail import get_devices, update_background
from korona_cloud import add_tags  # Ensure this file/function exists

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

        # Helper function: which devices should get this file?
        def get_target_devices_for_file(filename_no_ext):
            """
            1) If the file name includes exactly one device ID (e.g., "00001"), return [thatDevice].
            2) Otherwise, return all devices.
            """
            matched_device_id = None
            for dev in devices:
                if dev["id"] in filename_no_ext:
                    matched_device_id = dev["id"]
                    break

            if matched_device_id:
                return [matched_device_id]
            else:
                # No match => file goes to all devices
                return [dev["id"] for dev in devices]

        # Step 4: Update backgrounds
        logging.info("Step 4: Updating backgrounds for devices...")

        for uploaded_file in uploaded_files:
            file_name = uploaded_file["file"]
            cache_id = os.path.splitext(file_name)[0]
            video_url = uploaded_file["url"]

            # Get the device list for this file
            target_device_ids = get_target_devices_for_file(cache_id)

            if len(target_device_ids) == 1:
                logging.info(
                    f"File '{file_name}' => single device {target_device_ids[0]} "
                    f"(cacheId='{cache_id}', url='{video_url}')."
                )
            else:
                logging.info(
                    f"File '{file_name}' => multiple devices {target_device_ids} "
                    f"(cacheId='{cache_id}', url='{video_url}')."
                )

            # Update each target device
            for dev_id in target_device_ids:
                logging.info(
                    f"Device {dev_id}: updating background with file={file_name}, "
                    f"cacheId={cache_id}, url={video_url}"
                )
                try:
                    update_background(
                        VUSION_SUBSCRIPTION_KEY,
                        VUSION_STORE_ID,
                        dev_id,
                        video_url,
                        cache_id
                    )
                    logging.info(f"Device {dev_id}: background updated successfully.")
                    logging.info("Sleeping 5s before next update...")
                    time.sleep(5)
                except Exception as e:
                    logging.error(f"Failed to update background for device {dev_id}. Error: {e}")

        # Step 5: Create and post tags for Korona Cloud API
        logging.info("Step 5: Creating and posting tags for Korona Cloud API...")
        tags = []

        def get_target_devices_for_tags(filename_no_ext):
            # Same logic for tag creation
            matched_device_id = None
            for dev in devices:
                if dev["id"] in filename_no_ext:
                    matched_device_id = dev["id"]
                    break

            if matched_device_id:
                return [matched_device_id]
            else:
                return [dev["id"] for dev in devices]

        for uf in uploaded_files:
            file_name_no_ext = os.path.splitext(uf["file"])[0]
            target_device_ids = get_target_devices_for_tags(file_name_no_ext)

            if len(target_device_ids) == 1:
                dev_id = target_device_ids[0]
                tag = {
                    "name": f'{{"deviceId": "{dev_id}", "cacheId": "{file_name_no_ext}"}}'
                }
                tags.append(tag)
                logging.info(
                    f"File '{file_name_no_ext}' => single device {dev_id}. Tag: {tag}"
                )
            else:
                for dev_id in target_device_ids:
                    tag = {
                        "name": f'{{"deviceId": "{dev_id}", "cacheId": "{file_name_no_ext}"}}'
                    }
                    tags.append(tag)
                    logging.info(
                        f"File '{file_name_no_ext}' => device {dev_id}. Tag: {tag}"
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
