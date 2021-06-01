import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

# Create the top 100 database
Top100 = sqlite3.connect('Top100Prospects.db')

#Year list for the top 100 prospects
yearList = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

#Function to create the tables from 2012-2019
def top_100_table(year):
    tp = Top100.cursor()
    #concatenate the string
    table_values = '(Rank INTEGER, Player_Name TEXT, Team TEXT, Organization_Rank TEXT, Age INTEGER, Position TEXT, MLB_Est TEXT)'
    tp.execute('CREATE TABLE IF NOT EXISTS _' + year + 'Top100Prospects' + table_values)
    tp.close()

#Function to enter the data into the respective SQLite table
def data_entry(year, rank, player_name, team, organization_rank, age, position, mlb_est):
    tp = Top100.cursor()
    insertStatement = "INSERT INTO _" + year + "Top100Prospects (Rank, Player_Name, Team, Organization_Rank, Age, Position, MLB_Est) VALUES(?, ?, ?, ?, ?, ?, ?)"
    statTuple = (rank, player_name, team, organization_rank, age, position, mlb_est)
    tp.execute(insertStatement, statTuple)
    Top100.commit()
    tp.close()

#Function to web scrape The Baseball Cube for the top 100 prospects
def web_scrape(playerList, year):
    source = requests.get('http://www.thebaseballcube.com/prospects/years/byYear.asp?Y=' + year + '&Src=ba').text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('table', id = 'grid2')
    table_rows = table.find_all('tr')
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        #Manipulates the data that is not needed
        if len(row) > 9:
            row[9] = row[9][:4]
            row[13] = row[13][:4]
            del row[-2:]
            del row[10:13]
            del row[5:9]
        playerList.append(row)
    #removes the table labels that are not needed
    del playerList[:2]
    del playerList[25]
    del playerList[50]
    del playerList[75]
    del playerList[100]


def main():
    #create the database for every top 100 prospect from 2012-2019
    for i in range(len(yearList)):
        #call the method to create 8 tables
        top_100_table(yearList[i])
        #stores the data of all available free agent    
        playerList = []
        #call web_scrape method
        web_scrape(playerList, yearList[i])
        for j in range(len(playerList)):
            #insert the top100prospect data
            data_entry(yearList[i], int(playerList[j][0]), playerList[j][1], playerList[j][2], playerList[j][3], int(yearList[i]) - int(playerList[j][5]) + 1, playerList[j][4], playerList[j][6])

if __name__ == "__main__":
    main()
