# Script for padding and pivoting timeseries of denugue cases in SP and RJ ###########
# Developed by Denise Cammarota

import numpy as np
import pandas as pd
import os
import sys 
import glob
import epiweeks
from epiweeks import Week, Year


municipios = [355030,330455] # SP, RJ

for municipio in municipios:
    file = './data/raw/serotypes/'+str(municipio)+'_total_serotype'+'.csv'
    file_2 = './data/raw/timeseries/'+str(municipio)+'_total_new'+'.csv'
    years = np.arange(2000,2024,1)
    
    
    # serotypes - extract info from before 2007 to unite with the rest
    df = pd.read_csv(file, delimiter = ';')
    df = df.drop(columns = ['Unnamed: 0'])
    df['SOROTIPO'] = df['SOROTIPO'].replace(' ', 'NONE')
    df = df.pivot(index = ['WEEK_PRI','YEAR_PRI'], columns = 'SOROTIPO', values = 'CASES')
    df = df.fillna(0)
    df= df.reset_index()
    df = df[df['YEAR_PRI'] >= 2007]
    
    
    
    # timeseries
    df_2 = pd.read_csv(file_2, delimiter = ';')
    df_2 = df_2.drop(columns = ['Unnamed: 0'])
    df_2['SOROTIPO'] = 'NONE'
    df_2 = df_2.pivot(index = ['WEEK_PRI','YEAR_PRI'], columns = 'SOROTIPO', values = 'CASES')
    df_2 = df_2.reset_index()
    df_2[['1','2','3','4']] = 0
    df_2 = df_2[['WEEK_PRI','YEAR_PRI','1','2','3','4','NONE']]
    df_2 = df_2[df_2['YEAR_PRI'] < 2007]
    
    # joining everything
    df_total = pd.concat([df,df_2])
    df_total = df_total.reset_index()
    df_total = df_total.drop(columns = ['index'])
    
    
    # padding 
    years = np.arange(2000,2024,1)
    for year in years:
        n_weeks = Year(year).totalweeks()
        print(year,n_weeks)
        for week in range(n_weeks):
            # check if register exists
            print(year,week+1)
            tf = ((df_total['WEEK_PRI'] == week+1) & (df_total['YEAR_PRI'] == year)).any() # true or false
            if(tf == False):
                df_aux =  pd.DataFrame([[week+1,year,0,0,0,0,0]], columns=['WEEK_PRI','YEAR_PRI','1','2','3','4','NONE'])
                df_total = pd.concat([df_total, df_aux])
    
    # calculating total cases
    df_total['TOTAL'] = df_total['NONE'] + df_total['1'] + df_total['2'] + df_total['3'] + df_total['4']
    
    # creating ocurrences for serotypes
    df_total['OCURENCE_1'] = np.where(df_total['1'] >= 1, 1, 0)
    df_total['OCURENCE_2'] = np.where(df_total['2'] >= 1, 1, 0)
    df_total['OCURENCE_3'] = np.where(df_total['3'] >= 1, 1, 0)
    df_total['OCURENCE_4'] = np.where(df_total['4'] >= 1, 1, 0)     
    df_total = df_total.sort_values(by = ['WEEK_PRI','YEAR_PRI'])
    df_total.to_csv('./data/processed/'+str(municipio)+'_total.csv')     
        







