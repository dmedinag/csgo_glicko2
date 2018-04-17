#!/usr/bin/python3
# scrape HLTV results for CS:GO Matches


from requests import get
from bs4 import BeautifulSoup
import re
from csv import DictWriter
from time import gmtime, strftime


def formatMatch(hltvMatch):
    '''
    extract match information and format to list
    '''
    # team names
    hltvMatchNames = [name.get_text() for name in hltvMatch.select('div.team')]
    # match id
    hltvMatchLink = hltvMatch.select('a.a-reset')[0]['href'][9:] # removes the prefix '/matches/'
    hltvMatchId = hltvMatchLink[:hltvMatchLink.index('/')]
    # team ids
    hltvMatchTeamLogoSources = [id_text['src'] for id_text in hltvMatch.select('img.team-logo')]
    hltvMatchTeamIds = [src[src.replace('/', '_', src.count('/')-1).index('/')+1:] for src in hltvMatchTeamLogoSources]
    # event id
    hltvMatchEventLink = hltvMatch.select('td.event img')[0]['src']
    hltvMatchEventLink = hltvMatchEventLink.replace('/', '', hltvMatchEventLink.count('/')-1)
    hltvMatchEventId = hltvMatchEventLink[hltvMatchEventLink.index('/')+1:hltvMatchEventLink.index('.')]
    
    # score(s)
    try:
        # when there was a tie, retrieve the shared score.
        # This will raise an Exception if there was no tie, handled afterwards
        hltvMatchScoreTie = hltvMatch.select('span.score-tie')[0].get_text()
        score1 = hltvMatchScoreTie
        score2 = hltvMatchScoreTie
        hltvMatchTeamWon = 0
    except IndexError:
        # when there wasn't a tie, retrieve the winning team and the different scores
        hltvMatchTeamWon = hltvMatchNames.index(hltvMatch.select('div.team-won')[0].get_text())
        score1 = hltvMatch.select('span.score-won')[0].get_text()
        score2 = hltvMatch.select('span.score-lost')[0].get_text()

    return {
        "team1": hltvMatchNames[hltvMatchTeamWon],
        "team2": hltvMatchNames[1-hltvMatchTeamWon],
        "map": hltvMatch.select('div.map-text')[0].get_text(),
        "event": hltvMatch.select('span.event-name')[0].get_text(),
        "matchid": hltvMatchId,
        "teamid1": hltvMatchTeamIds[hltvMatchTeamWon],
        "teamid2": hltvMatchTeamIds[1-hltvMatchTeamWon],
        "eventid": hltvMatchEventId,
        "score1": score1,
        "score2": score2
    }

def getMatchesOfPage(hltvUrl):
    '''
    gets all matches from one page
    '''
    # get website content
    hltvReq = get(hltvUrl, headers={'User-Agent' : "github users please insert something meaningful here"}) 
    hltvHTML = hltvReq.text
    # obtain the html soup from the raw content
    hltvSoup = BeautifulSoup(hltvHTML, 'html.parser')
    # retrieve a list with a soup per match
    hltvMatches = hltvSoup.select('div.result-con')
    # parse every match html soup into meaningful content
    hltvMatchesFormatted = [formatMatch(hltvMatch) for hltvMatch in hltvMatches]
        
    return hltvMatchesFormatted


def writeMatchesToFile(matchesOfPage, iteration):
    '''
    writes lists to file
    '''
    with open('hltv_org_matches_2018.csv', 'a+') as csvfile:
        hltvWriter = DictWriter(csvfile, matchesOfPage[0].keys())
        if iteration == 0:
            hltvWriter.writeheader()
        for match in matchesOfPage:
            hltvWriter.writerow(match)


for offset in range(0, 9000, 100):
    hltvUrlbase = 'http://www.hltv.org/results?offset='
    hltvUrl = hltvUrlbase + str(offset)
    matchesOfPage = getMatchesOfPage(hltvUrl)
    writeMatchesToFile(matchesOfPage, offset)
    print(strftime("%Y-%m-%d %H:%M:%S: ", gmtime()) + str(offset + 50) + " HLTV CS:GO matches completed.")
