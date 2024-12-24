import requests

def get_devices(subscription_key, store_id):
    url = f"https://eu-api.vusionrail.com/v1/stores/{store_id}/devices"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def update_background(subscription_key, store_id, device_id, video_url, cache_id):
    url = f"https://eu-api.vusionrail.com/v1/stores/{store_id}/devices/{device_id}/background"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    payload = {
        "layers": [
            {
                "id": "layer-1",
                "type": "video",
                "width": 1920,
                "height": 158,
                "url": video_url,
                "cacheId": cache_id,
                "visible": True
            }
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
