# Crime_Analysis
Project Title: Analysis of crime data of police force UK

Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
See deployment for notes on how to run the project.

Prerequisites

Install python 2.7
Pandas Package to be installed from link "https://pandas.pydata.org/pandas-docs/stable/install.html"

or

Install Anaconda with python 2.7


How to run 'Crime_Correlation.py'

1. Download json file from repository
2. Run the python script
3. It asks to input json file path with filename
4. All ouput files will be saved in the path where python script is running
        Correlation.csv: All possible correlation patterns for each LSAO name and combination of crime types
        Correlation_Rank.csv: Rank correlation patterns for each LSAO name and combination of crime types
        Correlation_Rank_Map.txt: Correlation text file as a input to the HTML page
        
How to run 'crime.HTML'

1. Choose 'Correlation_Rank_Map.txt' files as input to correlation option
2. Choose 'policeGeoJSON.js' as input to Lat/Long option
3. After loading above files, drag down options for choosing LSOA Name, Crime Type and time shift (lag) will be appear
4. By default you can have all the crime types for any LSOA Name and lag value
5. Then click 'Generate Heatmap'
5. Also have options to 
        Toggle Heatmap
        Change gradient
        Change radius
        Change opacity
       
