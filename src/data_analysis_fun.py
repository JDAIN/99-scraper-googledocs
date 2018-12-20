import re
from collections import Counter
import json
from operator import itemgetter
#data =[]
with open('team_player_data.json','r') as file:
    data = json.load(file)


def players_with_most_teamswitches_in_active_teams(data):
    #data is kinda useless j4f, bc if a Team isnt active anymore it wont be counted
    Playerlist =[]
    #print(data)
    for key,value in data.items():
        for vv,vvv in value['Teams'].items():

             Playerlist.extend([x for x in vvv['Players'] if len(x)>1])

    print(Playerlist)
    ww = Counter(Playerlist)
    print(ww.most_common(50))


def oldest_and_newest_steam_ids(data):
    #j4f
    steamid_list = {}
    idiot_counter = 0
    for div ,divdata in data.items():
        for team,teamdata in divdata['Teams'].items():

            if teamdata['Players'] != 'no players, team deleted':
                for player, playerdata in teamdata['Players'].items():
                    player_steamid= playerdata['steam_id']
                    if len(player_steamid)>1:
                        try:
                            reg = re.search(r'^steam_[0|1]:[0|1]:\d{1,9}$', player_steamid).group()
                            number = int(player_steamid.split(':')[2])
                            player_and_steam_id = player +'|'+ player_steamid
                            steamid_list[player_and_steam_id] = number
                        except: #TODO make work
                            idiot_counter+=1
                            pass

    print('Filtered {} false Steam_ids'.format(idiot_counter))
    players_by_shortest_id = sorted(steamid_list.items(),key=itemgetter(1))
    print('Top20: oldest steam_ids {}'.format(players_by_shortest_id[:20]))
 #TODO remove number in print statement
    print('Top20: newest steam_ids {}'.format(players_by_shortest_id[-20:][::-1]))#last 20, -1 for reverse
    print(players_by_shortest_id)

    #print(steamid_list)


def wrong_steam_id(data):
    #useful
    for div, divdata in data.items():
        for team, teamdata in divdata['Teams'].items():

            if teamdata['Players'] != 'no players, team deleted':
                for player, playerdata in teamdata['Players'].items():
                    player_steamid = playerdata['steam_id']
                    if len(player_steamid) > 1:
                        try:
                            reg = re.search(r'^steam_[0|1]:[0|1]:\d{1,9}$', player_steamid).group()
                        except:
                            print(r'" {} " | {}   ({} | {} | {})'.format(player_steamid,player,team, div,teamdata['link']))


wrong_steam_id(data)

