import os
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from urllib.parse import urlparse


def getFiles(user, url):
    try:
        token = SocialToken.objects.get(
            account__user=user, account__provider='google')

        credentials = Credentials(
            token=token.token,
            refresh_token=token.token_secret,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=os.getenv('client-id', ""),
            client_secret=os.getenv('client-secret', ""))
        
        service = build('drive', 'v3', credentials=credentials)

        urlParts = urlparse(url)
        folderId = urlParts.path.split('/')[-1]
        results = service.files().list(q="'{}' in parents".format(folderId),
                                       fields="nextPageToken, files(name,mimeType)").execute()
        items = results.get('files', [])
        folderMimeType = "application/vnd.google-apps.folder"
        fileNames = [{"name": file["name"], "isFolder": True if (
            file["mimeType"] == folderMimeType) else False} for file in items]
        return fileNames
    except Exception as error:
        print(f'An error occurred: {error}')
