import json
import logging
import os
import time

import CONFIG
import gspread
import gspread_formatting
from oauth2client.service_account import ServiceAccountCredentials
import Data_analysis_sheet


def auth_google():
    # returns client
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CONFIG.GOOGLE_CLIENT_SECRET_FILENAME,
        ['https://spreadsheets.google.com/feeds'])
    return gspread.authorize(credentials)


def create_wrong_steam_id_sheet(data, client):
    sheet = client.open_by_url(CONFIG.GOOGLE_DOCS_LINK)
    sheet.values_clear(
        'wrong Steam_ids!A2:Z1000'
    )
    sheet.values_update(
        'wrong Steam_ids!A2',
        params={'valueInputOption': 'RAW'},
        body={'values': Data_analysis_sheet.wrong_steam_id_list(data)},

    )


def create_switched_team_more_than_once_sheet(data, client):
    sheet = client.open_by_url(CONFIG.GOOGLE_DOCS_LINK)
    sheet.values_clear(
        'switched_more_than_once!A2:Z1000'
    )
    switch_list = Data_analysis_sheet.readable_check_if_switched_team_more_than_once(
        data)

    sheet.values_update(
        'switched_more_than_once!A2',  # TODO RENAME
        params={'valueInputOption': 'RAW'},
        body={'values': switch_list},
        # TODO FORMATING
    )


def create_check_lower_div_join_sheet(data, client):
    sheet = client.open_by_url(CONFIG.GOOGLE_DOCS_LINK)
    sheet.values_clear(
        'lower_div!A2:Z1000'
    )
    lowerdiv_list = Data_analysis_sheet.readable_check_lower_div_join(data)

    sheet.values_update(
        'lower_div!A2',  # TODO RENAME
        params={'valueInputOption': 'RAW'},
        body={'values': lowerdiv_list},
        # TODO FORMATING
    )



if __name__ == '__main__':
    logger = logging.getLogger('spreader')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('logger.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    ch.setLevel(logging.INFO)
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.info('__________________________START_____________________')
    logger.info('scraping Data...')
    os.system("99DamageScraperConsole.py --scrap_all")
    logger.info('DONE')

    time.sleep(2)
    logger.info('Auth Google....')
    client = auth_google()
    logger.info('DONE')

    # read data
    with open('team_player_data.json', 'r') as file:
        logger.info('reading Data....')
        data = json.load(file)
    logger.info('DONE')

    logger.info('deleting team_player_data.json')

    # now = datetime.datetime.now()
    # timestring = now.strftime('%d-%m-%y %H-%M')
    # os.rename('team_player_data.json',
    #           'team_player_data' + timestring + '.json')
    os.remove("team_player_data.json")
    logger.info('DONE')
    # sheet with wrong steamids
    logger.info('updating sheets')
    create_wrong_steam_id_sheet(data, client)
    create_switched_team_more_than_once_sheet(data, client)
    create_check_lower_div_join_sheet(data, client)
    logger.info('DONE')
    logger.info('__________________________DONE_____________________')
