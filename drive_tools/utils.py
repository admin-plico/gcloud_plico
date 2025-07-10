import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from django.conf import settings


# SCOPES
SC = ['https://www.googleapis.com/auth/drive']

# Redirect URI registered in Google Cloud Console
REDIRECT_URI = 'https://PlicoAdmin.pythonanywhere.com/drive_tools/oauth2callback/'

# Path to client secret
CLIENT_SECRETS_FILE = os.path.join(settings.BASE_DIR, 'credentials', 'gc-client_secret-2.json')


def get_flow():
    """Create OAuth2 flow instance"""
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SC,
        redirect_uri=REDIRECT_URI
    )


def save_credentials_to_db(user, credentials):
    from cloud_mgmt.models import GoogleCredentials
    token, _ = GoogleCredentials.objects.get_or_create(user=user)
    token.token = credentials.token
    token.refresh_token = credentials.refresh_token or token.refresh_token
    token.token_uri = credentials.token_uri
    token.client_id = credentials.client_id
    token.client_secret = credentials.client_secret
    token.scopes = credentials.scopes
    token.save()


def get_drive_service(user):
    from cloud_mgmt.models import GoogleCredentials
    try:
        token = GoogleCredentials.objects.get(user=user)
        creds = Credentials(**token.as_dict())

        # Auto-refresh and save if needed
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            save_credentials_to_db(user, creds)

        return build('drive', 'v3', credentials=creds)
    except GoogleCredentials.DoesNotExist:
        return None
