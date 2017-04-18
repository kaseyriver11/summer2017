# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:24:11 2017

@author: kaseyriver11
"""


import datetime as dt 
import calendar
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
# Create the URL and Scrap
url = "http://m.mlb.com/schedule/2017/" + month + "/" + str(dt.datetime.now().day) + "/"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

## Matchups
text = soup.find_all('td', {'class' : 'schedule-matchup text-left'})
away = []; home= [];
for i in range(0,len(text)):
    matchup = text[i].getText().split()
    for j in range(0,len(matchup)):
        if matchup[j] == "@":
            away.append(" ".join(matchup[0:j]))
            home.append(" ".join(matchup[(j+1):len(matchup)]))

## Times & Date
text = soup.find_all('td', {'class' : 'schedule-time text-left'})
times = []
for i in range(0,len(text)):
    value = text[i].getText()
    value = value.replace("\n", "")
    times.append(value)

games = pd.DataFrame(columns=('Away', 'Home', 'Time'))
games['Away'] = away; games['Home'] = home; games['Time'] = times

## Grab Only Todays Games!
daybreaks = []     
for i in range(0,(len(away)-1)):
    if times[i+1][0:times[i+1].index(':')] < times[i][0:times[i].index(':')]:
        daybreaks.append(i+1)
games = games[:daybreaks[0]]
del(text, times, daybreaks, away, home, url, r, soup, i, j, matchup, month, value)


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

df = df[:games.shape[0]] 
  
  
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


df.to_csv("data\\winnings_4.14.2017.csv")






