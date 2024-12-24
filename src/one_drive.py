import requests
import os

def download_files_from_onedrive(base_url, download_path):
    headers = {"Authorization": f"Bearer {os.getenv('ONEDRIVE_ACCESS_TOKEN')}"}
    response = requests.get(base_url, headers=headers)
    response.raise_for_status()

    files = response.json().get("value", [])
    downloaded_files = []

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for file in files:
        file_name = file["name"]
        download_url = file["@microsoft.graph.downloadUrl"]
        file_path = os.path.join(download_path, file_name)

        with open(file_path, "wb") as f:
            f.write(requests.get(download_url).content)
        downloaded_files.append(file_name)

    return downloaded_files
