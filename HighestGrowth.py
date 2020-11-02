# Look at the spreadsheets and see at the past 2-3 weeks of new cases and presents the
# highest to lowest growth zip codes. If some zip codes has the same number, they could
# be grouped together. Format the colors of the text.
#
# Try to fine today's file. If you can't find todays file, find yesterday's  &
# then go back 1 week from yesterday.
#
# 1. Give user the option to look at city, county, and per capita (100k).
# 2. Give user option to look at specific zip code. Future option: surrounding zips.
# 3. Color outputs and overlay outputs on AZ map.

import datetime, time, openpyxl, xlrd
from openpyxl.utils import get_column_letter, column_index_from_string

week = 7
date = datetime.date.today()
today_file     = str(date) + '.xls'
yesterday_file = str(date - datetime.timedelta(days=1)) + '.xls'
week_ago_file  = str(date - datetime.timedelta(days=week)) + '.xls'

try:
	today_wb = xlrd.open_workbook(today_file)
except FileNotFoundError:
	today_wb = xlrd.open_workbook(yesterday_file)
today_sh = today_wb.sheet_by_index(0)

for header in range(0, today_sh.nrows):
	if "POSTCODE" in str(header):
		
print(str(today_sh.row(0)[0]))

#today_dict = 
