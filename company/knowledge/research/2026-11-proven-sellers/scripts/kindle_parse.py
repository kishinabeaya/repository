"""Parse saved Amazon.co.jp bestseller list pages into CSV.
usage: python3 kindle_parse.py <html_dir> <out_csv> <node:name> ...   (file = <html_dir>/<node>.html; blocked pages skipped)
"""
import sys,re,html,csv,os,urllib.parse
d,out=sys.argv[1],sys.argv[2]
rows=[];skipped=[]
for a in sys.argv[3:]:
    node,name=a.split(':',1)
    p=f"{d}/{node}.html"
    if not os.path.exists(p): skipped.append(name); continue
    h=open(p,encoding='utf-8',errors='replace').read()
    if 'p13n-sc-uncoverable-faceout' not in h: skipped.append(name); continue
    parts=h.split('<span class="zg-bdg-text">#')[1:]
    for part in parts:
        rank=int(re.match(r'(\d+)',part).group(1))
        asin=re.search(r'id="([A-Z0-9]{10})" class="p13n-sc-uncoverable-faceout"',part)
        if not asin: continue
        title=re.search(r'line-clamp-\d_\w+">([^<]+)</div></span>',part)
        author=re.search(r'class="a-size-small a-link-child"[^>]*><div[^>]*>([^<]+)<',part)
        rate=re.search(r'aria-label="5つ星のうち([\d.]+)、([\d,]+)件のレーティング"',part)
        price=re.search(r'p13n-sc-price_\w+">([^<]+)<',part)
        fmt=re.search(r'a-color-secondary a-text-normal">([^<]+)<',part)
        rows.append(dict(category=name,node=node,rank=rank,asin=asin.group(1),title=html.unescape(title.group(1)) if title else '',
            author=html.unescape(author.group(1)) if author else '',price_jpy=re.sub(r'[^\d]','',price.group(1)) if price else '',
            rating=rate.group(1) if rate else '',rating_count=rate.group(2).replace(',','') if rate else '',
            format=html.unescape(fmt.group(1)) if fmt else '',publisher='',release_date='',publishing_type='未確認',url=f"https://www.amazon.co.jp/dp/{asin.group(1)}"))
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows),'rows; skipped (blocked/not fetched):',skipped)
