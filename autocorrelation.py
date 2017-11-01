# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 15:21:44 2017

@author: DIKONDA
"""

##########################################################################
# program: autocorrelation and cross correlation 
# author: Divya
# date: October 25, 2017
# description:  Calculate the autocorrelation and cross correlation of a time history.
#               The file must have json file input
##########################################################################

# Required packages
import pandas as pd
from datetime import datetime, timedelta
from collections import OrderedDict
import numpy as np
from scipy.stats import rankdata

########################################################################
# Input the json file path with file name
filename = raw_input("Please Enter Path of .json file with filename: ") 

# Read Crime count data from crime_count.json file 
Data = pd.read_json(filename)

# LSOA Names
LSOA_Names = list(Data)

print('Generating Files')

# Dates as index from september 2014 to August 2017
dates = ["2014-09-01", "2017-09-01"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
Dates = OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in xrange((end - start).days)).keys()

Correlation = pd.DataFrame()
Correlation_Rank= pd.DataFrame()

# Loop runs for each LSOA name
for x in range(len(LSOA_Names)):
    Crime_Data = pd.DataFrame(Data[LSOA_Names[x]].values.tolist(), columns=Dates)
    Crime_Data.index=Data.index
    Crime_Data = Crime_Data.transpose()
    data_corr = pd.DataFrame(index = Crime_Data.columns, columns = Crime_Data.columns)
    data_corr_rank = pd.DataFrame(index = Crime_Data.columns, columns = Crime_Data.columns)
  
    for i in range(len(Crime_Data.columns)):                              # Loop for pairwise combination of crime types  
        for j in range(len(Crime_Data.columns)):  
            for k in range(len(Crime_Data.index)):                            # Loop for each time shift
                if(k == 0):
                    data_corr_array = np.array(Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[j]].shift(k).fillna(0)))    # Cross-correlation between each pair of crime type with time shift
                else:
                    data_corr_array = np.append(np.array(Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[j]].shift(k).fillna(0))),data_corr_array)   # Cross-correlation between each pair of crime type with time shift
            data_corr_rank.values[i,j] = rankdata(data_corr_array)
            data_corr.values[i,j] = data_corr_array
    
    data_corr['Crime type 1'] = data_corr.index
    data_corr = pd.melt(data_corr, id_vars='Crime type 1', value_name=LSOA_Names[x], var_name='Crime type 2')
    data_corr_rank['Crime type 1'] = data_corr_rank.index
    data_corr_rank = pd.melt(data_corr_rank, id_vars='Crime type 1', value_name=LSOA_Names[x], var_name='Crime type 2')
    #Correlation: correlation matrix with all possible combinations, Correlation_Rank: Rank of correlation matrix
    if (x == 0):
        Correlation = data_corr
        Correlation_Rank = data_corr_rank

    else:
        Correlation = Correlation.merge(data_corr)
        Correlation_Rank = Correlation_Rank.merge(data_corr_rank)
        
# converting Rank of correlation matrix to JSON file format
Correlation_Rank_Map = Correlation_Rank[Correlation_Rank['Crime type 1'] == Correlation_Rank['Crime type 2']]
Correlation_Rank_Map.index = Correlation_Rank_Map['Crime type 1']
Correlation_Rank_Map = Correlation_Rank_Map.drop(Correlation_Rank_Map.columns[[0, 1]],axis=1)
Correlation_Rank_Map = Correlation_Rank_Map.to_json(orient='columns')

with open("Correlation_Rank_Map.txt", "w") as text_file:
    text_file.write(Correlation_Rank_Map)
    
# To divide the array in each cell to individual value by adding'Time_Shift' column
Correlation = explode(Correlation, LSOA_Names, fill_value='')
Correlation['Time_Shift'] =  (range(len(Dates)) * len(Correlation))[0:len(Correlation)]

Correlation.to_csv('Correlation.csv')

# Getting highly correlated patterns
Correlation_sort = pd.melt(Correlation, id_vars=['Crime type 1','Crime type 2','Time_Shift'], value_vars=LSOA_Names,var_name='LSOA Name', value_name='correlation').sort_values('correlation',ascending=False)
High_Correlation = Correlation_sort[Correlation_sort['correlation']>0]

High_Correlation.to_csv('Top_Correlation.csv')


# Function to convert array in each cell to individual value
def explode(df, lst_cols, fill_value=''):
    # make sure `lst_cols` is a list
    if lst_cols and not isinstance(lst_cols, list):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)

    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()

    if (lens > 0).all():
        # ALL lists in cells aren't empty
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .loc[:, df.columns]
    else:
        # at least one list in cells is empty
        return pd.DataFrame({
            col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
            for col in idx_cols
        }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
          .append(df.loc[lens==0, idx_cols]).fillna(fill_value) \
          .loc[:, df.columns]

print('End of Code') 