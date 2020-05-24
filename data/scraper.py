#scrape nba teams and 3pt percentages and winning percentages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome('/Users/alsendor/SHIT/999/chromedriver')
driver.get('https://www.basketball-reference.com/leagues/NBA_2020.html')

#Offensive Statistics
teams = driver.find_elements_by_xpath('//div[@id="all_team-stats-per_poss"]//td[@class="left "][@data-stat="team_name"]')
teams_list = []
for t in range(len(teams)):
    name = teams[t].text
    #Check if team has an asterisk
    if name.endswith('*'):
        name = name[:-1]
    teams_list.append(name)

three_pct = driver.find_elements_by_xpath('//div[@id="all_team-stats-per_poss"]//td[@class="right "][@data-stat="fg3_pct"]')
three_pct_list = []
for t in range(len(three_pct)):
    three_pct_list.append(three_pct[t].text)
    
pp100 = driver.find_elements_by_xpath('//div[@id="all_team-stats-per_poss"]//td[@class="right "][@data-stat="pts"]')
pp100_list = []
for t in range(len(pp100)):
    pp100_list.append(pp100[t].text)

#create dataset
data = []
for i in range(len(teams_list)-1):
    temp_data = []
    temp_data.append(teams_list[i])
    temp_data.append(three_pct_list[i])
    temp_data.append(pp100_list[i])
    data.append(temp_data)

#Defensive Statistics
teams_def = driver.find_elements_by_xpath('//div[@id="all_opponent-stats-per_poss"]//td[@class="left "][@data-stat="team_name"]')
teams_def_list = []
for t in range(len(teams_def)):
    name = teams_def[t].text
    #Check if team has an asterisk
    if name.endswith('*'):
        name = name[:-1]
    teams_def_list.append(name)

three_pct_def = driver.find_elements_by_xpath('//div[@id="all_opponent-stats-per_poss"]//td[@class="right "][@data-stat="opp_fg3_pct"]')
three_pct_def_list = []
for t in range(len(three_pct_def)):
    three_pct_def_list.append(three_pct_def[t].text)
    
pp100_def = driver.find_elements_by_xpath('//div[@id="all_opponent-stats-per_poss"]//td[@class="right "][@data-stat="opp_pts"]')
pp100_def_list = []
for t in range(len(pp100_def)):
    pp100_def_list.append(pp100_def[t].text)
    
data_def = []
for i in range(len(teams_def_list)):
    temp_data = []
    temp_data.append(teams_def_list[i])
    temp_data.append(three_pct_def_list[i])
    temp_data.append(pp100_def_list[i])
    data_def.append(temp_data)

df1 = pd.DataFrame(data, columns = ['Teams', '3-pt%', 'Points Per 100 Possessions'])
df1.sort_values(by=['Teams'], inplace=True, ascending=True)

df2 = pd.DataFrame(data_def, columns = ['Teams', 'Opp 3-pt%', 'Opp Points Per 100 Possessions'])
df2.sort_values(by=['Teams'], inplace=True, ascending=True)

#print(data_tuples)
print(df1)
print(df2)

driver.close()

