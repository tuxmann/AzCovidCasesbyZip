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

#import csv, glob, xlrd
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Finding files\n")
daily_case_files = sorted((glob.glob('ADHS_data/*.xls')))
master_df = pd.DataFrame()
count = 0

# Get the zipcode:cases & put it in a dictionary and build the DF
print("Creating Master Cases DataFrame.\n")
for file in daily_case_files:
	fname = (((str(file)).split('/')[1]).split('.')[0]) # For LINUX
	#fname = (((str(file)).split('\\')[1]).split('.')[0]) # For WINDOWS
	df = pd.read_excel(file)
	ZipCaseDict = dict(zip(df.POSTCODE, df.ConfirmedCaseCount))
	if count == 0:
		master_df = pd.DataFrame(zip(df.POSTCODE, df.ConfirmedCaseCount))
		master_df = master_df.rename(columns={0:'ZipCode',1:fname})
		count += 1
	else:
		master_df[fname] = master_df['ZipCode'].map(ZipCaseDict)
		count += 1

# Remove the word Tribal from zipcodes. Tribal areas are currently
# supressing coronavirus data, so we're blind to these areas.
zip = master_df['ZipCode']
tribal = zip.str.contains('Tribal')
master_df['ZipCode'] = np.where(tribal, zip.str.replace(' Tribal',''), master_df['ZipCode'])

# Replacing supressed data with -100 for future color option.
# Replacing 1-10 value with 10 because we should assume the worst.
master_df = master_df.replace(['Data Suppressed'],'-100')
master_df = master_df.replace(['1-10'],'10')

print("Saving Master DataFrame to disk.\n")
master_df = master_df.set_index('ZipCode')
master_df.to_csv('master_cases.csv')

print("Creating New Cases by Day DataFrame")
# Change all the cell values to INT and calculate the new cases
master_df = master_df.astype(int)
daily_cases_df = master_df.diff(axis=1)
daily_cases_df.to_csv('daily_cases.csv')

print("Program finished. Look for master_cases.csv in this folder.")




#daily_cases_df = daily_cases_df.T
#print(master_df)
#print(daily_cases_df.sum())

#daily_cases_df.plot()
#plt.show()
