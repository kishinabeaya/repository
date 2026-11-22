"""ラッコM&A 一覧ページ(HTML保存済み)から案件カードを抽出。使い方: python3 -I 05_rakkoma_parse_list.py <html_dir> <out_json>"""
import re,html,json,sys,glob
d,out=sys.argv[1],sys.argv[2]
def txt(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()
def yen(s):
    m=re.search(r'¥\s*([\d,]+)',s); return int(m.group(1).replace(',','')) if m else None
rows={}
for f in sorted(glob.glob(d+'/list_*.html')):
    t=open(f).read()
    for card in t.split('<li class="project_list')[1:]:
        m=re.search(r'/project/detail/(\d+)',card)
        if not m: continue
        pid=m.group(1)
        icon=re.search(r'project_list_icon fa-(\w[\w-]*)',card)
        name=re.search(r'<h3>(.*?)</h3>',card,re.S)
        pa=card.find('project_list_price_area')
        seg=txt(card[pa:pa+3500]) if pa>=0 else ''
        price=yen(seg)
        rev=re.search(r'売上/月\s*¥\s*(-?[\d,]+)',seg); prof=re.search(r'利益/月\s*¥\s*(-?[\d,]+)',seg)
        pub=re.search(r'<span>(\d{4}/\d\d/\d\d)</span>',card)
        views=re.search(r'fa-eye mr-1"></i>\s*<span>(\d+)',card)
        rows[pid]=dict(id=pid,icon=icon.group(1) if icon else '',title=txt(name.group(1)) if name else '',
          price=price,rev=int(rev.group(1).replace(',','')) if rev else None,
          profit=int(prof.group(1).replace(',','')) if prof else None,
          pub=pub.group(1) if pub else '',views=int(views.group(1)) if views else None,
          seg=seg[:400])
json.dump(list(rows.values()),open(out,'w'),ensure_ascii=False)
print(len(rows))
