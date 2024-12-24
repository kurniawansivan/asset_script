import requests
import os
import logging

def download_files_from_onedrive(base_url, download_path, access_token, test_only=False):
    """
    Mengunduh file dari OneDrive.

    Args:
        base_url (str): URL API OneDrive untuk direktori target.
        download_path (str): Path lokal untuk menyimpan file yang diunduh.
        access_token (str): Token akses untuk otentikasi OneDrive.
        test_only (bool): Jika True, hanya memvalidasi token tanpa mengunduh file.

    Returns:
        list: Daftar nama file yang berhasil diunduh.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        # Request file metadata
        response = requests.get(base_url, headers=headers)
        if test_only:
            return response  # Validasi token jika test_only=True
        response.raise_for_status()

        files = response.json().get("value", [])
        downloaded_files = []

        # Buat direktori jika belum ada
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        logging.info(f"Found {len(files)} files in OneDrive folder.")

        # Unduh setiap file
        for file in files:
            try:
                file_name = file["name"]
                download_url = file["@microsoft.graph.downloadUrl"]
                file_path = os.path.join(download_path, file_name)

                # Cek apakah file sudah ada
                if os.path.exists(file_path):
                    logging.info(f"File {file_name} already exists. Skipping download.")
                    continue

                logging.info(f"Downloading {file_name}...")
                with open(file_path, "wb") as f:
                    f.write(requests.get(download_url).content)

                downloaded_files.append(file_name)
                logging.info(f"Successfully downloaded {file_name}.")

            except Exception as e:
                logging.error(f"Failed to download file {file_name}. Error: {e}")

        return downloaded_files

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch files from OneDrive. Error: {e}")
        raise
