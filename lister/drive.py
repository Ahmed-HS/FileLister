import os
from google.oauth2.credentials import Credentials
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build


def getFiles(user, folderId):
    try:
        token = SocialToken.objects.get(
            account__user=user, account__provider='google')

        credentials = Credentials(
            token=token.token,
            refresh_token=token.token_secret,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=os.getenv('clientId', ""),
            client_secret=os.getenv('clientSecret', ""))
        
        service = build('drive', 'v3', credentials=credentials)

        if not folderId:
            folderId = "root"
        
        query = f"'{folderId}' in parents"
        
        fields="nextPageToken, files(id,name,mimeType)"
        results = service.files().list(q=query,fields=fields).execute()
        files = results.get('files', [])

        folderMimeType = "application/vnd.google-apps.folder"
        for file in files:
            file["isFolder"] =  True if (file["mimeType"] == folderMimeType) else False
        return files
    except Exception as error:
        print(f'An error occurred: {error}')
