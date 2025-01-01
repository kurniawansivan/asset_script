import requests
from requests.auth import HTTPBasicAuth
import logging

def add_tags(account_id, username, password, tags):
    """
    Add tags to the Korona Cloud API.

    Args:
        account_id (str): Korona account ID.
        username (str): Korona username.
        password (str): Korona password.
        tags (list): A list of tags in the format {"device_id": "00001", "cache_id": "testing_1_00001"}.

    Returns:
        None
    """
    # Endpoint URL
    url = f"https://196.koronacloud.com/web/api/v3/accounts/{account_id}/tags"
    auth = HTTPBasicAuth(username, password)

    # Prepare the payload
    payload = [{"name": f'{{"deviceId": "{tag["device_id"]}", "cacheId": "{tag["cache_id"]}"}}'} for tag in tags]

    try:
        # Log request
        logging.info(f"Adding {len(payload)} tags to Korona Cloud...")

        # Send POST request
        response = requests.post(url, json=payload, auth=auth)
        response.raise_for_status()

        # Log success
        logging.info("Tags added successfully.")

    except requests.exceptions.RequestException as e:
        # Log error
        logging.error(f"Failed to add tags to Korona Cloud. Error: {e}")
        raise e
