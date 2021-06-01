import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

# Create the team stat database
TeamStats = sqlite3.connect('TeamSeasonAnnual.db')

# List for the Free Agency Pool
yearList = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

def player_draft_table(year):
    ts = TeamStats.cursor()
    #concanate the string
    table_values = '(Team_Name TEXT, Wins INTEGER, Runs INTEGER, Run_Differential INTEGER, WAR INTEGER, WPA INTEGER, Dollars REAL, Batter TEXT, AVG REAL, OBP REAL, SLG REAL, OPS REAL, wOBA REAL, wRCplus REAL, BBperc TEXT, Kperc TEXT, Spd REAL, Def REAL, BWAR REAL, BWPA REAL, BDollars TEXT, Pitcher TEXT, ERA REAL, ERAminus REAL, WHIP REAL, FIPx REAL, FIPxminus REAL, Kper9 REAL, Kper9plus REAL, HRper9 REAL, GBperc REAL, PWAR REAL, PWPA REAL, PDollars TEXT)'
    ts.execute('CREATE TABLE IF NOT EXISTS _' + year + 'TeamStats' + table_values)
    ts.close()

#36
#Enter the data of a player into the respective table
def data_entry(year, team_name, wins, runs, rd, war, wpa, dollar, batter, avg, obp, slg, ops, woba, wrc, bb, k, spd, defense, bwar, bwpa, bdollar, pitcher, era, eramin, whip, fipx, fipxmin, kper9, kper9plus, hrper9, gbperc, pwar, pwpa, pdollar):
    ts = TeamStats.cursor()
    insertStatement = "INSERT INTO _" + year + "TeamStats (Team_Name, Wins, Runs, Run_Differential, WAR, WPA, Dollars, Batter, AVG, OBP, SLG, OPS, wOBA, wRCplus, BBperc, Kperc, Spd, Def, BWAR, BWPA, BDollars, Pitcher, ERA, ERAminus, WHIP, FIPx, FIPxminus, Kper9, Kper9plus, HRper9, GBperc, PWAR, PWPA, PDollars) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    statTuple = (team_name, wins, runs, rd, war, wpa, dollar, batter, avg, obp, slg, ops, woba, wrc, bb, k, spd, defense, bwar, bwpa, bdollar, pitcher, era, eramin, whip, fipx, fipxmin, kper9, kper9plus, hrper9, gbperc, pwar, pwpa, pdollar)
    ts.execute(insertStatement, statTuple)
    TeamStats.commit()
    ts.close()

def web_scrape(playerList, year):

    source = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c,6,117,62,119,36,301,40,48,63,60,4,59,32,17,42&season=' + year + '&month=0&season1=' + year + '&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31&sort=1,a').text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('table', class_ = 'rgMasterTable')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        del row[:1]
        
        if len(row) != 0:
            row[8] = row[8][:-1]
            if row[10] == '($1.9)':
                row = '$1.9'
            row[10] = row[10][1:]
        #Check to make the correct data is being added
            playerList.append(row)

    source = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=c,12,34,35,23,37,38,50,61,199,58,62,59,60,13,39&season=' + year + '&month=0&season1=' + year + '&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31&sort=1,a').text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('table', class_ = 'rgMasterTable')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        del row[:2]

        if len(row) != 0:
            row[1] = row[1][:-1]
            row[2] = row[2][:-1]
            
            if row[11] == '($20.6)':
                row[11] = '$20.6'
            if row[11] == '($19.0)':
                row[11] = '$19.0'
            row[11] = row[11][1:]
            playerList.append(row)
        #Check to make the correct data is being added



for i in range(len(yearList)):
    playerList = []
    player_draft_table(yearList[i])
    web_scrape(playerList, yearList[i])
    for j in range(30):
        data_entry(yearList[i], playerList[j][0], playerList[j][11], int(playerList[j][13]), int(playerList[j+30][13]) - int(playerList[j][14]), round(float(playerList[j][12]) + float(playerList[j+30][9]), 3), round(float(playerList[j][9]) + float(playerList[j+30][10]), 3), round(float(playerList[j][10]) + float(playerList[j+30][11]), 3), '-', float(playerList[j+30][3]), float(playerList[j+30][4]), float(playerList[j+30][5]), float(playerList[j+30][14]), float(playerList[j+30][6]), int(playerList[j+30][7]), float(playerList[j+30][1]), float(playerList[j+30][2]), float(playerList[j+30][12]), float(playerList[j+30][8]), float(playerList[j+30][9]), float(playerList[j+30][10]), float(playerList[j+30][11]), '-', float(playerList[j][1]), int(playerList[j][2]), float(playerList[j][15]), float(playerList[j][3]), float(playerList[j][4]), float(playerList[j][5]), float(playerList[j][6]), float(playerList[j][7]), float(playerList[j][8]), float(playerList[j][12]), float(playerList[j][9]), float(playerList[j][10]))