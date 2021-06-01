import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

# Create the Cumulative database
CTeamStats = sqlite3.connect('CumulativeTeamStats.db')

# This vector will be used to collect every team from 2012 to 2019
yearList = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

#Function to create the tables from 2012-2019
def cumulative_team_stats_table():
    #cts -> cumulative team stats
    cts = CTeamStats.cursor() 
    table_values = '(Team_Name TEXT, Wins INTEGER, Runs INTEGER, Run_Differential INTEGER, WAR INTEGER, WPA INTEGER, Dollars REAL, Batter TEXT, AVG REAL, OBP REAL, SLG REAL, OPS REAL, wOBA REAL, wRCplus REAL, BBperc TEXT, Kperc TEXT, Spd REAL, Def REAL, BWAR REAL, BWPA REAL, BDollars TEXT, Pitcher TEXT, ERA REAL, ERAminus REAL, WHIP REAL, FIPx REAL, FIPxminus REAL, Kper9 REAL, Kper9plus REAL, HRper9 REAL, GBperc REAL, PWAR REAL, PWPA REAL, PDollars TEXT)'
    #concatenate the string
    cts.execute('CREATE TABLE IF NOT EXISTS Cumulative_Team_Stats' + table_values)
    cts.close()

#Fucntion used to enter the data of a team into the cts database
def data_entry(year, team_name, wins, runs, rd, war, wpa, dollar, batter, avg, obp, slg, ops, woba, wrc, bb, k, spd, defense, bwar, bwpa, bdollar, pitcher, era, eramin, whip, fipx, fipxmin, kper9, kper9plus, hrper9, gbperc, pwar, pwpa, pdollar):
    cts = CTeamStats.cursor()
    insertStatement = "INSERT INTO Cumulative_Team_Stats (Team_Name, Wins, Runs, Run_Differential, WAR, WPA, Dollars, Batter, AVG, OBP, SLG, OPS, wOBA, wRCplus, BBperc, Kperc, Spd, Def, BWAR, BWPA, BDollars, Pitcher, ERA, ERAminus, WHIP, FIPx, FIPxminus, Kper9, Kper9plus, HRper9, GBperc, PWAR, PWPA, PDollars) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    statTuple = (year + team_name, wins, runs, rd, war, wpa, dollar, batter, avg, obp, slg, ops, woba, wrc, bb, k, spd, defense, bwar, bwpa, bdollar, pitcher, era, eramin, whip, fipx, fipxmin, kper9, kper9plus, hrper9, gbperc, pwar, pwpa, pdollar)
    cts.execute(insertStatement, statTuple)
    CTeamStats.commit()
    cts.close()

#Function used to scrape fangraphs to get all of the desired team statistics
def web_scrape(teamList, year):
    #adds all the pitcher stats from the teams
    source = requests.get('https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c,6,117,62,119,36,301,40,48,63,60,4,59,32,17,42&season=' + year + '&month=0&season1=' + year + '&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate=2019-01-01&enddate=2019-12-31&sort=1,a').text
    soup = BeautifulSoup(source, "html.parser")
    #use the identifier class to scrape the right table
    table = soup.find('table', class_ = 'rgMasterTable')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        del row[:1]
        #Simple conditional checks to make sure all the data looks the same
        if len(row) != 0:
            row[8] = row[8][:-1]
            if row[10] == '($1.9)':
                row = '$1.9'
            row[10] = row[10][1:]
            teamList.append(row)
    #adds all the batter stats to the teams
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
            teamList.append(row)
        #Check to make the correct data is being added

#Main Program
def main(): 
    cumulative_team_stats_table()
    #for every year in the vector yearList
    for i in range(len(yearList)):
        teamList = []
        #Scrape the table for the entire year
        web_scrape(teamList, yearList[i])
        #Enter the data for all 30 major league teams
        for j in range(30):
            data_entry(yearList[i], teamList[j][0], teamList[j][11], int(teamList[j][13]), int(teamList[j+30][13]) - int(teamList[j][14]), round(float(teamList[j][12]) + float(teamList[j+30][9]), 3), round(float(teamList[j][9]) + float(teamList[j+30][10]), 3), round(float(teamList[j][10]) + float(teamList[j+30][11]), 3), '-', float(teamList[j+30][3]), float(teamList[j+30][4]), float(teamList[j+30][5]), float(teamList[j+30][14]), float(teamList[j+30][6]), int(teamList[j+30][7]), float(teamList[j+30][1]), float(teamList[j+30][2]), float(teamList[j+30][12]), float(teamList[j+30][8]), float(teamList[j+30][9]), float(teamList[j+30][10]), float(teamList[j+30][11]), '-', float(teamList[j][1]), int(teamList[j][2]), float(teamList[j][15]), float(teamList[j][3]), float(teamList[j][4]), float(teamList[j][5]), float(teamList[j][6]), float(teamList[j][7]), float(teamList[j][8]), float(teamList[j][12]), float(teamList[j][9]), float(teamList[j][10]))

if __name__ == "__main__":
    main()
