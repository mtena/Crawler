import requests
import re
import sys, getopt
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

def main(first,Words,url,section):
    #default to ten
    numOfWords=10

    #Ensures correct first arg is 1 or larger
    try:
        strFirstArg=first
        if(strFirstArg.isnumeric()):
            numOfWordsPreCheck=int(first)
            if(numOfWordsPreCheck>0):    
                numOfWords=numOfWordsPreCheck
        else:
            print("First arg is invaid, must be int greater than 0.")
    except:
        print("First arg is invaid, must be int greater than 0.")
   
    cleanLisfOfBandedWords=Clean_words(Words) 
   
   
    htmlRequest = requests.get(url).text
    goodSoup = BeautifulSoup(htmlRequest, 'html.parser')#whole html
    table = goodSoup.findAll('div',{'class':'mw-body-content mw-content-ltr'})#content protion
     
    wordList = []
    CleanwordList=[]

    flag=False
    for each_text in table:
        content = each_text.findAll(['h2', 'p','div','h3'])
        
        for row in content:    
            try:
                if(row.span!=None):
                    if(row.span.attrs['class'][0]=="mw-headline"):
                        if(row.span.attrs['id']==section):
                            #alows the parser to start adding word once the right section had been found
                            flag=True
                        else:
                            flag=False
                   
                elif(flag):
                    contents = row.text
                    words=contents.lower().split()
                    for eachWord in words:
                        wordList.append(eachWord)
            except:
                X=1
               
    CleanwordList=Clean_words(wordList)
        
    wordCount = {}
    for word in CleanwordList:
        if word in wordCount:
            wordCount[word] += 1
        elif(word not in cleanLisfOfBandedWords):
            wordCount[word] = 1
 

    c = Counter(wordCount)
 
    # returns the most occurring elements
    top = c.most_common(numOfWords)
    print(top)


#gets rid of odd characters
def Clean_words(list):
    cleanList= []
    for word in list:

        input = word.lower()
        s = re.sub(r'[^a-z0-9]', '', input)
        
        if len(s) > 0:
            cleanList.append(s)
    return cleanList



if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Microsoft"
    section='History'
    main(sys.argv[1],sys.argv[2:],url,section)