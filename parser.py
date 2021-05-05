import re
import textract
import sys
import os
from nltk.tag import StanfordNERTagger
import pandas as pd
import textract
#Set environmental variables programmatically.
#Set the classpath to the path where the jar file is located
os.environ['CLASSPATH'] = "stanford-ner-2015-04-20/stanford-ner.jar"

#Set the Stanford models to the path where the models are stored
os.environ['STANFORD_MODELS'] = 'stanford-ner-2015-04-20/classifiers'

#Set the java jdk path
java_path = "/usr/bin/java"
os.environ['JAVAHOME'] = java_path


#Set the path to the model that you would like to use
stanford_classifier  =  'stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz'

#Build NER tagger object
st = StanfordNERTagger(stanford_classifier)
def find_name(txt):
    lines = txt.split('\n')
    c=0
    name=""
    for l in lines:
        l=(l.strip()).replace("b'",'')
        if c>1:
            break
        #print(l)
        tg=st.tag(str(l).split())
        for e in tg:
            t=list(e)
            if c>1:
                break
            if t[1]=='PERSON':
                c+=1
                name+=t[0]+" "
                #print(t)
    return name
for filename in sys.argv[1:]:
    
        text_raw=str(textract.process((str(filename))))
        
        txt = bytes(text_raw, 'utf-8').decode('unicode_escape')
        text        = ' '.join((txt.split()))
     
        
        
        name=find_name(txt)
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
        contact = re.findall(r'[\+\()]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        corr_contact=[]
        for c in contact:
      
            if len(re.findall(r'\d\d\d\d\d',c))>0 or len(re.findall(r'\d\d\d\d\d\d\d\d\d\d',c))>1 :
                corr_contact.append(c)
        
        print("NAME:",name)
        print("EMAIL:",emails)
        print("Contact:",corr_contact)
