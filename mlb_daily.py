# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:24:11 2017

@author: kaseyriver11
"""

import datetime as dt 
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
from fuzzywuzzy import process

cnx = mysql.connector.connect(host='baseball-db.ctxqwovrv2n6.us-east-1.rds.amazonaws.com',
                              user='baseball_proj',
                              password='NCSUMSA2017',
                              database='baseball_db')
cursor = cnx.cursor()

query = ("SELECT * FROM mlb_team_names")
team_names_query = cursor.execute(query)
team_names = pd.DataFrame(cursor.fetchall())
team_names = team_names.rename(columns= {0:'team_id', 1:'team_name', 2:'city', 3:'team_abbr'})

                    ###                      ###
                    ### --- TODAYS GAMES --- ###
                    ###                      ###
# What is today?
month = dt.datetime.now().month
if month < 10:
    month = str(0) + str(month)
year = dt.datetime.now().year; day = dt.datetime.now().day
                      
# Create the URL and Scrap
url = "http://m.mlb.com/schedule/" + str(year) + "/" + month + "/" + str(day) + "/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

## Matchups
today = soup.find_all('table', {'class' : 'data schedule-list'})
text = today[0].find_all('td', {'class' : 'schedule-matchup text-left'})
away = []; home= [];
for i in range(0,len(text)):
    matchup = text[i].getText().split()
    for j in range(0,len(matchup)):
        if matchup[j] == "@":
            away.append(" ".join(matchup[0:j]))
            home.append(" ".join(matchup[(j+1):len(matchup)]))

away = [x.lower() for x in away]
home = [x.lower() for x in home]

#Function to make the team names match the names in our database table
def match_names(scraped_team_names, db_team_names):
  out = []
  for name in scraped_team_names:
    x = fuzzywuzzy.process.extract(name, db_team_names, limit = 1)[0][0]
    out.append(x)

  return pd.DataFrame(out, columns=['team_name'])

away = match_names(away, team_names.team_name)
away = away.merge(team_names, on = 'team_name')
away = away.team_abbr
home = match_names(home, team_names.team_name)
home = home.merge(team_names, on = 'team_name')
home = home.team_abbr


## Times & Date
text = today[0].find_all('td', {'class' : 'schedule-time text-left'})
times = []
for i in range(0,len(text)):
    value = text[i].getText()
    value = value.replace("\n", "")

    times.append(value)

games = pd.DataFrame(columns=('time', 'away', 'home'))
games['time'] = times; games['away'] = away; games['home'] = home
games.insert(0, 'Date', time.strftime("%x")) 
games.insert(0, 'ID', "")
for i in range(0,len(times)):
    times[i] = times[i][0:times[i].index(":")]
games['id'] = month + str(day) + str(year) + "." + games['away'] + "." + games['home'] + "." + times

#del(text, times, away, home, url, r, soup, i, j, matchup, month, value, day, year, team_names)


