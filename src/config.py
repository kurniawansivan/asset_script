from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# OneDrive Configuration
ONEDRIVE_BASE_URL = os.getenv("ONEDRIVE_BASE_URL", "https://graph.microsoft.com/v1.0/me/drive/root")
ONEDRIVE_ACCESS_TOKEN = os.getenv("ONEDRIVE_ACCESS_TOKEN")
ONEDRIVE_CLIENT_ID = os.getenv("ONEDRIVE_CLIENT_ID")
ONEDRIVE_CLIENT_SECRET = os.getenv("ONEDRIVE_CLIENT_SECRET")
ONEDRIVE_TENANT_ID = os.getenv("ONEDRIVE_TENANT_ID")
ONEDRIVE_AUTHORITY_URL = os.getenv(
    "ONEDRIVE_AUTHORITY_URL", f"https://login.microsoftonline.com/{ONEDRIVE_TENANT_ID}/oauth2/v2.0/token"
)

# Azure Blob Storage Configuration  
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "default-container")

# Vusion Rail Configuration
VUSION_SUBSCRIPTION_KEY = os.getenv("VUSION_SUBSCRIPTION_KEY")
VUSION_STORE_ID = os.getenv("VUSION_STORE_ID")

# Korona Cloud Configuration
KORONA_ACCOUNT_ID = os.getenv("KORONA_ACCOUNT_ID")
KORONA_USERNAME = os.getenv("KORONA_USERNAME")
KORONA_PASSWORD = os.getenv("KORONA_PASSWORD")

# Check for missing critical configurations
if not ONEDRIVE_CLIENT_ID or not ONEDRIVE_CLIENT_SECRET or not ONEDRIVE_TENANT_ID:
    logging.warning("Missing OneDrive credentials. Check .env file for ONEDRIVE_CLIENT_ID, CLIENT_SECRET, and TENANT_ID.")
if not AZURE_STORAGE_ACCOUNT or not AZURE_STORAGE_KEY:
    logging.warning("Missing Azure Blob Storage credentials. Check .env file for AZURE_STORAGE_ACCOUNT and AZURE_STORAGE_KEY.")
if not KORONA_ACCOUNT_ID or not KORONA_USERNAME or not KORONA_PASSWORD:
    logging.warning("Missing Korona Cloud credentials. Check .env file for KORONA_ACCOUNT_ID, USERNAME, and PASSWORD.")
