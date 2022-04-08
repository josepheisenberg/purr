import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import numpy
import regex
import nltk


info = pd.read_csv("PURR_datasets_with_title_abstract_description_author_and_tags_04012022_.csv") #Read info from an excel sheet
numpyinfo = info.to_numpy() #Convert info to a numpy array
tags=[]
descriptions = []
titles = []
abstracts = []
for i in range(len(numpyinfo)): #retrieve descriptions and tags
    tags.append(numpyinfo[i][6])
    descriptions.append(numpyinfo[i][5])
    titles.append(numpyinfo[i][3])
    abstracts.append(numpyinfo[i][4])
    
for j in range(len(tags)): #split each item in tags into a list of the tags for a publication
    tags[j] = tags[j].split(", ")

tagset = set() #create a set with every tag
for j in tags:
    for i in j:
        tagset.add(i)
        
cleandescriptions = []
for k in range(len(descriptions)): #clean descriptions
    desc = descriptions[k]