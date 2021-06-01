import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

# Create the free agency database
International = sqlite3.connect('InternationalProspects.db')


# List for the Free Agency Pool
yearList = ['2015', '2016', '2017', '2018', '2019']

#Create the International Table from 2015-2019 
def international_table(year):
    ip = International.cursor()
    #concanate the string
    table_values = '(Rank INTEGER, Player_Name TEXT, Position TEXT, Age INTEGER, Projected_Team TEXT, Future_Value TEXT)'
    ip.execute('CREATE TABLE IF NOT EXISTS _' + year + 'TopInternationalClass' + table_values)
    ip.close()

#Enter the data of a player into the respective table
def data_entry(year, rank, player_name, position, age, proj_team, fut_val):
    ip = International.cursor()
    #need the underscore because a table can't start with a number
    insertStatement = "INSERT INTO _" + year + "International_Prospects (Rank, Player_Name, Team, Organization_Rank, Age, Position, MLB_Est) VALUES(?, ?, ?, ?, ?, ?, ?)"
    statTuple = (rank, player_name, position, age, proj_team, fut_val)
    ip.execute(insertStatement, statTuple)
    International.commit()
    ip.close()

#Scrapes ESPN for all of the Free Agents for a given year
def web_scrape(playerList, year):
    #URL changes based on the year
    source = requests.get('https://www.fangraphs.com/prospects/the-board/' + year + '-international/summary?sort=-1,1&type=0&pageitems=200&pg=0').text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find_all('table')
    for table_rows in table:
        table_row = table_rows.find_all('tr')
        #Scrape all the data from the table
        for tr in table_row:
            td = tr.find_all('td')
            row = [i.text for i in td]
            playerList.append(row)

#main function to create the database of all the top international free agents from 2015-2019
def main():
    #5 tables will be created in sqLite with all available international free agents from fangraphs 
    for i in range(len(yearList)):
        international_table(yearList[i])

if __name__ == "__main__":
    main()