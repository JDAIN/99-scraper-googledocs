import copy
import pprint
import re
from collections import Counter
from datetime import datetime


def teamdic_change_datestrings_to_timedate_objects(team_dic):
    """
    Enter a team_dic changes datetime_strings to Datetime objects
    :param team_dic: teamdic
    :return:
    """

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

            # get the items with the indices from the list with joined or left player
            l = []
            for e in indices:
                l.append(joinleave_player_list[e])

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


def readable_check_if_switched_team_more_than_once(data):
    """
    Regel: 4. Zusammensetzung der Teams D. Spielertransfer I.
        Das Wechseln des Teams während einer laufenden Saison ist nur ein Mal erlaubt.
        Mehrfacher Wechsel führt zur Sperrung des Spielers für die laufende Saison und Playoffs bzw.Relegationen.\n
    """

    read_dic = check_if_switched_team_more_than_once(data)

    ret_dic = []
    for player_entry in read_dic:
        first_row_player_dic = [''] * 9

        # name of player
        first_row_player_dic[0] = str(player_entry[0][0])

        if player_entry[0][-2] != '-':
            # steam_id if active

            first_row_player_dic[1] = player_entry[0][-2]
        else:
            # player is inactive '-'
            first_row_player_dic[1] = '-- (inactive)'

        for p in range(len(player_entry)):
            if p == 0 and player_entry[0][-2] != '-':
                first_row_player_dic[2] = player_entry[p][2]  # current team
                first_row_player_dic[3] = player_entry[p][1]  # current div
                first_row_player_dic[5] = player_entry[p][3]  # join date
                first_row_player_dic[7] = 'Aktiv'  # Dauer
                first_row_player_dic[8] = player_entry[p][-4]  # link
                ret_dic.append(first_row_player_dic)
            else:
                not_first_row_player_dic = [''] * 9
                not_first_row_player_dic[2] = player_entry[p][2]  # team
                # current div
                not_first_row_player_dic[3] = first_row_player_dic[3]
                not_first_row_player_dic[4] = player_entry[p][1]  # prev div
                not_first_row_player_dic[6] = player_entry[p][4]  # leavedata
                not_first_row_player_dic[7] = str(player_entry[p][-3][0]) + ' Tage ' + str(
                    player_entry[p][-3][1]) + ' Std'
                not_first_row_player_dic[8] = player_entry[p][-4]
                if first_row_player_dic[1] != '-- (inactive)':
                    ret_dic.append(not_first_row_player_dic)
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
                            # added strip so it removes any leading and ending whitespaces
                            # TODO check for other errors bc of this
                            reg = re.search(
                                r'^steam_[0|1]:[0|1]:\d{1,9}$', player_steamid.strip()).group()
                        except:
                            ret_list.append(
                                [player, player_steamid, team, div, teamdata['link']])
    return ret_list


def check_lower_div_join(teamdata):
    """
    Rule: D. IV.
        : Spieler, die zu Beginn oder im Laufe einer jeden Saison in einem Team einer höheren Division vertreten waren, sind in einer niedrigeren Division nicht spielberechtigt.
        : Dies gilt unabhängig davon, ob bereits ein Match in der höheren Division bestritten wurde. Die Regelung ist auch für die Relegationen gültig.
    """
    # read json data
    ret_list = []

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


def readable_check_lower_div_join(data):
    """
        Rule: D. IV.
            : Spieler, die zu Beginn oder im Laufe einer jeden Saison in einem Team einer höheren Division vertreten waren, sind in einer niedrigeren Division nicht spielberechtigt.
            : Dies gilt unabhängig davon, ob bereits ein Match in der höheren Division bestritten wurde. Die Regelung ist auch für die Relegationen gültig.
    """
    ret_dic = []
    read_dic = check_lower_div_join(data)
    # print(len(read_dic))
    for player_entry in read_dic:
        first_row_player_dic = [''] * 9
        # name of player
        first_row_player_dic[0] = str(player_entry[0][0])
        # print('%s' % (str(player_entry[0][0])))
        if player_entry[0][-2] != '-':
            # steam_id if active
            # print(player_entry[0][-2])
            first_row_player_dic[1] = player_entry[0][-2]
        else:
            # player is inactive '-'
            # print('-- (inactive)')
            first_row_player_dic[1] = '-- (inactive)'

        for p in range(len(player_entry)):
            # if player_entry[0][-2] != '-':
            if p == 0 and player_entry[0][-2] != '-':
                first_row_player_dic[2] = player_entry[p][2]  # current team
                first_row_player_dic[3] = player_entry[p][1]  # current div
                first_row_player_dic[5] = player_entry[p][3]  # join date
                first_row_player_dic[7] = 'Aktiv'  # Dauer
                first_row_player_dic[8] = player_entry[p][-4]  # link
                ret_dic.append(first_row_player_dic)
                # print('aktuelles Team: %s (%s) Beitritt: %s Dauer: Aktiv %s' % (
                #    player_entry[p][2], player_entry[p][1], player_entry[p][3], player_entry[p][-4]))
            else:
                not_first_row_player_dic = [''] * 9
                not_first_row_player_dic[2] = player_entry[p][2]  # team
                # current div
                not_first_row_player_dic[3] = first_row_player_dic[3]
                not_first_row_player_dic[4] = player_entry[p][1]  # prev div
                not_first_row_player_dic[6] = player_entry[p][4]  # leavedata
                not_first_row_player_dic[7] = str(player_entry[p][-3][0]) + ' Tage ' + str(
                    player_entry[p][-3][1]) + ' Std'
                not_first_row_player_dic[8] = player_entry[p][-4]
                if first_row_player_dic[1] != '-- (inactive)':
                    ret_dic.append(not_first_row_player_dic)
        #         print('vorheriges Team: %s (%s) Verlassen: %s Dauer: %s Tage %s Std %s' % (
        #             player_entry[p][2], player_entry[p][1], player_entry[p][4], player_entry[p][-3][0],
        #             player_entry[p][-3][1], player_entry[p][-4]))
        # print("_________________________")
    return ret_dic
