# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:25:41 2017

@author: kaseyriver11
"""
    
from bs4 import BeautifulSoup, Comment
import pandas as pd
import requests

# Go to website and create soup
url = "http://www.baseball-reference.com/boxes/ARI/ARI201704250.shtml"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

# Find the comments - as this is where the tables are stored
comments=soup.find_all(string=lambda text:isinstance(text,Comment))
keep = []
for i in range(0,len(comments)):
    print(len(comments[i]))
    if len(comments[i]) > 2000:
        keep.append(i)
comments = [comments[i] for i in keep]   
    
    
##### - Away Team Batting - #####    
s = BeautifulSoup(comments[1], 'lxml')
table = s.find('table'); table_body = table.find('tbody')        

data = []; players = []; position = []
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)   
    cols2 = row.find_all('th')
    cols2 = [ele.text.strip() for ele in cols2][0]
    play = cols2[0:cols2.rfind(' ')]; pos = cols2[(cols2.rfind(' ')+1):]
    players.append(play)
    position.append(pos)

table_header = table.find('thead')    
rows = table_header.find_all('tr')
headers = []   
for row in rows:
    cols = row.find_all('th')
    cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele])
    headers.append(cols)   

aBat = pd.DataFrame(data, columns=headers[0][1:])    
aBat.insert(0, 'Player', players); aBat.insert(1, 'Position', position)
# Remove all people who did not have an at bat
aBat = aBat[aBat['PA'] != '0']   
    
    
##### - Home Team Batting - #####    
s = BeautifulSoup(comments[2], 'lxml')
table = s.find('table'); table_body = table.find('tbody')        

data = []; players = []; position = []
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)   
    cols2 = row.find_all('th')
    cols2 = [ele.text.strip() for ele in cols2][0]
    play = cols2[0:cols2.rfind(' ')]; pos = cols2[(cols2.rfind(' ')+1):]
    players.append(play)
    position.append(pos)

table_header = table.find('thead')    
rows = table_header.find_all('tr')
headers = []   
for row in rows:
    cols = row.find_all('th')
    cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele])
    headers.append(cols)   

hBat = pd.DataFrame(data, columns=headers[0][1:])    
hBat.insert(0, 'Player', players); hBat.insert(1, 'Position', position)
# Remove all people who did not have an at bat
hBat = hBat[hBat['PA'] != '0']      
    
    
##### - Away Team Pitching - #####    
s = BeautifulSoup(comments[3], 'lxml')
table = s.find_all('table')
table_body = table[0].find('tbody')   

data = []; players = []; decision = []
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)   
    cols2 = row.find_all('th')
    cols2 = [ele.text.strip() for ele in cols2][0]
    if cols2.find(',') == -1:
        play = cols2; dec = ""
    if cols2.find(',') != -1:
        play = cols2[0:cols2.find(',')]; dec = cols2[cols2.find(',')+2]
    players.append(play)
    decision.append(dec)  
  
table_header = table[0].find('thead')    
rows = table_header.find_all('tr')
headers = []   
for row in rows:
    cols = row.find_all('th')
    cols = [ele.text.strip() for ele in cols]
    headers.append(cols)   
    
aPit = pd.DataFrame(data, columns=headers[0][1:])    
aPit.insert(0, 'Player', players); aPit.insert(1, 'Decision', decision)    
    
    
 ##### - Home Team Pitching - #####    
s = BeautifulSoup(comments[3], 'lxml')
table = s.find_all('table')
table_body = table[1].find('tbody')   

data = []; players = []; decision = []
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append(cols)   
    cols2 = row.find_all('th')
    cols2 = [ele.text.strip() for ele in cols2][0]
    if cols2.find(',') == -1:
        play = cols2; dec = ""
    if cols2.find(',') != -1:
        play = cols2[0:cols2.find(',')]; dec = cols2[cols2.find(',')+2]
    players.append(play)
    decision.append(dec)  
  
table_header = table[1].find('thead')    
rows = table_header.find_all('tr')
headers = []   
for row in rows:
    cols = row.find_all('th')
    cols = [ele.text.strip() for ele in cols]
    headers.append(cols)   
    
hPit = pd.DataFrame(data, columns=headers[0][1:])    
hPit.insert(0, 'Player', players); hPit.insert(1, 'Decision', decision)    
    
    
    
    






























