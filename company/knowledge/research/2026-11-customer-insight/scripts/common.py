import json,re,os
BASE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','raw')
def jl(n): return [json.loads(l) for l in open(os.path.join(BASE,n),encoding='utf-8')]
def mask(s):
    s=re.sub(r'https?://\S+','[URL]',s)
    s=re.sub(r'[\w.+-]+@[\w.-]+','[MAIL]',s)
    s=re.sub(r'\d{2,4}-\d{2,4}-\d{3,4}','[TEL]',s)
    s=re.sub(r'[一-龥A-Za-z]{1,4}(先生|様)','[名前]\\1',s)
    return s
def classify(text,dic):
    return [k for k,ws in dic.items() if any(w in text for w in ws)]
