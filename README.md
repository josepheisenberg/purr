# purr: This is a repository for displaying networks of info related to PURR, Purdue University Research Repository

## Files and their descriptions:

#### Purr_datasets_with_title_abstract_description_author_and_tags_04012022_.csv

All PURR datasets with associated info in a spreadsheet. Text analysis on this is performed in tagnet.py

#### PURRSubjectTafs_wColleges.xlsx

All Purdue departments/research subjects are paired with their associated college in a spreadsheet. This is used to create a network in depttagnet.py.

#### requirements.txt

This file is used when showing the network in a streamlit site and gives streamlit module requirement information

#### createcsv.py

This file creates the table.csv file. It takes the PURRSubjectTags_wColleges.xlsx file and adds a column for the number of results in PURR using webscraping

#### table.csv

A spreadsheet like PURRSubjectTags_wColleges.xlsx that has number of results added. This is created by createcsv.py

#### purrnet.html

The network created from PURRSubjectTafs_wColleges.xlsx in depttagnet.py

#### hostsite.py

This quickly opens purrnet.html without having to runb depttagnet.py

#### depttagnet.py

This file uses webscraping and network creation tools to take the information in PURRSubjectTags_wColleges.xlsx and create a network connecting subjects to colleges and displaying links to the results in PURR for each subject. It is compatible with streamlit. 

#### tagnet.py

This file performs text analysis on Purr_datasets_with_title_abstract_description_author_and_tags_04012022_.csv. It currently cleans the descriptions and creates a bag of words from the cleaned descriptions

#### bow.csv
A bag of words created in tagnet.py using description data in Purr_datasets_with_title_abstract_description_author_and_tags_04012022_.csv.
