import os
import requests
import gdown
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleDriveDownloader:
    def __init__(self, url, output_dir, credentials_json):
        self.url = url
        self.output_dir = output_dir
        self.credentials_json = credentials_json
        self.service = self.authenticate_drive_api()

    def authenticate_drive_api(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_json, scopes=['https://www.googleapis.com/auth/drive']
        )
        return build('drive', 'v3', credentials=credentials)

    def download(self):
        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        folder_id = self.extract_folder_id(self.url)
        if not folder_id:
            raise ValueError("Invalid Google Drive URL")

        # List files in the folder
        query = f"'{folder_id}' in parents"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])

        if not files:
            print('No files found in the folder.')
            return

        for file in files:
            file_id = file['id']
            file_name = file['name']
            download_url = f'https://drive.google.com/uc?id={file_id}'
            output_file = os.path.join(self.output_dir, file_name)

            if not self.is_file_accessible(download_url):
                print(f"Cannot access the file {file_name}. Please ensure the file is shared with 'Anyone with the link' permission.")
                continue

            try:
                gdown.download(download_url, output_file, quiet=False)
                print(f"File {file_name} downloaded to {output_file}")
            except gdown.exceptions.FileURLRetrievalError as e:
                print(f"Error downloading {file_name}: {e}")

    @staticmethod
    def extract_folder_id(url):
        if 'drive.google.com/drive/folders/' in url:
            return url.split('drive.google.com/drive/folders/')[1].split('?')[0]
        return None

    @staticmethod
    def is_file_accessible(url):
        try:
            response = requests.head(url, allow_redirects=True)
            return response.status_code == 200
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return False

# Usage example
if __name__ == '__main__':
    url = 'https://drive.google.com/drive/u/0/folders/10V1uRfJMqzRA95SIy9Bcj-UJXGCQ3uFr'
    output_dir = './downloads'
    credentials_json = 'path_to_your_service_account_credentials.json'
    
    downloader = GoogleDriveDownloader(url, output_dir, credentials_json)
    downloader.download()
