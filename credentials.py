import csv, os, sys

username, password, site_url = None, None, None
if not os.path.exists("credentials.csv"):
    open("credentials.csv", 'w')
    print("credentials.csv didnt exists so it is created please enter details.")
    sys.exit()

with open('credentials.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in data:
        rowdata = row[0].split(",")
        username = rowdata[0]
        password = rowdata[1]
        site_url  = rowdata[2]
