# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 09:25:22 2023

@author: berar

script will get all data and create a csv called schedule_results
"""

import pandas as pd
import numpy as np

def get_sched_results():
    a = pd.read_csv(rf'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\al.csv')
    n = pd.read_csv(rf'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\nl.csv')
    l = pd.concat([a,n])
    l.to_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\mlb_standings.csv', index=False)
    # t_list = l['AL'].to_list()
    df = pd.DataFrame()
    for index, row in l.iterrows():
        print(row['Division'], row['Tm'], row['League'])
        t = row['Tm']
        print(t)
        url = f'https://www.baseball-reference.com/teams/{t}/2023-schedule-scores.shtml'
        print(url)
        a = pd.read_html(url)
        a = pd.concat(a)
        a['Tm'] = row['Tm']
        a['Division'] = row['Division']
        a['League'] = row['League']
        df = pd.concat([df, a])
    a = df.copy()
    a= a[a['Unnamed: 2']!='preview']
    b = a[a['Gm#']!='Gm#']
    df = b
    df['Division'] = df['League'] + ' ' + df['Division']
    df.to_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\schedule_results.csv', index=False)

def get_teams():
    c = pd.read_html('https://www.baseball-reference.com/')
    d = pd.concat(c)
    g = d.copy()
    g['League'] = np.where(g['AL'].notnull(), 'AL', '')
    g['League'] = np.where(g['NL'].notnull(), 'NL', g['League'])
    div = g[g['League']=='AL']
    
    div['idx'] = div.index
    div = div.drop_duplicates(['idx'], keep='first')
    div['Division'] = pd.NA
    div['Division'] = np.where(div['AL']=='East', 'East', div['Division'])
    div['Division'] = np.where(div['AL']=='Central', 'Central', div['Division'])
    div['Division'] = np.where(div['AL']=='West', 'West', div['Division'])
    div['Division'] = div['Division'].ffill()
    div = div[div['AL']!='West']
    div = div[div['AL']!='Central']
    div = div[div['AL']!='East']
    div['Tm'] = div['AL']
    div = div[['Tm',
              'W',
              'L',
              'GB',
              'SRS',
              'Division',
              'League']]
    div.to_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\al.csv', index=False)
    
    div = g.copy()
    div = div[div['NL'].notnull()]
    div['idx'] = div.index
    div = div.drop_duplicates(['idx'], keep='first')
    div['Division'] = pd.NA
    div['Division'] = np.where(div['NL']=='East', 'East', div['Division'])
    div['Division'] = np.where(div['NL']=='Central', 'Central', div['Division'])
    div['Division'] = np.where(div['NL']=='West', 'West', div['Division'])
    div['Division'] = div['Division'].ffill()
    div = div[div['NL']!='West']
    div = div[div['NL']!='Central']
    div = div[div['NL']!='East']
    div['Tm'] = div['NL']
    div = div[['Tm',
              'W',
              'L',
              'GB',
              'SRS',
              'Division',
              'League']]
    div.to_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\baseball\data\nl.csv', index=False)

def get_attendance():
    c = pd.read_html('https://www.baseball-reference.com/leagues/majors/2023-misc.shtml')
    d = pd.concat(c)
    cap = pd.read_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\mlb_cap.csv')
    tm_abbv = pd.read_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\tm_abbv.csv')
    d = pd.merge(cap, d, how='inner', on=['Tm'])
    d = pd.merge(tm_abbv, d, how='inner', on=['Tm'])
    d['perc_full'] = d['Attend/G'] / d['CAPACITY']
    d.to_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\mlb_att.csv', index=False)

def get_capacity():
    c = pd.read_html('https://sports.betmgm.com/en/blog/mlb/biggest-mlb-stadiums-ranking-by-capacity-bm15/')
    d = pd.concat(c)
    d['Tm'] = d['HOME TEAM']
    d.to_csv(r'C:\Users\berar\Documents\Projects\visualization_demo\mlb_cap.csv', index=False)



def main():
    get_teams()
    get_sched_results()
    get_capacity()
    get_attendance()
