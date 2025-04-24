### README.md

```markdown
# Onboarding Asset Automation Project

This project automates the onboarding of assets to Azure Blob Storage, Vusion Rail API, and Korona Cloud API. It integrates with Microsoft OneDrive to retrieve files, Azure Blob Storage for file uploads, and third-party APIs for publishing and tagging assets dynamically.

## Features
- Retrieve files from OneDrive.
- Upload files to Azure Blob Storage.
- Map assets to devices using Vusion Rail API.
- Publish assets to devices on Vusion Rail.
- Add tags to Korona Cloud.

---

## Requirements

### Prerequisites
1. **Python**: Install Python 3.8 or higher.
2. **Dependencies**: Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables**:
   Create a `.env` file with the following structure:
   ```env
   # OneDrive Configuration
   ONEDRIVE_BASE_URL=https://graph.microsoft.com/v1.0/me/drive/root:/FolderName:/children
   ONEDRIVE_ACCESS_TOKEN=your_current_access_token
   ONEDRIVE_REFRESH_TOKEN=your_refresh_token
   ONEDRIVE_CLIENT_ID=your_client_id
   ONEDRIVE_CLIENT_SECRET=your_client_secret
   ONEDRIVE_TENANT_ID=your_tenant_id
   ONEDRIVE_REDIRECT_URI=http://localhost:8000
   ONEDRIVE_AUTHORIZATION_CODE=your_authorization_code

   # Azure Blob Storage Configuration
   AZURE_STORAGE_ACCOUNT=your_azure_storage_account_name
   AZURE_STORAGE_KEY=your_azure_storage_key
   AZURE_CONTAINER_NAME=your_azure_container_name

   # Vusion Rail Configuration
   VUSION_SUBSCRIPTION_KEY=your_subscription_key
   VUSION_STORE_ID=your_store_id

   # Korona Cloud Configuration
   KORONA_ACCOUNT_ID=your_korona_account_id
   KORONA_USERNAME=your_korona_username
   KORONA_PASSWORD=your_korona_password
   ```

---

## How to Get Started

### Step 1: Set Up Authorization for OneDrive

#### Register an App in Azure Portal
1. Visit the [Azure Portal](https://portal.azure.com/).
2. Navigate to **Azure Active Directory** > **App Registrations**.
3. Click **New Registration**, fill in the details, and register the app.
4. Note down:
   - **Client ID** (Application ID)
   - **Tenant ID** (Directory ID)
5. Go to **Certificates & Secrets** > **New Client Secret** and note down the secret.

#### Configure Redirect URI
1. Under your app's settings in Azure, go to **Authentication**.
2. Add a **Redirect URI**. Example: `http://localhost:8000`.

#### Generate Authorization Code
1. Construct the following URL:
   ```
   https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?
   client_id={client_id}&
   response_type=code&
   redirect_uri=http://localhost:8000&
   response_mode=query&
   scope=https://graph.microsoft.com/.default offline_access&
   state=12345
   ```
   Replace:
   - `{tenant_id}`: Your Azure Tenant ID.
   - `{client_id}`: Your Azure Client ID.
2. Open the URL in a browser, log in, and authorize the app.
3. You will be redirected to the redirect URI with an `authorization_code` in the URL.

#### Example Redirect URL:
```
http://localhost:8000/?code=AUTHORIZATION_CODE&state=12345
```
Extract the `AUTHORIZATION_CODE` from the URL and update your `.env` file:
```env
ONEDRIVE_AUTHORIZATION_CODE=AUTHORIZATION_CODE
```

---

### Step 2: Get Access Token
Run the following Python script to generate the `access_token` and `refresh_token`:
```bash
python access_token.py
```
The script will:
1. Use the `authorization_code` to request an `access_token`.
2. Print the `access_token` and `refresh_token`.
3. Automatically update the `.env` file with new tokens.

---

### Project Workflow

1. **Step 0: Validate or Refresh OneDrive Token**  
   Ensure the OneDrive token is valid. The script will refresh it automatically if expired.

2. **Step 1: Download Files from OneDrive**  
   Retrieve files from the specified folder in OneDrive.

3. **Step 2: Upload Files to Azure Blob Storage**  
   Upload retrieved files to the Azure Blob container.

4. **Step 3: Map Devices and Publish Assets**  
   - Fetch registered devices from Vusion Rail API.
   - Publish uploaded files to devices.

5. **Step 4: Add Tags to Korona Cloud**  
   Add tags for each file and device using the Korona Cloud API.

---

## Run the Project

To execute the workflow, run:
```bash
python main.py
```

---

## Troubleshooting

1. **Invalid Authorization Code**:
   - Ensure the `ONEDRIVE_AUTHORIZATION_CODE` is fresh and correctly copied.
   - Generate a new code using the authorization URL if needed.

2. **Expired Tokens**:
   - Refresh tokens using:
     ```bash
     python access_token.py
     ```

3. **HTTP Errors**:
   - Check API keys and ensure all environment variables are correctly set.
   - Verify network connectivity and endpoint accessibility.

4. **Missing Dependencies**:
   - Ensure all required packages are installed:
     ```bash
     pip install -r requirements.txt
     ```

---

## Contributing

Contributions are welcome! If you have suggestions or find any issues, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License.
```
