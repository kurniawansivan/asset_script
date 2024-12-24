from azure.storage.blob import BlobServiceClient
import re

def sanitize_blob_name(blob_name):
    """
    Sanitize blob name to ensure it meets Azure Blob Storage naming rules.
    """
    # Remove invalid characters and replace spaces with hyphens
    sanitized_name = re.sub(r"[\\/#?]", "-", blob_name).strip()
    return sanitized_name

def upload_to_azure_blob(storage_account, storage_key, container_name, file_path, blob_name):
    connection_string = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={storage_account};"
        f"AccountKey={storage_key};"
        f"EndpointSuffix=core.windows.net"
    )

    # Sanitize the blob name
    blob_name = sanitize_blob_name(blob_name)

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        return blob_client.url
    except Exception as e:
        raise Exception(f"Failed to upload {file_path} to Azure Blob Storage. Error: {e}")
