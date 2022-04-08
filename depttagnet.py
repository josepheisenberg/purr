import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import numpy
import networkx as nx
from bs4 import BeautifulSoup as soup
import requests
import regex


purrnet = Network(height="1000px", width="100%", font_color="black",heading='Departments of each college')
#Create a pyvis network named purrnet

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
graph = nx.Graph() #Create a networkx graph
count = 1 #Keeps track of groups by college with
for j in collegesdict.keys(): #For each college
    bignsize =20 + 3 *len(collegesdict[j]) #College node size based on number of departments
    graph.add_node(j, size=bignsize, title=j, group = count) #Add nodes for the colleges
    for k in collegesdict[j]: #For each department within college j
        numresults = depttagsdict[k][1]
        smallnsize = 10
        if(numresults > 0):
            smallnsize += 2 + 4*numpy.log(numresults)
        graph.add_node(k+" ", size=smallnsize, title=depttagsdict[k][0], group=count) #Create a node for the department. The " " prevents issues with departments/colleges with the same name
        graph.add_edge(j, k+" ", weight = 5) #Create an edge between the above department and its college
    count+=1 #Increment count
purrnet.from_nx(graph) #Convert the networkx graph to the pyvis network
purrnet.show("purrnet.html") #Create and show an html file with the pyvis network

HtmlFile = open("purrnet.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
st.componentsv1.html(source_code, height = 1000)