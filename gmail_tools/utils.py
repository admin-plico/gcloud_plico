import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from admin_connection_local import get_admin_directory_service
# from drive_tools.utils import get_drive_service # use this one when in django

CLOUD_USER = "cloud@plicodesignstudio.com"


SERVICE_ACCOUNT_FILE = '../credentials/service-account.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
DELEGATE_EMAIL = 'super@plicodesignstudio.com'  # for delegated access


def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    ).with_subject(DELEGATE_EMAIL)

    return build('drive', 'v3', credentials=creds)


def get_all_user_emails():
    service = get_admin_directory_service()

    results = []
    page_token = None

    while True:
        response = service.users().list(
            customer='my_customer',
            maxResults=100,
            orderBy='email',
            pageToken=page_token
        ).execute()

        users = response.get('users', [])
        results.extend([user['primaryEmail'] for user in users])

        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return results


def get_user_profile_ss(user_email: str) -> dict:
    """
    Fetch user profile details from Google Workspace.

    Returns:
        dict: JSON-compatible user data including name, phone, title, etc.
    """
    try:
        service = get_admin_directory_service()
        user = service.users().get(userKey=user_email).execute()

        data = {
            "email": user.get("primaryEmail"),
            "name": f"{user['name'].get('givenName', '')} {user['name'].get('familyName', '')}",
            "title": user.get("organizations", [{}])[0].get("title", ""),
            "phone": "",
            "studies": "",
        }

        # Optional fields
        phones = user.get("phones", [])
        if phones:
            work_phones = [p['value'] for p in phones if p.get("type") == "work"]
            if work_phones:
                data["phone"] = work_phones[0]

        orgs = user.get("organizations", [])
        if orgs:
            data["location"] = orgs[0].get("location", "")
        print(json.dumps(data, indent=4))
        return data

    except Exception as e:
        print(f"❌ Error retrieving data for {user_email}: {e}")
        return {}


def get_user_profile(user_email: str) -> dict:
    """
    Fetch selected user attributes from Google Workspace Admin SDK.

    Returns:
        dict: Contains full name, job title, home phone, and employee type.
    """
    try:
        service = get_admin_directory_service()
        user = service.users().get(userKey=user_email).execute()
        email =  user.get("primaryEmail")
        full_name = user.get("name", {}).get("fullName", "")
        organizations = user.get("organizations", [])
        phones = user.get("phones", [])

        # Get job title and employee type from organizations
        job_title = ""
        studies = ""
        if organizations:
            job_title = organizations[0].get("title", "")
            # STUDIES GOES IN THE "EMPLOYEE TYPE" IT THE EMPLOYEE PROFILE OF GOOGLE WORKSPACE
            studies = organizations[0].get("description", "")

        # Get home phone
        home_phone = ""
        for phone in phones:
            if phone.get("type") == "home":
                home_phone = phone.get("value", "")
                break

        data = {
            "name": full_name,
            "email": email,
            "function": job_title,
            "mobile": home_phone,
            "studies": studies
        }
        print(json.dumps(data, indent=4))
        return data
    except Exception as e:
        print(f"❌ Error retrieving user data for {user_email}: {e}")
        return {}


def list_files_in_folder(folder_id):
    service = get_drive_service()
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id, name, mimeType)",
        pageSize=100
    ).execute()

    for f in results.get('files', []):
        print(f"✅ {f['name']} ({f['mimeType']})")


def ensure_file_is_public(file_id):
    service = get_drive_service()
    service.permissions().create(
        fileId=file_id,
        body={"role": "reader", "type": "anyone"},
        fields="id"
    ).execute()


def get_plico_logo():
    file_name = "PLICO DESIGN STUDIO_CURRENT.png"
    parent_folder_id = "1VAFisv9tRuRZJWN_dG9YQxdZpvJ2MkfD"
    """Return the Google Drive direct image link for a given file name."""
    list_files_in_folder(parent_folder_id)
    service = get_drive_service()

    # query = f"name = '{file_name}' and mimeType contains 'image/'"
    # if parent_folder_id:
    #     query += f" and '{parent_folder_id}' in parents"
    query = (
        f"name = '{file_name}' and mimeType contains 'image/' and '{parent_folder_id}' in parents"
    )
    results = service.files().list(
        q=query,
        pageSize=1,
        fields="files(id, name)"
    ).execute()

    items = results.get('files', [])
    if not items:
        raise FileNotFoundError(f"Image file '{file_name}' not found in Google Drive.")

    file_id = items[0]['id']
    # ensure_file_is_public(file_id)
    # ensure_file_is_public(file_id)
    link = f"https://drive.google.com/uc?export=view&id={file_id}"

    return link


# get_plico_logo()


# get_user_profile("david@plicodesignstudio.com")