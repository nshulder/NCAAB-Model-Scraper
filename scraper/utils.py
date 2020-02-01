"""
Utilities needed for getting Kenpom and Bart Torvik lines.
"""

import mechanicalsoup
import bs4


def fix_team_names(team):
    """

    Schools with Saint in their name are different between the betting lines and Kenpom/Bart Torvik. Modify the string
    to follow the conventions they use so the lines will be correctly found

    :param team: team name to be string manip'd into something usable
    :return: 'Fixed' team name that follows the naming convention
    """
    mutable_team = list(team.strip())
    if mutable_team[-2] != "'":
        mutable_team[-1] = "'"
        mutable_team.append('s')
        team = ""
        for c in mutable_team:
            if c == '\'':
                team += "'"
            else:
                team += c
    if team != "St. John's":
        team = team.replace("St.", "Saint")  # BartTorvik uses Saint instead of St. (Except for St. Johns lmao)
    return str(team)


def has_numbers(input_string):
    """
    Helper method for identifying the right cells in the return HTML tables.

    :param input_string: Cell contents to check

    :return: true if the string has numbers, false otherwise
    """
    return any(char.isdigit() for char in input_string)


def set_up_odds_dictionary(team_names, odds):
    odds_dictionary = dict()

    count = 0
    for odd in odds:
        for line in odd.contents[0]:
            # Filter out html tags, only want content
            if not(isinstance(line, bs4.element.Tag)):
                split_line = line.split('\n')[0]
                if split_line.find('+') >= 0 or split_line.find('PK') >= 0:
                    count = count + 1
                elif split_line.find('-') >= 0:
                    odds_dictionary[team_names[count].contents[0]] = split_line
                    count = count + 1

    return odds_dictionary


def kenpom_login(email, password):
    """

    Login to Kenpom member area to access the lines behind the paywall

    :param email: email for Kenpom account
    :param password: password for Kenpom account
    :return: browser logged into Kenpom account
    """
    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='MyBot/0.1: mysite.example.com/bot_info',
    )

    browser.open("https://kenpom.com/index.php")
    browser.select_form('form[action="handlers/login_handler.php"]')
    browser["email"] = email
    browser["password"] = password
    resp = browser.submit_selected()

    if resp.status_code != 200:
        raise Exception(
            'Logging in to kenpom.com failed - check that the site is available and your credentials are correct.')

    return browser
