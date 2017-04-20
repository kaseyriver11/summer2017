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

## Read Team Names
team_names = pd.read_csv("data\\team_names.csv")


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

# Fix Home and Away Names
for i in range(0,len(away)):
    for j in range(0,len(team_names['Team2'])):
        if away[i] == team_names['Team2'][j]:
            away[i] = team_names['ESPN'][j]
        if home[i] == team_names['Team2'][j]:
            home[i] = team_names['ESPN'][j]

## Times & Date
text = today[0].find_all('td', {'class' : 'schedule-time text-left'})
times = []
for i in range(0,len(text)):
    value = text[i].getText()
    value = value.replace("\n", "")
    times.append(value)

games = pd.DataFrame(columns=('Time', 'Away', 'Home'))
games['Time'] = times; games['Away'] = away; games['Home'] = home
games.insert(0, 'Date', time.strftime("%x")) 
games.insert(0, 'ID', "")
for i in range(0,len(times)):
    times[i] = times[i][0:times[i].index(":")]
games['ID'] = month + str(day) + str(year)[2:4] + "." + games['Away'] + "." + games['Home'] + "." + times 

del(text, times, away, home, url, r, soup, i, j, matchup, month, value, day, year, team_names)


