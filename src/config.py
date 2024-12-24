from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OneDrive Configuration
ONEDRIVE_BASE_URL = os.getenv("ONEDRIVE_BASE_URL")
ONEDRIVE_ACCESS_TOKEN = os.getenv("ONEDRIVE_ACCESS_TOKEN")
ONEDRIVE_CLIENT_ID = os.getenv("ONEDRIVE_CLIENT_ID")
ONEDRIVE_CLIENT_SECRET = os.getenv("ONEDRIVE_CLIENT_SECRET")
ONEDRIVE_TENANT_ID = os.getenv("ONEDRIVE_TENANT_ID")
ONEDRIVE_AUTHORITY_URL = os.getenv("ONEDRIVE_AUTHORITY_URL")

# Azure Blob Storage Configuration
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

# Vusion Rail Configuration
VUSION_SUBSCRIPTION_KEY = os.getenv("VUSION_SUBSCRIPTION_KEY")
VUSION_STORE_ID = os.getenv("VUSION_STORE_ID")

# Korona Cloud Configuration
KORONA_ACCOUNT_ID = os.getenv("KORONA_ACCOUNT_ID")
KORONA_USERNAME = os.getenv("KORONA_USERNAME")
KORONA_PASSWORD = os.getenv("KORONA_PASSWORD")
