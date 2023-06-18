from Recognition import FaceRecognition
from Google import Create_Service
import os
import io
from googleapiclient.http import MediaIoBaseDownload
from  pathlib import Path
import pandas as pd
CLIENT_SECRET_FILE='client_desktop.json'
API_SERVICE_NAME='drive'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

def extract_folder_id(drive_link):
    prefix = "https://drive.google.com/drive/folders/"
    suffix = "?usp=sharing"
    if drive_link.startswith(prefix) and drive_link.endswith(suffix):
        folder_id = drive_link[len(prefix):-len(suffix)]
        return folder_id
    else:
        return None

def download_files(files):
    download_path = str(Path.home() / "Downloads")
    for file in files:
        file_id = file["id"]
        request = service.files().get_media(fileId = file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print('Download progress {0}'.format(status.progress()*100))

        fh.seek(0)

        with open(os.path.join(download_path, file["name"]), 'wb') as f:
            f.write(fh.read())
            f.close()

def search_photos(faces, link):
    print("Extracting files")
    folder_id = extract_folder_id(link)
    print(folder_id)
    query = f"parents = '{folder_id}'"

    response = service.files().list(q=query, pageSize=1000, fields='nextPageToken, files(id, name)').execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.files().list(q=query, pageSize=1000, pageToken=nextPageToken, fields='nextPageToken, files(id, name)').execute()
        files.extend(response.get('files', []))
        nextPageToken = response.get('nextPageToken')
    
    for file in files:
        print(file['id'])
    recognized_files = []
    print("Files extracted")
    fr = FaceRecognition(faces)
    print("Encoding complete")
    for file in files:
        print("Running file: "+file['id'])
        if(fr.run_recognition(file['id'])):
            recognized_files.append({"id" : file['id'], "name" : file['name']})
            print(file['name'])

    print(recognized_files)
    df = pd.DataFrame(files)
    return recognized_files, len(recognized_files)