import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import pandas as pd
import streamlit as st
import numpy
import regex
import nltk
from bs4 import BeautifulSoup as soup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

#This file looks at data from PURR regarding each dataset, its title, abstract, description,
#author, and tags. Currently, this file reads all the data in, and attempts to clean the descriptions
#and then creates a bag of words for these descriptions. 


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
    desc = soup(str(desc))
    text = desc.get_text()
    #filters out links, non-alpha numeric characters, underscores, numbers, and 
    #excessive spaces using refex
    text = regex.sub("(http.+)(\s)", " ", text)
    text = regex.sub("\W", " ", text)
    text = regex.sub("_", " ", text)
    text = regex.sub("\d", " ", text)
    text = regex.sub(" +", " ", text)
    text = text.lower() #set to lowercase
    cleandescriptions.append(text)

bow = CountVectorizer()
bow_matrix = bow.fit_transform(cleandescriptions)
bow_df = pd.DataFrame(bow_matrix.toarray())
print(bow_df.shape)
bow_df.columns = bow.get_feature_names()
bow_df.to_csv("bow.csv")
tfidfvector = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf = tfidfvector.fit(bow_matrix)
print(len(tagset))
