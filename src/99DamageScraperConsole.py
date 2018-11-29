import argparse
import sys
import threading
import scraper

import time


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    scrap_choice = parser.add_mutually_exclusive_group()

    scrap_choice.add_argument('--scrap_league',
                              help="Scraps Div and League data and creates json File (no Playerdata), est Runtime: 8 Min", action="store_true", dest='scrap_league')
    scrap_choice.add_argument('--add_players',
                              help='Adds Playerdata to scrap_league json (scrap_league must be run first), est Runtime: 38 Min', action="store_true", dest='add_players')
    scrap_choice.add_argument(
        '--scrap_all', help='Scraps Div and League Data first and than adds players to Data, est Runtime: 46 Min', action="store_true", dest='scrap_all')

    if len(sys.argv) < 2:  # if no arg
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    if args.scrap_league:
        print('League Scraper started...')
        # todo remove hardcoded leaguelink
        league_scrap_thread = threading.Thread(target=scraper.scrap_league_and_div_data, args=[
                                               'https://csgo.99damage.de/de/leagues/99dmg/989-saison-10', ], name='League Scrap', daemon=True)
        league_scrap_thread.start()
        # TODO cant be interrupted
        league_scrap_thread.join()

    if args.add_players:
        print('Add Players started...')
        add_team_thread = threading.Thread(
            target=scraper.add_teamdata_to_data, daemon=True)
        add_team_thread.start()
        # TODO cant be interrupted
        add_team_thread.join()
    if args.scrap_all:
        print('Scrap All (League and Players) started...')
        print('League Scraper started...')
        # todo remove hardcoded url
        league_scrap_thread = threading.Thread(target=scraper.scrap_league_and_div_data, args=[
                                               'https://csgo.99damage.de/de/leagues/99dmg/989-saison-10', ], name='League Scrap', daemon=True)
        league_scrap_thread.start()
        # TODO cant be interrupted
        league_scrap_thread.join()
        time.sleep(5)
        print('Add Players started...')
        add_team_thread = threading.Thread(
            target=scraper.add_teamdata_to_data, daemon=True)
        add_team_thread.start()
        # TODO cant be interrupted
        add_team_thread.join()
