from Team import *


def find_pos(find_by, teamNames, teamRank, teamPoints):
    table = []
    for i in range(0, len(teamNames)):
        if find_by == teamNames[i]:
            my_pos =  teamRank[i] + '. ' + teamNames[i] + ' with ' + teamPoints[i] + 'pts'
    for i in range(0, 5):
        table.append(Team(teamNames[i], teamRank[i], teamPoints[i]))
    return my_pos,table