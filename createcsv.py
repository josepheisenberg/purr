import pandas as pd
import numpy
import csv
import regex
from bs4 import BeautifulSoup as soup
import requests

#This file was created to webscrape data from the purr site to find how many results there
#Are for each of the subject tags

info = pd.read_excel("PURRSubjectTags_wColleges.xlsx") #Read subjects tags / colleges from excel sheet
numpyinfo = info.to_numpy() #Convert info to a numpy array
collegesdict = dict() #Create a dictionary where colleges will be the keys and departments the items
for i in numpyinfo:
    collegesdict[i[1]] = list() #Create a list as the item for each college in the dictionary
for i in numpyinfo:
    collegesdict[i[1]].append(i[0]) #Append department names to each list

depttags = [numpyinfo[i][0] for i in range(len(numpyinfo))] # Create a list with department tags
depttagsdict = dict() #Create a dictionary with department tags as the keys, and website links and number of results as the items
for i in depttags:
    depttagsdict[i] = list() #Establish keys
for i in depttagsdict.keys():
    depttagsdict[i].append("https://purr.purdue.edu/publications/browse?tag="+i) #add link to search for each key
    site_raw = requests.get("https://purr.purdue.edu/publications/browse?tag="+i) #webscrape
    site_soup = soup(site_raw.text, 'html.parser') #parse data
    site_info = site_soup.find("li", {"class":"counter"}) #locate count of results
    results = regex.compile("(<li class=\"counter\">)\s+((Results[\s\w-]+)|(No record found\s+))(<\/li>)") #regex that finds count of results
    match = results.search(str(site_info)) #look for the regex in site_info
    gtwo = match.group(3) #the group containing the number of results
    flag = True
    if(gtwo == None):
        gtwo = match.group(4)
        flag = False #if there are no results, set flag to false
    numresults = regex.compile("of ([\d]+)")
    if(flag):
        nummatch = numresults.search(gtwo)
        depttagsdict[i].append(int(nummatch.group(1))) #add number of results to dict
    else:
        depttagsdict[i].append(0) #add 0 to dict if there are no results
fid = open("table.csv", 'w') #put all the stored info in table.csv
writer=csv.writer(fid)
header = ["Department Tag", "College", "Number of PURR results"] #heading
writer.writerow(header)
for i in collegesdict.keys():
    for j in collegesdict[i]:
        writer.writerow([j, i, depttagsdict[j][1]]) #add dictionary below heading
fid.close() #close file