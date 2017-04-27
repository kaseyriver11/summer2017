# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 08:40:47 2017

@author: kaseyriver11
"""

import datetime as dt 
import requests
from bs4 import BeautifulSoup
import pandas as pd

team_names = pd.read_csv("data\\team_names.csv")

url = 'https://rotogrinders.com/lineups/mlb?site=fanduel'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

# Teams
text = soup.find_all('span', {'class' : 'shrt'})
away = []; home = []
for i in range(0,len(text),2):
    away.append(text[i].getText())
    home.append(text[i+1].getText())

# Fix Home and Away Names
for i in range(0,len(away)):
    for j in range(0,len(team_names['Roto'])):
        if away[i] == team_names['Roto'][j]:
            away[i] = team_names['ESPN'][j]
        if home[i] == team_names['Roto'][j]:
            home[i] = team_names['ESPN'][j]
# The times
text = soup.find_all('time')
times = []
for i in range(0,len(text)):
    times.append(text[i].getText())
    times[i] = times[i][0:(len(times[i])-3)]
    
month = dt.datetime.now().month
if month < 10:
    month = str(0) + str(month)
year = dt.datetime.now().year; day = dt.datetime.now().day   
for i in range(0,len(times)):
    times[i] = times[i][0:times[i].index(":")]
ID = []
for i in range(0,len(away)):
    ID.append(month + str(day) + str(year)[2:4] + "." + away[i] + "." + home[i] + "." + times[i]) 

# Players
text = soup.find_all('a', { 'class' : 'player-popup'})
s_p = []; 
s_1 = []; s_2 = []; s_3 = []
s_4 = []; s_5 = []; s_6 = []
s_7 = []; s_8 = []; s_9 = []

players = len(away)*2*10
for i in range(0,players,10):
    s_p.append(text[i].getText())
    s_1.append(text[i+1].getText())
    s_2.append(text[i+2].getText())
    s_3.append(text[i+3].getText())
    s_4.append(text[i+4].getText())
    s_5.append(text[i+5].getText())
    s_6.append(text[i+6].getText())
    s_7.append(text[i+7].getText())
    s_8.append(text[i+8].getText())
    s_9.append(text[i+9].getText())
    

    
lineups = pd.DataFrame(columns=('ID', 'a_s_p'))
lineups['ID'] = ID
# Away
lineups['a_s_p'] = s_p[0:len(s_p):2]
lineups['a_s_1'] = s_1[0:len(s_p):2]
lineups['a_s_2'] = s_2[0:len(s_p):2]
lineups['a_s_3'] = s_3[0:len(s_p):2]
lineups['a_s_4'] = s_4[0:len(s_p):2]
lineups['a_s_5'] = s_5[0:len(s_p):2]
lineups['a_s_6'] = s_6[0:len(s_p):2]
lineups['a_s_7'] = s_7[0:len(s_p):2]
lineups['a_s_8'] = s_8[0:len(s_p):2]
lineups['a_s_9'] = s_9[0:len(s_p):2]
# Home 
lineups['h_s_p'] = s_p[1:len(s_p):2]
lineups['h_s_1'] = s_1[1:len(s_p):2]
lineups['h_s_2'] = s_2[1:len(s_p):2]
lineups['h_s_3'] = s_3[1:len(s_p):2]
lineups['h_s_4'] = s_4[1:len(s_p):2]
lineups['h_s_5'] = s_5[1:len(s_p):2]
lineups['h_s_6'] = s_6[1:len(s_p):2]
lineups['h_s_7'] = s_7[1:len(s_p):2]
lineups['h_s_8'] = s_8[1:len(s_p):2]
lineups['h_s_9'] = s_9[1:len(s_p):2]

del(i,j,away,day,home,month,s_1,s_2,s_3,s_4,s_5,s_6,s_7,s_8,s_9,s_p,times,url,year,players)












