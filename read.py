# read.py
from google.oauth2 import service_account
from googleapiclient.discovery import build

def read_data_from_sheet(spread_sheet_id):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'keys.json'

    creds = None
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spread_sheet_id, range='original_menu!A:W').execute()
    results = result['values']

    v1_name = ''
    v2_name = ''
    v3_name = ''
    v1_category_names = []
    v2_category_names = []
    v3_category_names = []

    for index, row in enumerate(results, start=1):
        if index == 3:
            v1_name = row[1]
            v2_name = row[2]
            v3_name = row[3]
        elif index >= 4:
            v1_category_name = row[6]
            v2_category_name = row[7]
            v3_category_name = row[8]
            if v1_category_name not in v1_category_names and v1_category_name != '':
                v1_category_names.append(v1_category_name)
            if v2_category_name not in v2_category_names and v2_category_name != '':
                v2_category_names.append(v2_category_name)
            if v3_category_name not in v3_category_names and v3_category_name != '':
                v3_category_names.append(v3_category_name)

    return results, v1_name, v2_name, v3_name, v1_category_names, v2_category_names, v3_category_names
