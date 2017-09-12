
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
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

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
            updateSheet = service.spreadsheets().values().batchUpdate(
                spreadsheetId = spreadsheetId,
                body = UpdateValue(cellID = row, rowCount = rowCount)).execute()
            rowCount += 1

def CellID(rowCount):
    return 'CLEGO!C' + str(rowCount) + ':F' + str(rowCount)

def UpdateValue(cellID, rowCount):
    bashCommand = "ssh -tq dphan@minos60.fnal.gov ls /pnfs/minos/persistent/users/dphan/FeldmanCousinsAppearanceAnalysisDM" + ParseCellID(cellID=cellID[0]) + "/GridGenStandard/Output/gridfile_dm_" + cellID[0] + "*.root | wc -l"
    process = subprocess.Popen(bashCommand, shell=True, stdout = subprocess.PIPE)
    updatedGridGen = process.stdout.read();

    bashCommand = "ssh -tq dphan@minos60.fnal.gov ls /pnfs/minos/persistent/users/dphan/FeldmanCousinsAppearanceAnalysisDM" + ParseCellID(cellID=cellID[0]) + "/NueFitStandard/Output/ | wc -l"
    process = subprocess.Popen(bashCommand, shell=True, stdout = subprocess.PIPE)
    updatedNueFit = process.stdout.read();

    values = [
        [
            updatedGridGen, '=5*B'+str(rowCount), '=C'+str(rowCount)+'/D'+str(rowCount), updatedNueFit
        ]
    ]

    data = [
        {
            'range': CellID(rowCount=rowCount),
            'values': values
        }
    ]

    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    return body

def ParseCellID(cellID):
    cellidRegex = re.compile(r'[.]')
    return cellidRegex.sub('d', cellID)

if __name__ == '__main__':
    while (True):
        main()
        time.sleep(500)
