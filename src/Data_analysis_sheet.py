import pprint
import copy
import json
import re
from datetime import datetime
from collections import Counter


def teamdic_change_datestrings_to_timedate_objects(team_dic):
    '''
    Enter a team_dic changes datetime_strings to Datetime objects
    :param team_dic: teamdic
    :return:
    '''

    # creates new list and replaces the datestring with an datetimeobject
    date_team_dic = copy.deepcopy(team_dic)

    for key in date_team_dic.keys():
        counterjoin = 0
        counterleave = 0
        for i in date_team_dic[key]['join_dates']:
            date_team_dic[key]['join_dates'][counterjoin] = datetime.strptime(
                i, '%a, %d %b %Y %H:%M:%S %z')
            counterjoin += 1

        for i in date_team_dic[key]['leave_dates']:
            date_team_dic[key]['leave_dates'][counterleave] = datetime.strptime(
                i, '%a, %d %b %Y %H:%M:%S %z')
            counterleave += 1
    # pretty.pprint(date_team_dic)
    return date_team_dic


def check_if_switched_team_more_than_once(data):
    # TODO rule 24hr
    ret_list = []

    joinleave_player_list = []
    # copys dmgdata
    datasoup_date = copy.deepcopy(data)

    for k, v in data.items():
        for ks, vs in data[k]['Teams'].items():
            # gets only teamdic from dmgdata
            team_dic = data[k]['Teams'][ks]['Players']
            # print('%s : %s : %s ' % (k, ks, team_dic.keys()))
            # checks if player is a dic or just the string 'Team deleted'
            if type(datasoup_date[k]['Teams'][ks]['Players']) == dict:
                # changes/updates datestrings in team_dic_date to datetime object for comparission
                datasoup_date[k]['Teams'][ks]['Players'].update(teamdic_change_datestrings_to_timedate_objects(
                    team_dic))

    for k, v in datasoup_date.items():

        for ks, vs in datasoup_date[k]['Teams'].items():

            if 'no players' not in datasoup_date[k]['Teams'][ks]['Players']:
                for kss, vss in datasoup_date[k]['Teams'][ks]['Players'].items():
                    if vss['join_afterSeasonStart'] or vss['leave_afterSeasonStart']:
                        # joinleave_player_list.append(
                        #   (kss, k, ks, vss['join_dates'], vss['leave_dates'], v['link'], vs['link'], ))
                        if len(vss['leave_dates']) > 0:
                            joinleave_player_list.append(
                                [kss, k, ks, vss['join_dates'][0], vss['leave_dates'][0], v['link'], vs['link'],
                                 vss['time_in_team'], vss['steam_id']])
                        else:
                            joinleave_player_list.append(
                                [kss, k, ks, vss['join_dates'][0], vss['leave_dates'], v['link'], vs['link'],
                                 vss['time_in_team'], vss['steam_id']])

    player_counter = Counter(x[0] for x in joinleave_player_list)

    for k, v in player_counter.items():
        # k = playername v = amount
        # if player left or joined more than or two teams in a season print his data
        if v > 2:
            # get index of the duplicate player items
            indices = [i for i, x in enumerate(
                joinleave_player_list) if x[0] == k]
            # print(indices)
            # get the items with the indices from the list with joined or left player
            l = []
            for e in indices:
                l.append(joinleave_player_list[e])
                # print(joinleave_player_list[e])
            # print(l)

            # makes new list for players teams sorted after joindate
            sorted_after_joindate = sorted(l, key=lambda x: x[3], reverse=True)

            for i in range(len(sorted_after_joindate)):

                sorted_after_joindate[i][3] = sorted_after_joindate[i][3].strftime(
                    '%d.%m.%y %H:%M:%S %z')

                # needed bc if leavedate is a list
                try:
                    sorted_after_joindate[i][4] = sorted_after_joindate[i][4].strftime(
                        '%d.%m.%y %H:%M:%S %z')
                except:
                    pass
            first = True
            l = 0
            for e in sorted_after_joindate:
                l += 1
                e.append(l)

                if first:
                    first_e = e
                    first = False

                if first_e[-1] == e[-1]:
                    ret_list.append(sorted_after_joindate)

    return ret_list


def readable_check_if_switched_team_more_than_once():
    print('''Regel: 4. Zusammensetzung der Teams D. Spielertransfer I.
        Das Wechseln des Teams während einer laufenden Saison ist nur ein Mal erlaubt.
        Mehrfacher Wechsel führt zur Sperrung des Spielers für die laufende Saison und Playoffs bzw.Relegationen.\n''')
    with open('team_player_data.json', 'r') as file:
        data = json.load(file)

    read_dic = check_if_switched_team_more_than_once(data)
    # print(len(read_dic))
    ret_dic = []
    for player_entry in read_dic:
        first_row_player_dic = [''] * 9

        # name of player
        player_name = str(player_entry[0][0])
        print(player_name)
        first_row_player_dic[0] = player_name
        if player_entry[0][-2] != '-':
            # steam_id if active
            print(player_entry[0][-2])
            first_row_player_dic[1] = player_entry[0][-2]
        else:
            # player is inactive '-'
            print('-- (inactive)')
            first_row_player_dic[1] = '-- (inactive)'

        # else:
        # return

        for p in range(len(player_entry)):
            # if player_entry[0][-2] != '-':

            if p == 0 and player_entry[0][-2] != '-':
                first_row_player_dic[2] = player_entry[p][2]  # current team
                first_row_player_dic[3] = player_entry[p][1]  # current div
                first_row_player_dic[5] = player_entry[p][3]  # join date
                first_row_player_dic[7] = 'Aktiv'  # Dauer
                first_row_player_dic[8] = player_entry[p][-4]  # link
                ret_dic.append(first_row_player_dic)
                print('aktuelles Team: %s (%s) Beitritt: %s Dauer: Aktiv %s' % (
                    player_entry[p][2], player_entry[p][1], player_entry[p][3], player_entry[p][-4]))
            else:
                not_first_row_player_dic = [''] * 9
                not_first_row_player_dic[2] = player_entry[p][2]  # team
                not_first_row_player_dic[3] = first_row_player_dic[3]  # current div
                not_first_row_player_dic[4] = player_entry[p][1]  # prev div
                not_first_row_player_dic[6] = player_entry[p][4]  # leavedata
                not_first_row_player_dic[7] = str(player_entry[p][-3][0]) + ' Tage ' + str(
                    player_entry[p][-3][1]) + ' Std'
                not_first_row_player_dic[8] = player_entry[p][-4]
                if first_row_player_dic[1] != '-- (inactive)':
                    ret_dic.append(not_first_row_player_dic)
                print('vorheriges Team: %s (%s) Verlassen: %s Dauer: %s Tage %s Std %s' % (
                    player_entry[p][2], player_entry[p][1], player_entry[p][4], player_entry[p][-3][0],
                    player_entry[p][-3][1], player_entry[p][-4]))
        print("_________________________")
    print(ret_dic)
    return ret_dic


def wrong_steam_id_list(data):
    # useful
    ret_list = []
    # ret_list.append(['Steam_id', 'Player', 'Team', 'Division', 'Teamlink'])
    for div, divdata in data.items():
        for team, teamdata in divdata['Teams'].items():

            if teamdata['Players'] != 'no players, team deleted':
                for player, playerdata in teamdata['Players'].items():
                    player_steamid = playerdata['steam_id']
                    if len(player_steamid) > 1:
                        try:
                            reg = re.search(r'^steam_[0|1]:[0|1]:\d{1,9}$', player_steamid).group()
                        except:
                            ret_list.append([player, player_steamid, team, div, teamdata['link']])
                            # print(r'" {} " | {}   ({} | {} | {})'.format(player_steamid,player,team, div,teamdata['link']))
    return ret_list
