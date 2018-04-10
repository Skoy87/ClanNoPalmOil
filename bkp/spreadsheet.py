from oauth2client.service_account import ServiceAccountCredentials
import gspread

def spreadsheet():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)


    sheet = client.open("clan").sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    return list_of_hashes
print (spreadsheet())