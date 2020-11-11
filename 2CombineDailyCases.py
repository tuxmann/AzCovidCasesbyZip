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
# https://realpython.com/python-csv/
# https://realpython.com/pandas-read-write-files/
# https://xlrd.readthedocs.io/en/latest/api.html

import csv, glob, xlrd
from xlrd.sheet import ctype_text 

daily_case_files = sorted((glob.glob('./*.xls')))


for file in daily_case_files:
	print(file)
	xlwb = xlrd.open_workbook(file)
	xlsh = xlwb.sheet_by_index(0)
	headers = xlsh.row(0)
	print('(Column #) type:value')
	for idx, cell_obj in enumerate(headers):
		cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
		print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
		if "POSTCODE" in cell_obj.value:
			zipcode_col = idx
			print("Zip found")
		elif "ConfirmedCaseCount" in cell_obj.value:
			CaseCount_col = idx
		else:
			continue
