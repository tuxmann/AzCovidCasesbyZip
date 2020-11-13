# This script will combine the daily cases into one file so that the data is cleaned up.
# To make the script efficient, the newest daily cases will be put on the left most side.
# The script will see if file "master_cases.csv" is made and will make it if it doesn't
# exist. All the .xls files in the folder will be found, opened and then merged into the
# master file.
#
### NOTE: openpyxl not used because it doesn't support the older XLS file format ###
#
# Example CSV Case structure:
#
# "POSTCODE","Today's Date'","Today - 1","Today - 2","Today - 3","Today - 4"
# "85003","555","444","333","222","111"
#
# Cases that are not an integer shall be thrown out. There are many zipcodes where
# data is being supressed or not reported. 
#
# Resources:
# https://blogs.harvard.edu/rprasad/2014/06/16/reading-excel-with-python-xlrd/
# https://realpython.com/learning-paths/pandas-data-science/
# https://realpython.com/pandas-read-write-files/
# https://xlrd.readthedocs.io/en/latest/api.html

import csv, glob, xlrd
import pandas as pd
from xlrd.sheet import ctype_text 

daily_case_files = sorted((glob.glob('./*.xls')))
master_df = pd.DataFrame()
count = 0

# Get the zipcode:cases & put it in a dictionary and build the DF
for file in daily_case_files:
	fname = (((str(file)).split('/')[1]).split('.')[0]) # For LINUX
	fname = (((str(file)).split('\\')[1]).split('.')[0]) # For WINDOWS
	df = pd.read_excel(file)
	ZipCaseDict = dict(zip(df.POSTCODE, df.ConfirmedCaseCount))
	if count == 0:
		master_df = pd.DataFrame(zip(df.POSTCODE, df.ConfirmedCaseCount))
		master_df = master_df.rename(columns={0:'ZipCode',1:fname})
		print(master_df)
		count += 1
	else:
		master_df[fname] = master_df['ZipCode'].map(ZipCaseDict)
		count += 1

print(master_df)
master_df.to_csv('master_cases.csv')
