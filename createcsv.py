import pandas as pd
import numpy
import csv
import regex
from bs4 import BeautifulSoup as soup
import requests

info = pd.read_excel("PURRSubjectTags_wColleges.xlsx") #Read info from an excel sheet
numpyinfo = info.to_numpy() #Convert info to a numpy array
collegesdict = dict() #Create a dictionary where colleges will be the keys and departments the items
for i in numpyinfo:
    collegesdict[i[1]] = list() #Create a list as the item for each college in the dictionary
for i in numpyinfo:
    collegesdict[i[1]].append(i[0]) #Append department names to each list

depttags = [numpyinfo[i][0] for i in range(len(numpyinfo))]
depttagsdict = dict()
for i in depttags:
    depttagsdict[i] = list()
for i in depttagsdict.keys():
    depttagsdict[i].append("https://purr.purdue.edu/publications/browse?tag="+i)
    site_raw = requests.get("https://purr.purdue.edu/publications/browse?tag="+i)
    site_soup = soup(site_raw.text, 'html.parser')
    site_info = site_soup.find("li", {"class":"counter"})
    results = regex.compile("(<li class=\"counter\">)\s+((Results[\s\w-]+)|(No record found\s+))(<\/li>)")
    match = results.search(str(site_info))
    gtwo = match.group(3)
    flag = True
    if(gtwo == None):
        gtwo = match.group(4)
        flag = False
    numresults = regex.compile("of ([\d]+)")
    if(flag):
        nummatch = numresults.search(gtwo)
        depttagsdict[i].append(int(nummatch.group(1)))
    else:
        depttagsdict[i].append(0)
fid = open("table.csv", 'w')
writer=csv.writer(fid)
header = ["Department Tag", "College", "Number of PURR results"]
writer.writerow(header)
for i in collegesdict.keys():
    for j in collegesdict[i]:
        writer.writerow([j, i, depttagsdict[j][1]])
fid.close()