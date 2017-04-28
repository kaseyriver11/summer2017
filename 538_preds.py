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
team_names = pd.read_csv("data/team_names.csv")

                    ###                            ###
                    ### --- TODAYS Predictions --- ###
                    ###                            ###

url = "https://projects.fivethirtyeight.com/2017-mlb-predictions/games/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

## What is today?
#today = calendar.month_name[dt.datetime.now().month] + " " + str(dt.datetime.now().day)
#tomorrow = dt.date.today() + dt.timedelta(days=1)
#tomorrow = calendar.month_name[tomorrow.month] + " " + str(tomorrow.day)

# Grab the Team Names
df = pd.DataFrame(columns=('Away', 'Home'))

text = soup.find_all('p', { 'class' : 'teams-names'})
for i in range(0, len(text)):
    game = text[i].getText(separator=u' ')
    words = game.split()
    if len(words) == 5: 
        teams = [words[0], words[3]]
    if len(words) == 9: 
        teams =[" ".join(words[0:2]), " ".join(words[5:7])]
    if (len(words) == 7) & (words[4] == "at"):
        teams = [" ".join(words[0:2]), words[5]]
    if (len(words) == 7) & (words[4] != "at"):
        teams = [words[0], " ".join(words[5:7])]
    df.loc[i] = teams


# Grab the chance of winning
chance = soup.find_all('p', { 'class' : 'chance' })
away = []
home = []
for i in range(0,len(chance),2):
    away.append(chance[i].getText()[0:2])
    home.append(chance[i+1].getText()[0:2])
df['Away_Chance'] = away 
df['Home_Chance'] = home                  

del(game, home, i, teams, url, words, away)

df = df[:game.shape[0]]
  






