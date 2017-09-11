
from __future__ import print_function
import httplib2
import os
import subprocess
import re
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    """
        Your code start here!
    """

    # SpeadSheetID
    spreadsheetId = '1uT8k_ab_qyUaTMsuascYDpQcc9zonsR66mjtxm_lfRs'
    # Specify range of cells to work with
    rangeName = 'CLEGO!A2:H17'

    # Actual processing code
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        rowCount = 2;
        for row in values:
            updateSheet = service.spreadsheets().values().update(
                spreadsheetId = spreadsheetId,
                range = CellID(rowCount),
                valueInputOption = 'USER_ENTERED',
                body = UpdateValue(row[0])).execute()
            rowCount += 1

def CellID(rowCount):
    return 'CLEGO!F' + str(rowCount)

def UpdateValue(cellID):

    bashCommand = "ssh -tq dphan@minos60.fnal.gov ls /pnfs/minos/persistent/users/dphan/FeldmanCousinsAppearanceAnalysisDM" + ParseCellID(cellID=cellID) + "/NueFitStandard/Output/ | wc -l"
    process = subprocess.Popen(bashCommand, shell=True, stdout = subprocess.PIPE)

    body = {
        'values':[[process.stdout.read()]]
    }
    return body

def ParseCellID(cellID):
    cellidRegex = re.compile(r'[.]')
    return cellidRegex.sub('d', cellID)

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(500)
