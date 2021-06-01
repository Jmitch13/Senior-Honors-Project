import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup

#Creates the player draft database
PlayerDraft = sqlite3.connect('PlayerDraft.db')

yearList = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']

#Function to create the player draft tables
def player_draft_table(year):
    pd = PlayerDraft.cursor()
    #concanate the string
    table_values = '(Player_Name TEXT, Rank INTEGER, Position TEXT, School TEXT)'  
    pd.execute('CREATE TABLE IF NOT EXISTS _' + year + 'Draft_Class' + table_values)
    pd.close()

#Inserts the data into the table
def data_entry(year, player_name, rank, position, school):
    pd = PlayerDraft.cursor()
    insertStatement = "INSERT INTO _" + year + "Draft_Class (Player_Name, Rank, Position, School) VALUES(?, ?, ?, ?)"
    statTuple = (player_name, rank, position, school)
    pd.execute(insertStatement, statTuple)
    PlayerDraft.commit()
    pd.close()

#Scrapes the internet from Baseball Almanac
def web_scrape(draftList, year):
    source = requests.get('https://www.baseball-almanac.com/draft/baseball-draft.php?yr=' + year).text
    soup = BeautifulSoup(source, "html.parser")
    table = soup.find('table')
    table_rows = table.find_all('tr')
    #Scrape all the data from the table
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text for i in td]
        #Adds the top 200 prospects for every year
        if len(draftList) > 201:
            break            
        draftList.append(row)

#main function to create a database for the top prospects from 2012-2019
def main():
    for i in range(len(yearList)):
        player_draft_table(yearList[i])
        draftList = []
        web_scrape(draftList, yearList[i])
        #removes the heading of the table due to the structure on Baseball Almanac
        draftList.pop(0)
        draftList.pop(0)
        for j in range(len(draftList)):
            data_entry(yearList[i], draftList[j][3], draftList[j][1], draftList[j][5], draftList[j][6])

if __name__ == "__main__":
    main()
