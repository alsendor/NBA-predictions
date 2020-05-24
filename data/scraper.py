#scrape nba teams and 3pt percentages and winning percentages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('/Users/alsendor/SHIT/999/chromedriver')
driver.get('https://www.basketball-reference.com/leagues/NBA_2020.html')

teams = driver.find_elements_by_xpath('//div[@id="all_team-stats-per_game"]//td[@class="left "][@data-stat="team_name"]')
teams_list = []
for t in range(len(teams)):
    name = teams[t].text
    #Check if team has an asterisk
    if name.endswith('*'):
        name = name[:-1]
    teams_list.append(name)

three_pct = driver.find_elements_by_xpath('//div[@id="all_team-stats-per_game"]//td[@class="right "][@data-stat="fg3_pct"]')
three_pct_list = []
for t in range(len(three_pct)):
    three_pct_list.append(three_pct[t].text)

data_tuples = list(zip(teams_list[1:],three_pct_list[1:]))
df = pd.DataFrame(data_tuples, columns = ['Teams', '3-pt %'])

#print(data_tuples)
print(df)

driver.close()

