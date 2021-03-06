from lxml import html
from datetime import datetime
from time import sleep
import requests
import subprocess
from position import find_pos
from Result import *

i = datetime.now()
dt = {'year': i.year, 'day': i.day, 'month': i.month}
test = {'year': 2017, 'day': 04, 'month': 3}

FIXTURES_URL = 'http://www.goal.com/en-india/fixtures/'
RESULTS_URL = 'http://www.goal.com/en-india/results/'
TABLES_FIXED = 'http://www.goal.com/en-india/tables/'

HOME_TEAM_XPATH ='//div[@class="module module-team simple home"]/span/text()'
AWAY_TEAM_XPATH ='//div[@class="module module-team simple away"]/span/text()'
RESULT_XPATH = '//td[@class="vs"]/div/text()'
STATUS_PATH = '//td[@class="status"]/text()'
TEAM_RANKWISE_XPATH = '//td[@class="legend team short"]'

IMAGE = "/home/abhishek/Downloads/football.png"


def notification_system(league, find_by):

    print "Loading..",

    url_league = league

    fixtures_page = requests.get(FIXTURES_URL+ url_league)
    fixtures_tree = html.fromstring(fixtures_page.text)

    result_page = requests.get(RESULTS_URL + url_league)
    result_tree = html.fromstring(result_page.text)

    table_page = requests.get(TABLES_FIXED + url_league)
    table_tree = html.fromstring(table_page.text)


    team_home = fixtures_tree.xpath(HOME_TEAM_XPATH)
    team_away = fixtures_tree.xpath(AWAY_TEAM_XPATH)
    total_teams = len(team_home)
    status = fixtures_tree.xpath(STATUS_PATH)
    vs = fixtures_tree.xpath(RESULT_XPATH)
    result = result_tree.xpath(RESULT_XPATH)
    result_team_home = result_tree.xpath(HOME_TEAM_XPATH)
    result_team_away = result_tree.xpath(AWAY_TEAM_XPATH)

    result_total_teams = len(result_team_home)
    teamRank = table_tree.xpath(
        '//td[@class="legend position"]/text()')
    teamPoints = table_tree.xpath('//td[@class="pts-last"]/text()')
    EPL_HREF_CONTAINS_XPATH = '/a[starts-with(@href, "/en-india/teams/england/")]/text()'
    tempTeamName = table_tree.xpath(
        TEAM_RANKWISE_XPATH + EPL_HREF_CONTAINS_XPATH)
    teamName = []
    for temp_team in tempTeamName:
        teamName += [temp_team.split("\n")[1]]

    date_list = fixtures_tree.xpath('//th[@class="comp-date"]/text()')
    time_list = fixtures_tree.xpath('//@data-match-time')
    result_time_list = result_tree.xpath('//@data-match-time')
    result_datelist = result_tree.xpath('//th[@class="status"]/text()')
    real_date = []
    result_real_date = []

    for time in time_list:
        match_details = datetime.fromtimestamp(int(time))
        temp = {
            'month': match_details.month,
            'day': match_details.day,
            'year': match_details.year,
            'time': match_details.strftime('%H:%M')
        }
        real_date.append(temp)

    for t in result_time_list:
        match_details = datetime.fromtimestamp(int(t))
        temp = {
            'month': match_details.month,
            'day': match_details.day,
            'year': match_details.year,
            'time': match_details.strftime('%H:%M')
        }
        result_real_date.append(temp)

        # Function to search for user input team
    def find(hometeam, awayteam, length, filter_by, vs, status):
        for i in range(0, length):
            if hometeam[i] == filter_by or awayteam[i] == filter_by:
                if real_date[i]['year'] == dt['year'] and real_date[i]['month'] == dt['month'] and real_date[i]['day'] == dt['day']:
                    match = hometeam[i] + ' ' + vs[i] + ' ' + awayteam[i] + '\n' + 'at ' + status[i] + ' today'
                    return match

    def find_result(hometeam, awayteam, length, filte_by, result):
        for i in range(0, length):
            if hometeam[i] == filte_by or awayteam[i] == filte_by:
                if result_real_date[i]['year'] == dt['year'] and result_real_date[i]['month'] == \
                        dt['month'] and result_real_date[i]['day'] == dt['day']:
                    match = Result(hometeam[i], awayteam[i], result[i])
                    return match

    my_pos,table = find_pos(find_by, teamName, teamRank, teamPoints)
    standing = []
    for team in table:
        standing.append(team.rank + '. ' + team.name + ' with ' + team.points + 'pts')
    standing = '\n'.join(standing)
    body = 'Current position : \n' + my_pos + '\n' + '-----------------------------------------------\n' + 'Table :\n' + '-------------\n' + standing

    message = find(team_home, team_away, total_teams, find_by, vs, status)
    print message
    result = find_result(result_team_home, result_team_away, result_total_teams, find_by, result)
    if message:
        subprocess.Popen(['notify-send', '-i', IMAGE, message, body])
    sleep(0.15)
    if result:
        result_message = 'Final Score' + '\n' + result.home_team + ' ' + result.result + ' ' + result.away_team
        subprocess.Popen(['notify-send','-i', IMAGE, result_message, body])
    else:
        subprocess.Popen(['notify-send', '-i', IMAGE, 'No reults to show', body])

