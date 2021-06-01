import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

# Create the batter pool database
BatterPool = sqlite3.connect('TeamBatterPool.db')

positionList = ['c', '1b', '2b', 'ss', '3b', 'rf', 'cf', 'lf', 'dh']
yearList = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
teamList = ["Los_Angeles_Angels", "Baltimore_Orioles", "Boston_Red_Sox", "White_Sox", "Cleveland_Indians", "Detroit_Tigers", "Kansas_City_Royals", "Minnesota_Twins", "New_York_Yankees", "Oakland_Athletics", "Seattle_Mariners", "Tamba_Bay_Rays", "Texas_Rangers", "Toronto_Blue_Jays", "Arizona_Diamondbacks", "Atlanta_Braves", "Chicago_Cubs", "Cincinatti_Reds", "Colarado_Rockies", "Miami_Marlins", "Houston_Astros", "Los_Angeles_Dodgers", "Milwaukee_Brewers", "Washingon_Nationals", "New_York_Mets", "Philadelphia_Phillies", "Pittsburgh_Pirates", "St_Louis_Cardinals", "San_Diego_Padres", "San_Francisco_Giants"]
source = "https://www.baseball-reference.com/players/t/troutmi01.shtml"

def batter_pool_table(team_name, year):
    bp = BatterPool.cursor()
    #concanate the string
    table_values = '(Player_Name TEXT, Age INTEGER, Position TEXT, WAR REAL, WPA REAL, wRCplus REAL, PA INTEGER, AVG REAL, OBP REAL, SLG REAL, OPS REAL, BABIP REAL, wOBA REAL, BBperc REAL, Kperc REAL, SPD REAL, DEF REAL, Worth TEXT)'
    bp.execute('CREATE TABLE IF NOT EXISTS _' + year + team_name + table_values)
    bp.close()

def data_entry(team_name, year, player_name, age, position, war, wpa, rcplus, pa, avg, obp, slg, ops, babip, oba, bbpec, kperc, speed, defense, worth):
    bp = BatterPool.cursor()
    insertStatement = "INSERT INTO _" + year + team_name + " (Player_Name, Age, Position, WAR, WPA, wRCplus, PA, AVG, OBP, SLG, OPS, BABIP, wOBA, BBperc, Kperc, SPD, DEF, Worth) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    statTuple = (player_name, age, position, war, wpa, rcplus, pa, avg, obp, slg, ops, babip, oba, bbpec, kperc, speed, defense, worth)
    bp.execute(insertStatement, statTuple)
    BatterPool.commit()
    bp.close()

def web_scrape(playerList):
    source = requests.get("https://www.baseball-reference.com/players/g/guerrvl01.shtml#all_br-salaries").text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('table', id = 'batting_value')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        #th = tr.find('th')
        row = [i.text for i in td]
        #row.append(th.text)
        playerList.append(row)
    '''
    table = soup.find('table', id = 'batting_standard')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        th = tr.find('th')
        row = [i.text for i in td]
        row.append(th.text)
        playerList.append(row)
    '''

playerList = []
web_scrape(playerList)
print(playerList)
