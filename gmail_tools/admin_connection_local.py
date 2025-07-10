import os
import pickle
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user',
          'https://www.googleapis.com/auth/gmail.settings.sharing',
          'https://www.googleapis.com/auth/gmail.settings.basic',
          'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '../credentials/service-account.json'
DELEGATE_EMAIL = 'super@plicodesignstudio.com'  # must be a super admin


def get_admin_directory_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    ).with_subject(DELEGATE_EMAIL)

    return build('admin', 'directory_v1', credentials=creds)


def get_gmail_service(user_email):
    # SCOPES = ['https://www.googleapis.com/auth/gmail.settings.sharing']
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    ).with_subject(user_email)  # impersonate the user

    return build('gmail', 'v1', credentials=creds)
# get_admin_directory_service()




