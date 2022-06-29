import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import numpy
import networkx as nx
import streamlit.components.v1 as components
from bs4 import BeautifulSoup as soup
import requests
import regex
import webbrowser

#This file creates a network connecting Purdue Colleges to the research subjects
#related to these colleges and PURR datasets related to these subjects. 


purrnet = Network(height="1000px", width="100%", font_color="black",heading='Departments of each college')
#Create a pyvis network named purrnet

info = pd.read_excel("edited_PURRSubjectTags_wColleges.xlsx") #Read info from an excel sheet
numpyinfo = info.to_numpy() #Convert info to a numpy array
collegesdict = dict() #Create a dictionary where colleges will be the keys and departments the items
for i in numpyinfo:
    collegesdict[i[1]] = list() #Create a list as the item for each college in the dictionary
for i in numpyinfo:
    collegesdict[i[1]].append(i[0]) #Append department names to each list

depttags = [numpyinfo[i][0] for i in range(len(numpyinfo))]
depttagsdict = dict() #creates a dictionary where subjects will be keys and links.number of results will be items
for i in depttags: 
    depttagsdict[i] = list() #establish keys
for i in depttagsdict.keys():
    l = regex.sub(" ", "+", i)
    depttagsdict[i].append("https://purr.lib.purdue.edu/registry?q="+l) #add link to search for each key
    site_raw = requests.get("https://purr.lib.purdue.edu/registry?q="+l, verify = False) #webscrape for number of results
    site_soup = soup(site_raw.text, 'html.parser') #parse data
    site_info = site_soup.find("p", {"class":"ml-2 mt-3"}) #locate count of results
    results = regex.compile("(<p class=\"ml-2 mt-3\">)\s*((Results[\s\w-]+)|(No record found\s+))(<\/p>)") #regex that finds count of results
    match = results.search(str(site_info)) #search for the results regexin site_info
    if(match != None):
        gtwo = match.group(3) #group with number of results
        flag = True
    else:
        flag = False #Set flag to false when there are no results
    numresults = regex.compile("of ([\d]+)")
    if(flag):
        nummatch = numresults.search(gtwo) 
        depttagsdict[i].append(int(nummatch.group(1))) #add number of results to dictionary
    else:
        depttagsdict[i].append(0) #add 0 to dictionary if no results
graph = nx.Graph() #Create a networkx graph
count = 1 #Keeps track of groups by college with
for j in collegesdict.keys(): #For each college
    bignsize =15 + 2 *len(collegesdict[j]) #College node size based on number of departments
    graph.add_node(j, size = bignsize, title=j, group = count, shape = "text") #Add nodes for the colleges
    for k in collegesdict[j]: #For each department within college j
        hyperlink = "<a href="+depttagsdict[k][0]+">View results for: "+k+"</a>" #link for highlighting
        numresults = depttagsdict[k][1]
        smallnsize = 7
        if(numresults > 0):
            smallnsize += 3 + 1.5 * numpy.log(numresults) + numresults/150 #Adjust size based on number of results
        titl = "\nNumber of results: "+str(depttagsdict[k][1])
        graph.add_node(k + " ", size=smallnsize, title=hyperlink + titl, group=count) #Create a node for the department. The " " prevents issues with departments/colleges with the same name
        graph.add_edge(j, k + " ", width = 6) #Create an edge between the above department and its college
    count+=1 #Increment count
purrnet.from_nx(graph) #Convert the networkx graph to the pyvis network
purrnet.show("purrnet.html") #Create and show an html file with the pyvis network

HtmlFile = open("purrnet.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height = 1000, width = 1000)

webbrowser.open_new_tab("purrnet.html")