import logging
import requests
from requests.auth import HTTPBasicAuth

def add_tags(account_id, username, password, tags):
    # Adjust URL/domain if your Korona instance is different
    url = f"https://196.koronacloud.com/web/api/v3/accounts/{account_id}/tags"
    auth = HTTPBasicAuth(username, password)

    logging.info(f"Sending {len(tags)} tag(s) to Korona Cloud: {tags}")

    try:
        for tag in tags:
            logging.info(f"Posting tag: {tag}")
            
            response = requests.post(
                url,
                json=tag,  # The tag dict has the "name" key with the JSON string inside
                auth=auth,
                headers={"Content-Type": "application/json"}
            )

            # Log the response details
            logging.info(f"Response status code: {response.status_code}")
            logging.info(f"Response body: {response.text}")

            # Raise HTTPError if non-2xx status code
            response.raise_for_status()

            logging.info(f"Successfully posted tag: {tag}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to add tags to Korona Cloud. Error: {e}")
        raise
