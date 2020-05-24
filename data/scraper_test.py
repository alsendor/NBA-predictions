#test scraper for warriors players
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('/Users/alsendor/SHIT/999/chromedriver')
driver.get('https://www.basketball-reference.com/teams/GSW/2020.html')

players = driver.find_elements_by_xpath('//div[@id="all_per_game"]//td[@class="left "]')
players_list = []
for p in range(len(players)):
    players_list.append(players[p].text)

print(players_list)

driver.close()
