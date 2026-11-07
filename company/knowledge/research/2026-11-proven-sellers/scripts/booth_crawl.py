"""BOOTH wish-list-sorted top items per category/keyword (GET only, no login). 1.5s pacing.
usage: python3 booth_crawl.py <raw_dir> <out_csv> <topN>
"""
import sys,re,time,json,subprocess,csv,html,urllib.parse,os
raw,outcsv,topn=sys.argv[1],sys.argv[2],int(sys.argv[3]); os.makedirs(raw,exist_ok=True)
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
def get(url):
    time.sleep(1.5)
    r=subprocess.run(["curl","-sS","--compressed","-m","30","-A",UA,"-w","\n%{http_code}",url],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n"); return code,body
Q=[("cat","技術書"),("cat","その他書籍"),("cat","エッセイ"),("cat","評論"),("cat","素材（その他）"),("cat","フォント・書体"),("cat","ステーショナリー"),("cat","カレンダー"),
   ("q","占い"),("q","タロット"),("q","Notion"),("q","Excel"),("q","家計簿"),("q","ワークシート")]
seen=set(); rows=[]; nreq=0
for kind,name in Q:
    e=urllib.parse.quote(name)
    url=f"https://booth.pm/ja/browse/{e}?sort=wish_lists" if kind=="cat" else f"https://booth.pm/ja/search/{e}?sort=wish_lists"
    code,body=get(url); nreq+=1
    if code!="200": print("FAIL",kind,name,code,flush=True); continue
    ids=[]
    for m in re.finditer(r'data-product-id="(\d+)"[^>]*?data-product-name="([^"]*)"',body):
        if m.group(1) not in ids: ids.append(m.group(1))
    got=0
    for i in ids:
        if got>=topn: break
        if i in seen: continue
        seen.add(i)
        code,j=get(f"https://booth.pm/ja/items/{i}.json"); nreq+=1
        if code!="200": print("FAIL json",i,code,flush=True); continue
        open(f"{raw}/{i}.json","w").write(j)
        d=json.loads(j); c=d.get('category') or {}
        pr=re.sub(r'[^\d]','',d.get('price') or '') 
        v=d.get('variations') or []
        rows.append(dict(query_type=kind,query=name,rank_in_search=ids.index(i)+1,item_id=i,name=d['name'],price_jpy=pr,
            wish_lists_count=d.get('wish_lists_count'),category=c.get('name'),parent_category=(c.get('parent') or {}).get('name'),
            tags="|".join(t['name'] for t in d.get('tags',[])),published_at=d.get('published_at'),
            variation_types="|".join(sorted({str(x.get('type') or '') for x in v})) ,
            n_variations=len(v),shop=(d.get('shop') or {}).get('name'),url=f"https://booth.pm/ja/items/{i}"))
        got+=1
    print(kind,name,len(ids),got,flush=True)
with open(outcsv,"w",newline="",encoding="utf-8") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("requests",nreq,"rows",len(rows))
