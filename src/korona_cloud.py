import requests
from requests.auth import HTTPBasicAuth
import logging

def add_tags(account_id, username, password, tags):
    """
    Menambahkan tag ke KORONA Cloud.

    Args:
        account_id (str): ID akun KORONA Cloud.
        username (str): Username untuk autentikasi.
        password (str): Password untuk autentikasi.
        tags (list of dict): Daftar tag dengan format [{"device_id": "123", "cache_id": "abc"}].

    Returns:
        None
    """
    # Endpoint URL
    url = f"https://196.koronacloud.com/web/api/v3/accounts/{account_id}/tags"
    auth = HTTPBasicAuth(username, password)

    # Buat payload
    payload = [{"name": tag["cache_id"], "number": tag["device_id"]} for tag in tags]

    try:
        # Log request
        logging.info(f"Adding {len(payload)} tags to KORONA Cloud...")

        # Kirim request POST
        response = requests.post(url, json=payload, auth=auth)
        response.raise_for_status()

        # Log success
        logging.info("Tags added successfully.")

    except requests.exceptions.RequestException as e:
        # Log error
        logging.error(f"Failed to add tags to KORONA Cloud. Error: {e}")
        raise e
