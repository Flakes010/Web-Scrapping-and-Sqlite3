import sqlite3
from bs4 import BeautifulSoup
import requests

# DATABASE
vt = sqlite3.connect("football_datas")
c = vt.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS matches(
        home TEXT, 
        score TEXT, 
        away TEXT,
        date TEXT,
        UNIQUE(home, score, away)
    )""")
    vt.commit()

def insert_row(home, score, away, date):
    c.execute("INSERT OR IGNORE INTO matches VALUES (?, ?, ?, ?)", (home, score, away, date))
    vt.commit()

def delete_table():
    c.execute("DROP TABLE matches")
    vt.commit()
# DATABASE

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
         1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
         2018]

def get_matches(*args):
    for year in args:    
        url = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

        response = requests.get(url)
        content = response.text
        soup = BeautifulSoup(content, 'lxml')
        matches = soup.find_all('div', {"class" : "footballbox"})

        for match in matches:
            home_matches = match.find('th', {"class" : "fhome"}).text.replace('\xa0', '')
            score_matches = match.find('th', {"class" : "fscore"}).text.replace('(a.e.t.)', '')
            away_matches = match.find('th', {"class" : "faway"}).text.replace('\xa0', '')
            date_matches = match.find('div', {"class" : "fdate"}).text

            insert_row(home_matches, score_matches, away_matches, date_matches)

create_table()
for year in years:
    get_matches(year) # can take a while!!!

#get_matches(1994, 2002, 2010)

vt.close()
