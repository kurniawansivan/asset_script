from azure.storage.blob import BlobServiceClient

def upload_to_azure_blob(storage_account, storage_key, container_name, file_path, blob_name):
    connection_string = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={storage_account};"
        f"AccountKey={storage_key};"
        f"EndpointSuffix=core.windows.net"
    )

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return blob_client.url
