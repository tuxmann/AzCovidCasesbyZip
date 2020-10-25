# Download the .xls file from the website. URL doesn't change each day.
# Change the name of the file to the date.
# Oct 20, 2020
# https://adhsgis.maps.arcgis.com/sharing/rest/content/items/8a2c089c866940bbac0ee70a41ea27bd/data
# https://adhsgis.maps.arcgis.com/sharing/rest/content/items/8a2c089c866940bbac0ee70a41ea27bd/data

import datetime, time, wget

date = str(datetime.date.today())
time_to_get_file = datetime.time(12).strftime("%H") # 24-hour clock req'd, only hour needed
url = "https://adhsgis.maps.arcgis.com/sharing/rest/content/items/8a2c089c866940bbac0ee70a41ea27bd/data"

wget.download(url, date+".xls")
print("\nGetting file: " + date+".xls")
downloaded_file = True      # False means that the file hasn't been DL'd today.
old_date = ""
old_hour = ""

while True:
    current_time = (datetime.datetime.now()).strftime("%H")
    hour = current_time
    date = str(datetime.date.today())

    if hour != old_hour:
        old_hour = hour
        print ("Current hour is : " + hour)

    if downloaded_file == False and time_to_get_file == current_time:
        wget.download(url, date+".xls")
        print("\nGetting file: " + date+".xls")
        downloaded_file = True
    elif old_date != date:
        downloaded_file = False
        old_date = date
        print("The date changed to " + date)
    else:
        time.sleep(600)
