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
def get_total_experience(txt):
    lines = txt.split('\n')
    t_p=['till now','present','Till Date','to till']
    x=datetime.now()
    date_check=[]
    T_exp=relativedelta.relativedelta(x,x)
    #print("init:",T_exp)
    sy=2021
    ey=0
    prev=True
    date=[]
    for l in lines:
        l=l.strip()
        l=re.sub(r'[^A-Za-z0-9 /.%]+', '', l)
        
        no_date=["birth",'dob','university',' board ','%','percentage','percent','cpi ','gpa ','cg ','grade','Institute',"date of birth"]
        #print(l)
        if re.compile('|'.join(no_date),re.IGNORECASE).search(l):
            prev=False
            continue
        
        if len(re.findall(r'\d\d\d\d\d',l))>0:
            continue
        if (search_dates(l)) is not None and prev==False:
            prev=True
            continue

        q=re.findall(r'\d\d\d\d',str(l))
        #print(len(list(q)),"->",q)    
         
        if len(q)>0:   
            d=search_dates(l)
            if d is None:
                date=[]
            if d is not None :
                if re.compile('|'.join(t_p),re.IGNORECASE).search(l):
                    d.append(('May 2021',datetime.now()))##change to current month year
                for e in d:
                    e=list(e)
                    if 'in' in e[0]:
                        continue
                    yr=re.findall(r'\d\d\d\d',e[0])

                    if len(yr)>0 and int(yr[0])<2022 and int(yr[0])>1990:
                        
                        y=int(yr[0])

                        try:
                            date.append(e[1])
                            
                            if len(date)==2:
                                if (date[0].year,date[1].year) in date_check:
                                    date=[]
                                    continue
                                
                                #print("f3:",date_check)
                                date_check.append((date[0].year,date[1].year))
            
                        except:
                            pass
                        sy=min(y,sy)
                        ey=max(ey,y)
                        #print(y)
                try:
                    
                    t_experience = relativedelta.relativedelta(date[1], date[0])
                    if len(date)>1:
                        date=[]
                    T_exp+=t_experience
        
                except:
                    pass
                
                
                #print(t)
        
    #print("total experience:",ey,"-",sy,"->",ey-sy)
    #print("total experience-T:",T_exp.years," ",T_exp.months)
    return str(T_exp.years)+"/"+str(T_exp.months)

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
        print("Total experience(year/month):",total_experience)
