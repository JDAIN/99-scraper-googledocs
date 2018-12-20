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


def check_if_switched_team_more_than_once():
    # TODO rule 24hr
    ret_list = []
    with open('team_player_data.json') as json_data:
        teamdata = json.load(json_data)
    joinleave_player_list = []
    # copys dmgdata
    datasoup_date = copy.deepcopy(teamdata)

    for k, v in teamdata.items():
        for ks, vs in teamdata[k]['Teams'].items():
            # gets only teamdic from dmgdata
            team_dic = teamdata[k]['Teams'][ks]['Players']
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
                    pp = pprint.pformat(sorted_after_joindate,
                                        depth=8, width=500, compact=True)
                    ret_list.append(sorted_after_joindate)

    return ret_list


def check_lower_div_join():
    '''
    Rule: D. IV.
        : Spieler, die zu Beginn oder im Laufe einer jeden Saison in einem Team einer höheren Division vertreten waren, sind in einer niedrigeren Division nicht spielberechtigt.
        : Dies gilt unabhängig davon, ob bereits ein Match in der höheren Division bestritten wurde. Die Regelung ist auch für die Relegationen gültig.
    '''
    # read json data
    ret_list = []
    with open('team_player_data.json') as json_data:
        teamdata = json.load(json_data)
    joinleave_player_list = []
    # copys dmgdata
    datasoup_date = copy.deepcopy(teamdata)

    for k, v in teamdata.items():
        for ks, vs in teamdata[k]['Teams'].items():
            # gets only teamdic from dmgdata
            team_dic = teamdata[k]['Teams'][ks]['Players']
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
                                 vss['time_in_team'],
                                 vss['steam_id']])
                        else:
                            joinleave_player_list.append(
                                [kss, k, ks, vss['join_dates'][0], vss['leave_dates'], v['link'], vs['link'],
                                 vss['time_in_team'],
                                 vss['steam_id']])

    player_counter = Counter(x[0] for x in joinleave_player_list)

    for k, v in player_counter.items():
        # k = playername v = amount
        # if player left or joined more than or two teams in a season print his data
        if v > 1:
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
            for e in sorted_after_joindate:

                if 'Starter' not in e[1]:
                    e.append(int(float(e[1].split()[1])))
                else:
                    e.append(int(7))

                if first:
                    first_e = e
                    first = False

                if first_e[-1] > e[-1]:
                    pp = pprint.pformat(sorted_after_joindate,
                                        depth=8, width=500, compact=True)
                    ret_list.append(sorted_after_joindate)

    return ret_list


# needed for colors :)
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def readable_check_lower_div_join_color():
    # todo add time
    # todo broken
    read_dic = check_lower_div_join()
    # print(len(read_dic))
    for player_entry in read_dic:

        # green+bold + name of player
        print('\033[92m\033[1m%s\033[0m' % (str(player_entry[0][0])))
        if player_entry[0][-2] != '-':
            # steam_id if active
            print(player_entry[0][-2])
        else:
            # player is inactive '-'
            print('-- (inactive)')
        # else:
        # return

        for p in range(len(player_entry)):
            # if player_entry[0][-2] != '-':

            if p == 0 and player_entry[0][-2] != '-':
                print('%saktuelles Team:%s %s %s(%s)%s join: %s %s' % (Color.BOLD, Color.END,
                                                                       player_entry[p][2], Color.YELLOW,
                                                                       player_entry[p][1], Color.END,
                                                                       player_entry[p][3], player_entry[p][-3]))
            else:
                print('%svorheriges Team:%s %s %s(%s)%s leave: %s %s' % (Color.BOLD, Color.END,
                                                                         player_entry[p][2], Color.RED,
                                                                         player_entry[p][1], Color.END,
                                                                         player_entry[p][4], player_entry[p][-3]))
        print("_________________________")


def readable_check_lower_div_join():
    print(
        '\n\n_________________________\n\nRegel: 4. Zusammensetzung der Teams D. Spielertransfers IV.  \nSpieler, die zu Beginn oder im Laufe einer jeden Saison in einem Team einer höheren Division vertreten waren, sind in einer niedrigeren Division nicht spielberechtigt.\n')

    read_dic = check_lower_div_join()
    # print(len(read_dic))
    for player_entry in read_dic:

        # name of player
        print('%s' % (str(player_entry[0][0])))
        if player_entry[0][-2] != '-':
            # steam_id if active
            print(player_entry[0][-2])
        else:
            # player is inactive '-'
            print('-- (inactive)')
        # else:
        # return

        for p in range(len(player_entry)):
            # if player_entry[0][-2] != '-':

            if p == 0 and player_entry[0][-2] != '-':
                print('aktuelles Team: %s (%s) Beitritt: %s Dauer: Aktiv %s' % (
                    player_entry[p][2], player_entry[p][1], player_entry[p][3], player_entry[p][-4]))
            else:
                print('vorheriges Team: %s (%s) Verlassen: %s Dauer: %s Tage %s Std %s' % (
                    player_entry[p][2], player_entry[p][1], player_entry[p][4], player_entry[p][-3][0],
                    player_entry[p][-3][1], player_entry[p][-4]))
        print("_________________________")


def readable99_check_lower_div_join():
    # TODO add time
    # todo broken
    print(
        '\n\n____________________________________________________________\n\nSpieler, die zu Beginn oder im Laufe einer jeden Saison in einem Team einer höheren Division vertreten waren, sind in einer niedrigeren Division nicht spielberechtigt.\n')

    read_dic = check_lower_div_join()
    # print(len(read_dic))
    for player_entry in read_dic:
        # 99dmgbold + name of player
        print('[b]%s[/b]' % (str(player_entry[0][0])))
        if player_entry[0][-2] != '-':
            # steam_id if active
            print(player_entry[0][-2])
        else:
            # player is inactive '-'
            print('-- (inactive)')

    for p in range(len(player_entry)):
        if p == 0 and player_entry[0][-2] != '-':
            print('aktuelles team: [url="%s"]%s[/url] (%s)   Beitritt: %s' % (
                player_entry[p][-3], player_entry[p][2], player_entry[p][1], player_entry[p][3]))
        else:
            print('vorheriges team: [url="%s"]%s[/url] (%s) Verlassen: %s' % (
                player_entry[p][-3], player_entry[p][2], player_entry[p][1], player_entry[p][4]))
        print("_________________________")


def readable_check_if_switched_team_more_than_once():
    print('''Regel: 4. Zusammensetzung der Teams D. Spielertransfer I.
        Das Wechseln des Teams während einer laufenden Saison ist nur ein Mal erlaubt.
        Mehrfacher Wechsel führt zur Sperrung des Spielers für die laufende Saison und Playoffs bzw.Relegationen.\n''')
    read_dic = check_if_switched_team_more_than_once()
    # print(len(read_dic))
    for player_entry in read_dic:

        # name of player
        print('%s' % (str(player_entry[0][0])))
        if player_entry[0][-2] != '-':
            # steam_id if active
            print(player_entry[0][-2])
        else:
            # player is inactive '-'
            print('-- (inactive)')
        # else:
        # return

        for p in range(len(player_entry)):
            # if player_entry[0][-2] != '-':

            if p == 0 and player_entry[0][-2] != '-':
                print('aktuelles Team: %s (%s) Beitritt: %s Dauer: Aktiv %s' % (
                    player_entry[p][2], player_entry[p][1], player_entry[p][3], player_entry[p][-4]))
            else:
                print('vorheriges Team: %s (%s) Verlassen: %s Dauer: %s Tage %s Std %s' % (
                    player_entry[p][2], player_entry[p][1], player_entry[p][4], player_entry[p][-3][0],
                    player_entry[p][-3][1], player_entry[p][-4]))
        print("_________________________")

def wrong_steam_id():
    # useful
    with open('team_player_data.json') as json_data:
        data = json.load(json_data)
    for div, divdata in data.items():
        for team, teamdata in divdata['Teams'].items():
            if teamdata['Players'] != 'no players, team deleted':
                for player, playerdata in teamdata['Players'].items():
                    player_steamid = playerdata['steam_id']
                    if len(player_steamid) > 1:
                        try:
                            reg = re.search(r'^steam_[0|1]:[0|1]:\d{1,9}$', player_steamid).group()
                        except:
                            print(r'" {} " | {}   ({} | {} | {})'.format(player_steamid, player, team, div,
                                                                         teamdata['link']))

if __name__ == '__main__':
    print(
        'Warnung:\n Liste ist nicht zu 100% genau, es sollte nochmal selber überprüft werden, ob es sich wirklich um einen Regelverstoß handelt\n')

    readable_check_if_switched_team_more_than_once()

    readable_check_lower_div_join()
    print('\n\n_____________________________________________\n Wrong SteamIDs')
    wrong_steam_id()
    input('Press Any Key to close...')
