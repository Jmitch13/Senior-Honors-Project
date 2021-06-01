import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

# Create the free agency database
FreeAgency = sqlite3.connect('FreeAgency.db')


# List to gather every year from 2012 to 2019
yearList = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

#Create the Free Agency Pool from 2012-2019 
def free_agency_table(year):
    fa = FreeAgency.cursor()
    #concatenate the string
    table_values = '(Player_Name TEXT, Age INTEGER, Position TEXT, FA_Type TEXT, Rank INTEGER, Years INTEGER, Amount TEXT)'
    fa.execute('CREATE TABLE IF NOT EXISTS _' + year + 'FA_Class' + table_values)
    fa.close()

#Enter the data of a player into the respective table
def data_entry(year, player_name, age, position, fa_type, rank, years, amount):
    fa = FreeAgency.cursor()
    insertStatement = "INSERT INTO _" + year + "FA_Class (Player_Name, Age, Position, FA_Type, Rank, Years, Amount) VALUES(?, ?, ?, ?, ?, ?, ?)"
    statTuple = (player_name, age, position, fa_type, rank, years, amount)
    fa.execute(insertStatement, statTuple)
    FreeAgency.commit()
    fa.close()

#Scrapes ESPN for all of the Free Agents for a given year
def web_scrape(playerList, year):
    source = requests.get('http://www.espn.com/mlb/freeagents/_/year/' + year).text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('table')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        #Check to make the correct data is being added
        if row[0] != 'PLAYER' and row[0] != 'Free Agents':
            playerList.append(row)
    #Remove 2011 team and new team
    for i in range(len(playerList)):
        del playerList[i][4:6]

#Function to modify the player list since some of the data from ESPN is not ideal for sorting purposes
def modifyPlayerList(playerList, i, j):
    if playerList[j][3] == 'Signed (A)':
        playerList[j][3] = 'A'
    elif playerList[j][3] == 'Signed (B)':
        playerList[j][3] = 'B'
    else:
        playerList[j][3] = 'None'
    #set the age to the correct number
    playerList[j][2] = int(playerList[j][2])
    playerList[j][2] -= (2020 - int(yearList[i]))
    #set the rank of the players, 51 is a place holder
    if playerList[j][5] == 'NR':
        playerList[j][5] = 51
    else:
        playerList[j][5] = int(playerList[j][5]) 
    playerList[j][5] = 51 if playerList[j][5] == 'NR' else int(playerList[j][5])
    #correct dollar amount FA
    if playerList[j][6] == '--' or playerList[j][6] == 'Minor Lg':
        playerList[j][4] = '0'
    if playerList[j][6] == '--':
        playerList[j][6] = 'Not Signed'

#Main function to create the free agent database which contains every free agent from 2012 to 2019
def main():
    #create the database for every freeagent from 2011-2020
    for i in range(len(yearList)):
        #call the method to create 10 tables
        free_agency_table(yearList[i])
        #stores the data of all available free agent    
        playerList = []
        #call web_scrape method
        web_scrape(playerList, yearList[i])
        print(playerList)
        for j in range(len(playerList)):
            #modify list method
            modifyPlayerList(playerList, i, j)
            #insert the free agent data
            data_entry(yearList[i], playerList[j][0], int(playerList[j][2]), playerList[j][1], playerList[j][3], playerList[j][5], int(playerList[j][4]), playerList[j][6])

if __name__ == "__main__":
    main()