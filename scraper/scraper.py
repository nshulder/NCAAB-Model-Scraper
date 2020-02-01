"""
This actually scrapes the lines off of the websites.
"""

import requests
from bs4 import BeautifulSoup
from scraper.utils import has_numbers
from scraper.utils import fix_team_names


def kenpom_line(browser, team):
    """

    Checks the kenpom 'fanmatch' page for expected results for the given team. If the given team is the winner, return
    the expected winning margin (line)

    :param browser: Authenticated browser for access to Kenpom's member area which includes 'FanMatch'
    :param team: Requested line
    :return: winning margin for 'team', if found
    """
    if "St." in team:
        team = fix_team_names(team)

    team = team.replace("State", "St.")  # BartTorvik uses St. for State rather than full State

    browser.open("https://kenpom.com/fanmatch.php")
    page = browser.get_current_page()
    rows = page.find_all("tr")
    for row in rows:
        if row.parent.name == 'tbody':
            for data in row.children:
                if data != '\n':
                    if team in data.contents[0] and '%' in data.contents[0]:
                        idx = 1
                        if len(team.split()) > 1:
                            idx = len(team.split())
                        if len(team.split()) + 2 == len(data.contents[0].split()):
                            score = data.contents[0].split()[idx]
                            winning_score = int(score.split('-')[0])
                            losing_score = int(score.split('-')[1])
                            print(team + ' -' + str(winning_score-losing_score))
                            return winning_score-losing_score


def trank_line(team):
    """

    Checks Bart Torvik's 'today's games' module and finds a match for team under T-Rank Line and returns the line if found

    :param team: Requested line
    :return: Winning margin for 'team' if found
    """
    if "St." in team and team != "St. Francis NY":
        team = fix_team_names(team)

    team = team.replace("State", "St.")  # BartTorvik uses St. for State rather than full State

    # Get page and parse it
    page = requests.get('http://www.barttorvik.com/schedule.php')
    soup = BeautifulSoup(page.text, 'html.parser')

    rows = soup.find_all("a")
    for row in rows:
        if row.parent.name == 'td' and row.contents:
            if team in row.contents[0] and has_numbers(row.contents[0]) and '-' in row.contents[0]:
                idx = 1
                if len(team.split()) > 1:
                    idx = len(team.split())
                if len(team.split()) + 1 == len(row.contents[0].split()):
                    print(team + ' ' + row.contents[0].split()[idx])
                    return float(row.contents[0].split()[idx])


def sangarin_line():
    raise NotImplementedError('Sangarin Support Coming soon')
