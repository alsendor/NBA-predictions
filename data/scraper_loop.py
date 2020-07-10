#scrape nba teams and 3pt percentages and winning percentages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from openpyxl import load_workbook

years = range(2010,2021) #years we will be taking stats from
main_df = pd.DataFrame(columns = ['Year', 'Teams', '3-pt%', 'Points Per 100 Possessions', 'Opp 3-pt%', 'Opp Points Per 100 Possessions'])

for year in years:
    driver = webdriver.Chrome('/Users/alsendor/SHIT/999/chromedriver')
    url_string = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html'
    driver.get(url_string)

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
    for i in range(len(teams_list)):
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

    driver.close()

    df1 = pd.DataFrame(data, columns = ['Teams', '3-pt%', 'Points Per 100 Possessions'])
    df1.sort_values(by=['Teams'], inplace=True, ascending=True)

    df2 = pd.DataFrame(data_def, columns = ['Teams', 'Opp 3-pt%', 'Opp Points Per 100 Possessions'])
    df2.sort_values(by=['Teams'], inplace=True, ascending=True)

    #print(data_tuples)
    #print(df1)
    #print(df2)

    df = pd.merge(df1, df2, on='Teams', how='outer')
    df.insert(0, 'Year', year)
    main_df = pd.concat([main_df,df])

    #get net values
    #df['Net Rating Per 100 Possessions'] = df.apply()
    
    #read existing excel file
    #fix this through excel!
    #writer.book = load_workbook('team-data.xlsx')
    #reader = pd.read_excel(r'team-data.xlsx')

    #Write to excel file
    #df.to_excel(writer, sheet_name='Threes Data', index=False, header=False)
    #df.to_excel(writer, sheet_name='Threes Data', index=False, header=False, startrow=len(reader)+1)
    #writer.save()
print(main_df)
#write to excel
writer = pd.ExcelWriter('team-data.xlsx', engine='xlsxwriter')
main_df.to_excel(writer, sheet_name='Threes Data', index=False)
writer.save()
