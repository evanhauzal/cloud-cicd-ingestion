import os
import json
import requests
from datetime import datetime, timezone
from azure.storage.blob import BlobServiceClient

CONTAINER_NAME = "ingested-data"

def fetch_data():
    # Ganti endpoint ini dengan sumber data final project tim kamu
    url = "https://jsonplaceholder.typicode.com/posts?_limit=10"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()

def upload_to_azure(data):
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("AZURE_STORAGE_CONNECTION_STRING tidak ditemukan.")

    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    blob_name = f"data_{timestamp}.json"

    blob_client = blob_service_client.get_blob_client(
        container=CONTAINER_NAME, blob=blob_name
    )
    blob_client.upload_blob(json.dumps(data, indent=2), overwrite=True)
    print(f"Berhasil upload {blob_name} ke container {CONTAINER_NAME}")

if __name__ == "__main__":
    records = fetch_data()
    upload_to_azure(records)