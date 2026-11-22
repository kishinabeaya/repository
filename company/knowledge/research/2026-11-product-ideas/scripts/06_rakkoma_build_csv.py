"""ラッコM&A: 一覧(list.json) + 個別ページ(det/*.html) -> rakkoma-sites.csv
使い方: python3 -I 06_rakkoma_build_csv.py <work_dir> <out_csv>
一覧カードに無い項目(運営開始時期・カテゴリ・収益モデル・運営状況・PV・工数の記載)は、個別ページを取得した案件(Webサイト・アプリで売上>0)のみ。"""
import re,html,json,sys,os,csv
w,out=sys.argv[1],sys.argv[2]
rows=json.load(open(w+'/list.json'))
KIND={'desktop':'サイト・アプリ等(Web)','user':'SNS・YouTube等アカウント','mobile-alt':'アプリ'}
def num(s): return int(s.replace(',','')) if s not in (None,'') else None
def lines(path):
    t=open(path).read()
    t=re.sub(r'<(script|style)[^>]*>.*?</\1>','',t,flags=re.S)
    t=re.sub(r'<[^>]+>','\n',t); t=html.unescape(t)
    return [x.strip() for x in t.split('\n') if x.strip()]
def after(L,key,n=1):
    return L[L.index(key)+n] if key in L else ''
def plat(title):
    for k,v in [('YouTube','YouTube'),('ユーチューブ','YouTube'),('TikTok','TikTok'),('Instagram','Instagram'),('インスタ','Instagram'),('X(','X'),('Twitter','X'),('X（','X'),('Threads','Threads'),('Facebook','Facebook'),('LINE','LINE')]:
        if k in title: return v
    return ''
out_rows=[]
for r in rows:
    seg=r['seg']
    def g(label,pat):
        m=re.search(label+r'\s*¥\s*(-?[\d,]+)(?:\s*平均\s*¥\s*(-?[\d,]+))?(?:\s*最高\s*¥\s*(-?[\d,]+))?',seg); return m
    rv=g('売上/月',0); pf=g('利益/月',0)
    pv=re.search(r'PV/月\s*([\d,]+)(?:\s*平均\s*([\d,]+))?(?:\s*最高\s*([\d,]+))?',seg)
    fol=re.search(r'フォロワー数\s*（登録者数）\s*([\d,]+)',seg)
    d=dict(id=r['id'],url='https://rakkoma.com/project/detail/'+r['id'],listed=r['pub'],kind=KIND.get(r['icon'],r['icon']),
      title=r['title'],price_jpy=r['price'],
      rev_latest=num(rv.group(1)) if rv else None, rev_avg=num(rv.group(2)) if rv and rv.group(2) else None, rev_max=num(rv.group(3)) if rv and rv.group(3) else None,
      profit_latest=num(pf.group(1)) if pf else None, profit_avg=num(pf.group(2)) if pf and pf.group(2) else None, profit_max=num(pf.group(3)) if pf and pf.group(3) else None,
      pv_latest=num(pv.group(1)) if pv else None, pv_avg=num(pv.group(2)) if pv and pv.group(2) else None,
      followers=num(fol.group(1)) if fol else None, views_on_listing=r['views'],
      account_platform_by_title=plat(r['title']) if r['icon']=='user' else '',
      detail_fetched='no',type_label='',start_month='',category='',revenue_model='',status='',negotiation_requests='',workload_text='',price_over_profit_latest='',price_over_profit_avg='')
    p=f"{w}/det/{r['id']}.html"
    if os.path.exists(p):
        L=lines(p); d['detail_fetched']='yes'
        d['start_month']=after(L,'運営開始時期'); d['category']=after(L,'カテゴリ'); d['revenue_model']=after(L,'収益モデル'); d['status']=after(L,'現在の運営状況')
        i=L.index('案件一覧',L.index('案件一覧')+1) if L.count('案件一覧')>1 else 0
        d['type_label']=' '.join(L[i+1:i+4]) if i else ''
        # type label: lines after title up to 受付中
        if i:
            tl=[]
            for x in L[i+2:i+6]:
                if x in('受付中',): break
                tl.append(x)
            d['type_label']=''.join(tl)
        m=re.search(r'交渉申込 :\s*(\S+)',' '.join(L)); d['negotiation_requests']=m.group(1) if m else ''
        body=' '.join(L)
        wl=re.findall(r'[^。\n■・]{0,25}(?:週|月|日|毎日|1日)\s*(?:約|およそ)?\s*[0-9０-９〜~\.]+\s*(?:時間|分)[^。\n]{0,15}',body)
        d['workload_text']=' / '.join(dict.fromkeys(x.strip() for x in wl))[:200]
    for a,b,c in (('price_over_profit_latest','profit_latest',None),('price_over_profit_avg','profit_avg',None)):
        if d['price_jpy'] and d[b] and d[b]>0: d[a]=round(d['price_jpy']/d[b],1)
    out_rows.append(d)
cols=list(out_rows[0].keys())
with open(out,'w',newline='',encoding='utf-8') as f:
    wr=csv.DictWriter(f,fieldnames=cols); wr.writeheader(); wr.writerows(out_rows)
print(len(out_rows),sum(1 for d in out_rows if d['detail_fetched']=='yes'))
