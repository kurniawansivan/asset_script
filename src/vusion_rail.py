import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_devices(subscription_key, store_id):
    """
    Mengambil daftar perangkat dari Vusion Rail API.
    
    Args:
        subscription_key (str): Kunci langganan untuk autentikasi API.
        store_id (str): ID toko Vusion Rail.
    
    Returns:
        list: Daftar perangkat dari API.
    """
    url = f"https://eu-api.vusionrail.com/v1/stores/{store_id}/devices"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    try:
        logging.info("Fetching devices from Vusion Rail API...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        devices = response.json()
        logging.info(f"Successfully retrieved {len(devices)} devices.")
        return devices
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch devices. Error: {e}")
        raise

def update_background(subscription_key, store_id, device_id, video_url, cache_id):
    """
    Memperbarui latar belakang perangkat Vusion Rail.
    
    Args:
        subscription_key (str): Kunci langganan untuk autentikasi API.
        store_id (str): ID toko Vusion Rail.
        device_id (str): ID perangkat Vusion Rail.
        video_url (str): URL video latar belakang.
        cache_id (str): ID cache untuk video.
    
    Returns:
        None
    """
    url = f"https://eu-api.vusionrail.com/v1/stores/{store_id}/devices/{device_id}/background"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    payload = {
        "layers": [
            {
                "id": "layer-1",
                "type": "video",
                "width": 1920,
                "height": 168,
                "url": video_url,
                "cacheId": cache_id,
                "visible": True
            }
        ]
    }
    try:
        logging.info(f"Updating background for device {device_id}...")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logging.info(f"Background updated successfully for device {device_id}.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to update background for device {device_id}. Error: {e}")
        raise

def update_backgrounds_bulk(subscription_key, store_id, video_url, cache_id, devices):
    """
    Memperbarui latar belakang untuk beberapa perangkat secara batch.
    
    Args:
        subscription_key (str): Kunci langganan untuk autentikasi API.
        store_id (str): ID toko Vusion Rail.
        video_url (str): URL video latar belakang.
        cache_id (str): ID cache untuk video.
        devices (list): Daftar perangkat (ID perangkat).
    
    Returns:
        None
    """
    for device in devices:
        try:
            update_background(subscription_key, store_id, device["id"], video_url, cache_id)
        except Exception as e:
            logging.error(f"Failed to update background for device {device['id']}. Skipping. Error: {e}")
