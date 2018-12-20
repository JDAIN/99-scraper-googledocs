import re

def wrong_steam_id_list(data):
    #useful
    ret_list =[]
    #ret_list.append(['Steam_id', 'Player', 'Team', 'Division', 'Teamlink'])
    for div, divdata in data.items():
        for team, teamdata in divdata['Teams'].items():

            if teamdata['Players'] != 'no players, team deleted':
                for player, playerdata in teamdata['Players'].items():
                    player_steamid = playerdata['steam_id']
                    if len(player_steamid) > 1:
                        try:
                            reg = re.search(r'^steam_[0|1]:[0|1]:\d{1,9}$', player_steamid).group()
                        except:
                            ret_list.append([player,player_steamid,team, div,teamdata['link']])
                            #print(r'" {} " | {}   ({} | {} | {})'.format(player_steamid,player,team, div,teamdata['link']))
    return ret_list