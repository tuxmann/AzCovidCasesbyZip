# Download the .xls file from the website. URL doesn't change each day.
# Change the name of the file to the date.
# Oct 20, 2020
# https://adhsgis.maps.arcgis.com/sharing/rest/content/items/8a2c089c866940bbac0ee70a41ea27bd/data
#
# TODO: Automatically upload files to Github.
import datetime, filecmp, subprocess, time, wget
from pathlib import Path
#from git import Repo

#repo_dir = 'AzCovidCasesbyZip'
#repo = Repo(repo_dir)
#commit_message = "Upload new xls file"
date = datetime.date.today()
time_to_get_file = datetime.time(12).strftime("%H") # 24-hour clock req'd, only hour needed
url = "https://adhsgis.maps.arcgis.com/sharing/rest/content/items/8a2c089c866940bbac0ee70a41ea27bd/data"

#wget.download(url, str(date)+".xls")
#print("\nGetting file: " + str(date)+".xls")
downloaded_file = True      # False means that the file hasn't been DL'd today.
old_date = ""
old_hour = ""

# Get the username & password from the text file. 
def Upload2Git():
	print("Uploading files to Github!")
	fhand = open("../git-userpass.txt")
	count = 0
	for line in fhand:
		count += 1
		line = (line.split(" "))[1].rstrip()
		if count == 1:
			username = line
		if count == 2:
			password = line
		else: 
			continue
	
	# Basic git terminal actions.
	# git add .
	# git pull
	# git commit -m 2020-12-06a.xls
	# git push origin main
	msg = "auto_upload"
	#gitcmd = subprocess.Popen(["git", "pull"])
	gitcmd = subprocess.Popen(["git", "add", "--all"])
	gitcmd = subprocess.Popen(["git", "commit", "-m", msg])
	gitcmd = subprocess.Popen(["git", "push", "origin", "main"],
								stdin =subprocess.PIPE,
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE,
								universal_newlines=True,
								bufsize=0)
	print("\n\n")
	gitcmd.stdin.write(username + "\n")
	print("\n\n")
	gitcmd.stdin.write(password + "\n")
	print("\n\n")
#for line in gitcmd.stdout:
#    print(line.strip())

Upload2Git()
quit()


def GetNewCases():
	print("\nGetting file: " + str(date)+".xls")
	wget.download(url, str(date)+".xls")
	yesterday = str(date - datetime.timedelta(days=1))
	file_size = Path(str(date)+".xls").stat().st_size
	try:
		test = filecmp.cmp(str(date)+'.xls', yesterday+'.xls')
	except FileNotFoundError:
		print("\n ### Yesterday's File Not Found!!! ###")
		test = False
	if file_size < 20000:
		print("                              WARNING!!!! File is smaller than expected!\n"*10)
	if test == True:
		print("                              PROBLEM!!!! File has not changed!\n"*10)


while True:
    current_time = (datetime.datetime.now()).strftime("%H")
    hour = current_time
    date = datetime.date.today()

    if hour != old_hour:
        old_hour = hour
        print ("Current hour is : " + hour)

    if downloaded_file == False and time_to_get_file == current_time:
        GetNewCases()
        downloaded_file = True
    elif old_date != str(date):
        downloaded_file = False
        old_date = str(date)
        print("The date changed to " + str(date))
    else:
        time.sleep(600)
