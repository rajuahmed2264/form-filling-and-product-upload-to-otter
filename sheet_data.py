import gspread
from google.oauth2.service_account import Credentials

# Load the credentials from the JSON key file downloaded earlier
credentials = Credentials.from_service_account_file('keys.json')

# Authenticate with the Google Sheets API
client = gspread.authorize(credentials)

# Open the shared Google Sheet using the URL
sheet_url = 'https://docs.google.com/spreadsheets/d/1iud5AkQ-cTF-QO7Q8dcIvmG2niZJKtFr7eMhacdxYOc/edit#gid=482786943'
sheet = client.open_by_url(sheet_url)

# Access the individual worksheets within the spreadsheet
worksheet = sheet.sheet1  # Replace 'sheet1' with the desired worksheet name

# Fetch data from the worksheet
data = worksheet.get_all_values()
print(data)
