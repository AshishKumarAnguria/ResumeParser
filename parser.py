import re
import textract
import sys
for filename in sys.argv[1:]:
    
        text_raw=str(textract.process((str(filename))))
        
        txt = bytes(text_raw, 'utf-8').decode('unicode_escape')
        text        = ' '.join((txt.split()))
     
        fn=filename.rindex('/')
        
        name=filename[fn+1:]
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
        contact = re.findall(r'[\+\()]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
        corr_contact=[]
        for c in contact:
      
            if len(re.findall(r'\d\d\d\d\d',c))>0 or len(re.findall(r'\d\d\d\d\d\d\d\d\d\d',c))>1 :
                corr_contact.append(c)
        
        print(name)
        print(emails)
        print(corr_contact)
