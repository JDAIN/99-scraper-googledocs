import re
import Data_analysis_sheet
from collections import Counter
import json
from operator import itemgetter
from gspread_formatting import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def auth_google():
    #returns client
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'client_secret.json',
        ['https://spreadsheets.google.com/feeds'])
    return gspread.authorize(credentials)




def create_wrong_steam_id_sheet(data, client):
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1oRedPa92QILDHDlBwsT1EYUpqn92ZuYY7Foc1Muy4Rk')
    # worksheet = sheet.get_worksheet(0)
    # list_of_lists = worksheet.get_all_values()
    my_list = Data_analysis_sheet.wrong_steam_id_list(data)
    sheet.values_clear(
        'wrong Steam_ids!A2:Z1000'
    )
    sheet.values_update(
        'wrong Steam_ids!A2',
        params={'valueInputOption': 'RAW'},
        body={'values': my_list},

    )

if __name__ == '__main__':
    client = auth_google()
    #read data
    with open('team_player_data.json', 'r') as file:
        data = json.load(file)
    #sheet with wrong steamids
    create_wrong_steam_id_sheet(data, client)

