import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

# Create the pitcher pool database
PitcherPool = sqlite3.connect('TeamPitcherPool1.db')

yearList = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
teamList = ["Los_Angeles_Angels", "Baltimore_Orioles", "Boston_Red_Sox", "White_Sox", "Cleveland_Indians", "Detroit_Tigers", "Kansas_City_Royals", "Minnesota_Twins", "New_York_Yankees", "Oakland_Athletics", "Seattle_Mariners", "Tamba_Bay_Rays", "Texas_Rangers", "Toronto_Blue_Jays", "Arizona_Diamondbacks", "Atlanta_Braves", "Chicago_Cubs", "Cincinatti_Reds", "Colarado_Rockies", "Miami_Marlins", "Houston_Astros", "Los_Angeles_Dodgers", "Milwaukee_Brewers", "Washingon_Nationals", "New_York_Mets", "Philadelphia_Phillies", "Pittsburgh_Pirates", "St_Louis_Cardinals", "San_Diego_Padres", "San_Francisco_Giants"]
source = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c,3,59,45,118,6,117,42,7,13,36,40,48,60,63&season=2011&month=0&season1=2011&ind=0&team=1&rost=0&age=0&filter=&players=0&startdate=2011-01-01&enddate=2011-12-31"

#Function to create the tables from 2012-2019
def pitcher_pool_table(year, team_name):
    pp = PitcherPool.cursor()
    #concatenate the string
    table_values = '(Player_Name TEXT, Age INTEGER, IP REAL, WAR REAL, WPA REAL, FIPx REAL, FIPXminus REAL, ERA REAL, ERAminus REAL, WHIP REAL, Kper9 REAL, HRper9 REAL, GBperc REAL, Worth TEXT)'
    pp.execute('CREATE TABLE IF NOT EXISTS _' + year + team_name + table_values)
    pp.close()

#Function to enter the data into the respective SQLite table
def data_entry(team_name, year, player_name, age, innings_pitched, war, wpa, fipx, fipx_minus, era, era_minus, whip, kPer9, hrPer9, gb_percentage, worth):
    pp = PitcherPool.cursor()
    insertStatement = "INSERT INTO _" + year + team_name + " (Player_Name, Age, IP, WAR, WPA, FIPx, FIPXminus, ERA, ERAminus, WHIP, Kper9, HRper9, GBperc, Worth) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    statTuple = (player_name, age, innings_pitched, war, wpa, fipx, fipx_minus, era, era_minus, whip, kPer9, hrPer9, gb_percentage, worth)
    pp.execute(insertStatement, statTuple)
    PitcherPool.commit()
    pp.close()

#Function to web scrape FanGraphs for every the pitcher on every team
def web_scrape(playerList, year, team):
    source = requests.get("https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=c,3,59,45,118,6,117,42,7,13,36,40,48,60,63&season=" + year + "&month=0&season1=" + year + "&ind=0&team=" + str(team + 1) + "&rost=0&age=0&filter=&players=0&startdate=2011-01-01&enddate=2011-12-31").text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('table', class_ = 'rgMasterTable')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        if len(row) == 16: 
            playerList.append(row)

#main function to add the desired pitcher stats for every team from 2012 to 2019
def main():
    counter = 0
    #iterate through every year
    for h in range(len(yearList)):
        #iterate through every team
        for i in range(30):
            pitcher_pool_table(yearList[h], teamList[i])
            playerList = []
            web_scrape(playerList, yearList[h], i)
            #iterate through every player
            for k in range(len(playerList)):
                counter += 1
                data_entry(teamList[i], yearList[h], playerList[k][1], playerList[k][2],  playerList[k][10], playerList[k][3], playerList[k][15], playerList[k][4], playerList[k][5], playerList[k][6], playerList[k][7], playerList[k][8], playerList[k][11], playerList[k][12], playerList[k][13], playerList[k][14])
    print(counter)

if __name__ == "__main__":
    main()
