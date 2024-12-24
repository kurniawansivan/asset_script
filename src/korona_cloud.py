import requests
from requests.auth import HTTPBasicAuth

def add_tags(account_id, username, password, device_id, cache_id):
    url = f"https://196.koronacloud.com/web/api/v3/accounts/{account_id}/tags"
    auth = HTTPBasicAuth(username, password)
    payload = [{"name": cache_id, "number": device_id}]
    response = requests.post(url, json=payload, auth=auth)
    response.raise_for_status()
