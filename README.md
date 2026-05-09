# Web Services and Web Data Search Engine Tool
Tool that crawls a web page, constructs an inverted index, and provides search commands through a command line interface
---

## Setup

pip install -r requirements.txt
python src/main.py


## Commands

### Build
Crawls the site and creates `data/index.json`.
build

### Load
Loads the previously saved index.
load

### Print
Displays inverted index for a given word
print life

### Find
Displays the urls of pages that contain all the words 
find life truth

### Help
Displays possible commands

### Exit
exit

---


## Architecture Overview

### src

#### crawler.py
- Crawls pages using BFS
- Extracts text and links using BeautifulSoup
- Handles network and page errors
- Enforces politiness delay between requests

#### indexer.py
Two-phase index creation:

1. Temporary dict-of-dicts  
   Efficient for counting and updating:
   index[word][url] = { freq, positions }

2. Final posting lists  
   Sorted lists for efficient search:
   index[word] = [ {url, freq, positions}, ... ]

#### search.py
- `print` returns the posting list for a single term  
- `find` returns intersection of urls across all terms

#### main.py
Command line interface

### tests

Contains test files for crawler, indexer and search functions. 

### data

#### index.json
Final inverted index created using command line interface

---

## Use of Gen AI

AI allowed for rapid initial development, producing functional code quickly.
I then tested and reviewed the code myself, finding gaps where the code didn't meet the requirements (such as the command line interface shell).
AI benefited my learning by explaining how BeautifulSoup works,  as well as talking me through the structure of the search logic. This was more efficient  than online code sources because I can ask follow up questions and get direct answers straight away. However, AI tends to be overly agreeable, so I made sure to verify decisions myself. An example is the inverted index data structure choice. 
Initial AI generated code used a dictionary of dictionaries. After researching standard practices, I then enforced the use of posting lists, improving algorithm efficency and matching standard information retrieval conventions.