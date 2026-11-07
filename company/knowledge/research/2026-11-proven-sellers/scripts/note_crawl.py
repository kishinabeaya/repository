"""note.com hashtag API (public GET, no login). Collect notes with price>0 (paid) and like_count.
Purchase counts are NOT exposed by this API. Follower count via /api/v2/creators/<urlname>.
usage: python3 note_crawl.py <raw_dir> <out_csv>
"""
import sys,json,time,subprocess,csv,urllib.parse,os
raw,outcsv=sys.argv[1],sys.argv[2]; os.makedirs(raw,exist_ok=True)
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
def get(url):
    time.sleep(2)
    r=subprocess.run(["curl","-sS","--compressed","-m","30","-A",UA,"-w","\n%{http_code}",url],capture_output=True,text=True)
    b,_,c=r.stdout.rpartition("\n"); return c,b
TAGS=["有料note","有料記事","占い","副業","転職","恋愛","自己分析","AI活用","電子書籍","テンプレート"]
paid={}; nreq=0; total=0; fails=[]
for t in TAGS:
    for order in ["hot"]:
        for pg in (1,2):
            u=f"https://note.com/api/v3/hashtags/{urllib.parse.quote(t)}/notes?order={order}&page={pg}"
            c,b=get(u); nreq+=1
            if c!="200": fails.append((t,pg,c)); break
            d=json.loads(b)['data']; open(f"{raw}/{t}-{pg}.json","w").write(b)
            for n in d['notes']:
                total+=1
                if (n.get('price') or 0)>0 and n['key'] not in paid:
                    paid[n['key']]=dict(hashtag=t,key=n['key'],title=n['name'],price_jpy=n['price'],like_count=n['like_count'],publish_at=n['publish_at'][:10],type=n['type'],
                        urlname=n['user']['urlname'],url=f"https://note.com/{n['user']['urlname']}/n/{n['key']}",follower_count='')
            if d.get('is_last_page'): break
print("scanned",total,"paid",len(paid),"fails",fails,flush=True)
# followers for top 20 paid by likes
top=sorted(paid.values(),key=lambda x:-x['like_count'])[:20]
for p in top:
    c,b=get(f"https://note.com/api/v2/creators/{p['urlname']}"); nreq+=1
    if c=="200":
        try: p['follower_count']=json.loads(b)['data']['followerCount']
        except Exception: pass
rows=list(paid.values())
if rows:
    with open(outcsv,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("requests",nreq,"rows",len(rows))
