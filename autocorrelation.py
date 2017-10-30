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
#               The file must have two columns: time(sec) & amplitude.
##########################################################################

# Required packages

import json
import pandas as pd
import datetime
import numpy as np
import os
########################################################################
# Set Working directory
#os.chdir('C:\\Users\\DIKONDA\\Documents\\Resume\\demystdata')

filename = raw_input("Please Enter Path of .json file with filename: ") 

# Read Crime count data from crime_count.json file 
Data = pd.read_json(filename)

LSOA_Names = list(Data)

from datetime import datetime, timedelta
from collections import OrderedDict
dates = ["2014-09-01", "2017-09-01"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
Dates = OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in xrange((end - start).days)).keys()


for x in range(len(LSOA_Names)):
    Crime_Data = pd.DataFrame(Data[LSOA_Names[x]].values.tolist(), columns=Dates)
    Crime_Data.index=Data.index
    Crime_Data = Crime_Data.transpose()
    Auto_Correlation = pd.DataFrame(index = Crime_Data.index, columns = Crime_Data.columns)
    Auto_Correlation_rank = pd.DataFrame()
    for i in range(len(Crime_Data.columns)):
        for j in range(len(Crime_Data.index)): 
            Auto_Correlation.values[j,i] = Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[i]].shift(j).fillna(0))
        Auto_Correlation_rank = pd.concat([Auto_Correlation.rank(),Auto_Correlation_rank],axis=1)
    Auto_Correlation.index = range(len(Crime_Data.index))
    
    globals()['Auto_Correlation_%s' % LSOA_Names[x]]= Auto_Correlation
    globals()['Auto_Correlation_Rank_%s' % LSOA_Names[x]] = Auto_Correlation_rank
    globals()['Auto_Correlation_%s' % LSOA_Names[x]].to_csv('Auto_Correlation_%s' % LSOA_Names[x] + '.csv')
    globals()['Auto_Correlation_Rank_%s' % LSOA_Names[x]].to_csv('Auto_Correlation_Rank_%s' % LSOA_Names[x] + '.csv')
    
    from scipy.stats import rankdata
    Cross_Correlation = pd.DataFrame(index = Crime_Data.columns, columns = Crime_Data.columns)
    Cross_Correlation_rank = pd.DataFrame(index = Crime_Data.columns, columns = Crime_Data.columns)
    for i in range(len(Crime_Data.columns)):
        for j in range(len(Crime_Data.columns)):
            for k in range(len(Crime_Data.index)):
                if(k == 0):
                    Cross_Correlation_array = np.array(Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[j]].shift(k).fillna(0)))
                else:
                    Cross_Correlation_array = np.append(np.array(Crime_Data[Crime_Data.columns[i]].corr(Crime_Data[Crime_Data.columns[j]].shift(k).fillna(0),method="spearman")),Cross_Correlation_array)
            Cross_Correlation_rank.values[i,j] = rankdata(Cross_Correlation_array)
            Cross_Correlation.values[i,j] = Cross_Correlation_array
    globals()['Cross_Correlation_%s' % LSOA_Names[x]] = Cross_Correlation
    globals()['Cross_Correlation_Rank_%s' % LSOA_Names[x]] = Cross_Correlation_rank
    globals()['Cross_Correlation_%s' % LSOA_Names[x]].to_csv('Cross_Correlation_%s' % LSOA_Names[x] + '.csv')
    globals()['Cross_Correlation_Rank_%s' % LSOA_Names[x]].to_csv('Cross_Correlation_Rank_%s' % LSOA_Names[x] + '.csv')




