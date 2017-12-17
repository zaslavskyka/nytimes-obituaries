# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 14:00:20 2017

@author: abdullahts
"""

####Extract --fileid, date, person, title, title blurb, first100ch, full obituary body (excluding metadata)
### Write to CSV

import os
import re
from collections import Counter
from nltk import word_tokenize

source = "/home/alec/Dropbox/NYT Obituaries/allmainfiles_stripped_ind" # File path where all files are located

csvRows = []

for f in os.listdir(source):
    date = ''
    name = ''
    title = ''
    monthlist = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    with open(os.path.join(source,f)) as nfile:
        if len(csvRows)%100==0:
            print(len(csvRows))
        #print(f)
        ###############################
        ##Let's get the person's name
        ###############################
        fullThing = nfile.read()
        head = re.split("(BYLINE|SECTION):", fullThing)[0]
        
        title = re.split("[0-9]+ of [0-9]+ DOCUMENTS", head)[1]
        title = " ".join( title.split("\n")[3:] )
        title = title.strip()
        name = re.split(r'[`\=~!@#$%^&*()_+\[\]{};\'\\:"|<,/<>?]', title)[0]
        
        ###############################
        ## Let's get the dateline and the date only
        ###############################
        headList = head.split("\n")
        newheadList =[]
        for i in headList:
            newheadList.append(i.strip())
        #print(newheadList)
            
        for i in newheadList:
            if len(i)>1:
                parsed = i.split()
                x = parsed[0]
                if x in monthlist:
                    dateline = i
                    
        #print(dateline)
        dateJoin = "|".join([x.lower() for x in monthlist])
        dateJoin = "(%s)" % dateJoin
        finddate = re.search(r'(%s\s+\d+\,\s+\d+)'%dateJoin, head.lower())
        date = finddate.group(1)
        
        if "DATELINE:" in fullThing:
            x = fullThing.split("DATELINE:")[1]
            y = x
        else: 
            x = fullThing.split("LENGTH:")[1] ## Need to think about DATELINE:
            y = x.split("words")[1]
            
        fullBody = re.split("[A-Z]+:", y)[0]
        fullBody = fullBody.replace("\n", " ")
        
        nWordsReport = re.search("LENGTH:\s*([0-9]+)\s*words", fullThing)
        nWordsReport = nWordsReport.group(1)
        
        #nWordsCalc = len( fullBody.split() )
        nWordsCalc  = len(word_tokenize(fullBody))
        word_counter = Counter(fullBody.split())
        distinctWords = len(word_counter)
        
        first500 = fullBody[:500]
        
        csvRows.append([f, date, name, title, fullBody, first500, nWordsReport, nWordsCalc, distinctWords])
       
outFn = "/home/alec/data projects/nytimes-obituaries/data/extracted.all.nice.csv"

from csv import writer
with open(outFn, 'w') as csvF:
    w = writer(csvF)
    w.writerow(["fName", "date", "name", "title", "fullBody", "first500", "nWordsReport", "nWordsCalc", "distinctWords"])
    for r in csvRows:
        w.writerow(r)