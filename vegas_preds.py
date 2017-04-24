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

### Scrap the Vegas Odds
url = "http://www.espn.com/mlb/lines"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

text = soup.find_all('tr', { 'class' : 'oddrow'})

away = []; home = []; away_odds = []; home_odds = [];
for i in range(0, len(text)):
    odds = text[i].getText(separator=u' ').split()
    if odds[0] == "Westgate":
        away.append(odds[1][0:(len(odds[1])-1)])
        away_odds.append(odds[2])
        home.append(odds[3][0:(len(odds[3])-1)])
        home_odds.append(odds[4])
## Fix Team Names
for i in range(0, len(away)):
    for j in range(0, len(team_names['ESPN'])):
        if team_names['ESPN'][j] == away[i]:
            away[i] = team_names['Team'][j]
for i in range(0, len(home)):
    for j in range(0, len(team_names['ESPN'])):
        if team_names['ESPN'][j] == home[i]:
            home[i] = team_names['Team'][j]
   
df2 = pd.DataFrame(columns=('Away', 'Home', 'Away_Odds', 'Home_Odds'))
df2['Away'] = away; df2['Home'] = home; df2['Away_Odds'] = away_odds;  df2['Home_Odds'] = home_odds

#df2 = df2[df2['Away'].isin(df['Away'])]

df = df.sort_values(by = ['Away'])
df2 = df2.sort_values(by = ['Away'])
games = games.sort_values(by = ['Away'])

df = df.reset_index(drop=True)
df2 = df2.reset_index(drop=True)
games = games.reset_index(drop=True)

df['Away_Odds'] = df2['Away_Odds']
df['Home_Odds'] = df2['Home_Odds']
df.insert(0, 'Date', time.strftime("%x")) 
df.insert(1, 'Time', games['Time'])

## Away Numbers
df['Away_Bet'] = 100; df['Away_Winnings'] = 0; df['Away_Projected_Winnings'] = 0;
for i in range(0,len(df['Away_Bet'])):
    if float(df['Away_Odds'][i]) < 0:
        df['Away_Winnings'][i] = -1*df['Away_Bet'][i]/float(df['Away_Odds'][i])*df['Away_Bet'][i] + df['Away_Bet'][i]
    if float(df['Away_Odds'][i]) > 0:
        df['Away_Winnings'][i] = df['Away_Bet'][i] + float(df['Away_Odds'][i])
    df['Away_Projected_Winnings'][i] = float(df['Away_Chance'][i])/100*df['Away_Winnings'][i]

## Home Numbers
df['Home_Bet'] = 100; df['Home_Winnings'] = 0; df['Home_Projected_Winnings'] = 0;
for i in range(0,len(df['Home_Bet'])):
    if float(df['Home_Odds'][i]) < 0:
        df['Home_Winnings'][i] = -1*df['Home_Bet'][i]/float(df['Home_Odds'][i])*df['Home_Bet'][i] + df['Away_Bet'][i]
    if float(df['Home_Odds'][i]) > 0:
        df['Home_Winnings'][i] = df['Home_Bet'][i] + float(df['Home_Odds'][i])
    df['Home_Projected_Winnings'][i] = float(df['Home_Chance'][i])/100*df['Home_Winnings'][i]

## Which bet do I make
df['Decision'] = ""
for i in range(0,len(df['Decision'])):
    away_diff = (df['Away_Projected_Winnings'][i] - df['Away_Bet'][i])
    home_diff = (df['Home_Projected_Winnings'][i] - df['Home_Bet'][i])
    if (away_diff > home_diff) & (away_diff >= 5):
        df['Decision'][i] = "Away"
    elif (home_diff > away_diff) & (home_diff >= 5):
        df['Decision'][i] = "Home"
    else:
        df['Decision'][i] = "None"

df['Bet'] = 0
df['Winnings'] = 0
for i in range(0,len(df['Winnings'])):
    if df['Decision'][i] == "Away":
        df['Bet'][i] = df['Away_Bet'][i]
        df['Winnings'][i] = df['Away_Projected_Winnings'][i]
    if df['Decision'][i] == "Home":
        df['Bet'][i] = df['Home_Bet'][i]
        df['Winnings'][i] = df['Home_Projected_Winnings'][i]

del(away, away_diff, away_odds, home, home_diff, i, j, odds, url)
print(sum(df['Bet']))
print(sum(df['Winnings']))


df.to_csv("data\\winnings2.csv")






