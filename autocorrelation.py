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

# Dates as index from september 2014 to August 2017
dates = ["2014-09-01", "2017-09-01"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
Dates = OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in xrange((end - start).days)).keys()

# Loop runs for each LSOA name
for x in range(len(LSOA_Names)):
    Crime_Data = pd.DataFrame(Data[LSOA_Names[x]].values.tolist(), columns=Dates)
    Crime_Data.index=Data.index
    Crime_Data = Crime_Data.transpose()
    Auto_Correlation = pd.DataFrame(index = Crime_Data.index, columns = Crime_Data.columns)
    Auto_Correlation_rank = pd.DataFrame()
    
    for i in range(len(Crime_Data.columns)):         # Loop for each crime type         
        for j in range(len(Crime_Data.index)):       # Loop for each time shift (shift in each month)
            Auto_Correlation.values[j,i] = Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[i]].shift(j).fillna(0))  # Auto-correlation function 
        Auto_Correlation_rank = pd.concat([Auto_Correlation.rank(),Auto_Correlation_rank],axis=1)                                        # Ranking Auto-correlation values for each crime type along time shifts                                   
    Auto_Correlation.index = range(len(Crime_Data.index))
    
    Auto_Correlation.to_csv('Auto_Correlation_%s' % LSOA_Names[x] + '.csv')   # Auto-correlation coefficients
    Auto_Correlation_rank.to_csv('Auto_Correlation_Rank_%s' % LSOA_Names[x] + '.csv')   # rank of auto correlation values
    
    
    Cross_Correlation = pd.DataFrame(index = Crime_Data.columns, columns = Crime_Data.columns)
    Cross_Correlation_rank = pd.DataFrame(index = Crime_Data.columns, columns = Crime_Data.columns)
  
    for i in range(len(Crime_Data.columns)):                              # Loop for pairwise combination of crime types  
        for j in range(len(Crime_Data.columns)):                          
            for k in range(len(Crime_Data.index)):                            # Loop for each time shift
                if(k == 0):
                    Cross_Correlation_array = np.array(Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[j]].shift(k).fillna(0)))    # Cross-correlation between each pair of crime type with time shift
                else:
                    Cross_Correlation_array = np.append(np.array(Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[j]].shift(k).fillna(0),method="spearman")),Cross_Correlation_array)   # Cross-correlation between each pair of crime type with time shift
            Cross_Correlation_rank.values[i,j] = rankdata(Cross_Correlation_array)
            Cross_Correlation.values[i,j] = Cross_Correlation_array

    Cross_Correlation.to_csv('Cross_Correlation_%s' % LSOA_Names[x] + '.csv')                        # Cross-correlation coefficients
    Cross_Correlation_rank.to_csv('Cross_Correlation_Rank_%s' % LSOA_Names[x] + '.csv')              # Rank Cross-correlation values




