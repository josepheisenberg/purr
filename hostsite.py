import streamlit.components.v1 as comps
import pyvis

purrnet = open("C:/CS/ILSResearch/purr/purrnet.html", 'r', encoding = 'utf-8')
code = purrnet.read()
comps.html(code)
