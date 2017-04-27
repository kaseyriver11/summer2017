# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 09:46:49 2017

@author: kaseyriver11
"""



import datetime as dt 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request as urllib2
import json
from pandas.io.json import json_normalize

### Read in Player IDs

# http://crunchtimebaseball.com/baseball_map.html
players = pd.read_csv('data\\master.csv', encoding = "ISO-8859-1")
pitchers = players[players.mlb_pos == 'P']
pitchers = pitchers[['mlb_name', 'bref_id']].dropna()

for i in range(0,20):
    ID = pitchers['bref_id'][i]

    url = "http://www.baseball-reference.com/players/gl.fcgi?id=" + ID + "&t=p&year=2016"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    
    # Teams
    data = []
    table = soup.find('table', {'class' : 'row_summable sortable stats_table'})
    if type(table) is not None:
        table_body = table.find('tbody')
        
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            #data.append([ele for ele in cols if ele])
            data.append(cols)
            
        headers = []
        table_head = table.find('thead')  
        rows = table_head.find_all('tr')
        for row in rows:
            cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            headers.append([ele for ele in cols if ele])
                
        headers[0].remove('Rk')
        headers[0].insert(4, 'Location')
            
        df = pd.DataFrame(data, columns=headers[0])   
        df.insert(0, 'Player', pitchers.mlb_name[i])
        df.insert(1, 'Year', '2016')    
        
    
    
    
    
    
    






















    
place = players[players['mlb_name'] == 'Dallas Keuchel'].index.tolist()[0]
ID = players['bref_id'][place]
#ID = 518692


url = "http://www.baseball-reference.com/players/gl.fcgi?id=" + ID + "&t=p&year=2016"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')



# Teams
data = []
table = soup.find('table', {'class' : 'row_summable sortable stats_table'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    #data.append([ele for ele in cols if ele])
    data.append(cols)
    
headers = []
table_head = table.find('thead')  
rows = table_head.find_all('tr')
for row in rows:
    cols = row.find_all('th')
    cols = [ele.text.strip() for ele in cols]
    headers.append([ele for ele in cols if ele])
        
headers[0].remove('Rk')
headers[0].insert(4, 'Location')
    
df = pd.DataFrame(data, columns=headers[0])


    
df.insert(0, 'Player', 'Dallas Keuchel')
df.insert(1, 'Year', '2016')    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    