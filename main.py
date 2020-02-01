from scraper.utils import kenpom_login
from scraper.writer import getgames

email = input("Kenpom Email: ")
password = input("Kenpom Password: ")
browser = kenpom_login(email, password)
getgames(browser)
