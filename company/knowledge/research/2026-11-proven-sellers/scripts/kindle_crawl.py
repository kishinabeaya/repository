"""Amazon.co.jp Kindle bestseller list crawler (GET only, no login, no evasion).
Amazon returns a 'click to continue' interstitial when requests are rapid; we do NOT click through.
We only slow down (25s pacing); after a block we wait 60s and retry once; 3 consecutive failures abort.
usage: python3 kindle_crawl.py <outdir> <node:name> ...
"""
import sys,time,subprocess,os
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
def get(url,path):
    r=subprocess.run(["curl","-sS","--compressed","-m","30","-A",UA,"-o",path,"-w","%{http_code}",url],capture_output=True,text=True)
    h=open(path,encoding='utf-8',errors='replace').read() if os.path.exists(path) else ''
    return r.stdout, ('p13n-sc-uncoverable-faceout' in h)
fails=0
for a in sys.argv[2:]:
    node,name=a.split(':',1)
    path=f"{out}/{node}.html"
    url=f"https://www.amazon.co.jp/gp/bestsellers/digital-text/{node}"
    time.sleep(int(os.environ.get("PACE","25")))
    code,ok=get(url,path)
    if not ok and os.environ.get("RETRY","1")=="1":
        time.sleep(60); code,ok=get(url,path)
    print(node,name,code,'OK' if ok else 'BLOCKED',flush=True)
    fails=0 if ok else fails+1
    if fails>=3: print('ABORT: 3 consecutive blocks'); break
