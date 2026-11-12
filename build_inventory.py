import concurrent.futures as cf
import datetime as dt,json,pathlib,urllib.request,urllib.error,urllib.parse,xml.etree.ElementTree as ET
ROOT=pathlib.Path('/workspace/gsc-export-2026-11-12'); BASE='https://hoathinhai.com'
source=json.loads((ROOT/'source-data.json').read_text())
rows={}; maps=[]; visited=set()
def add(url,origin,lastmod=''):
 if not url or urllib.parse.urlparse(url).hostname not in ('hoathinhai.com','www.hoathinhai.com'): return
 item=rows.setdefault(url,{'url':url,'sources':[],'lastmod':'','clicks':None,'impressions':None,'ctr':None,'position':None})
 if origin not in item['sources']: item['sources'].append(origin)
 if lastmod>item['lastmod']: item['lastmod']=lastmod
def get(url):
 result={'url':url,'fetched_at_utc':dt.datetime.now(dt.timezone.utc).isoformat()}
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (SEO inventory export)','Accept':'application/xml,text/xml,*/*'})
  with urllib.request.urlopen(req,timeout=25) as response: raw=response.read();result['status']=response.status
  tree=ET.fromstring(raw); kind=tree.tag.split('}')[-1];result['kind']=kind
  if kind=='sitemapindex': result['children']=[n.text.strip() for n in tree.findall('{*}sitemap/{*}loc') if n.text]
  elif kind=='urlset':
   result['entries']=[{'url':n.findtext('{*}loc','').strip(),'lastmod':n.findtext('{*}lastmod','').strip()} for n in tree.findall('{*}url')]
  else: result['error']='Unexpected XML root: '+kind
 except Exception as e: result['error']=str(e)
 return result
queue=list(dict.fromkeys([BASE+'/sitemap.xml']+[s['path'] for s in source['sitemaps'].get('sitemaps',[])]))
while queue:
 batch=[u for u in queue if u not in visited and urllib.parse.urlparse(u).hostname=='hoathinhai.com']; queue=[]
 if not batch: break
 visited.update(batch)
 with cf.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(get,batch))
 for r in results:
  maps.append(r)
  for u in r.get('children',[]):
   if u not in visited: queue.append(u)
  for e in r.get('entries',[]): add(e['url'],'sitemap:'+r['url'],e['lastmod'])
for item in source['pages'].get('rows',[]):
 url=item['keys'][0];add(url,'search_analytics:2026-10-16/2026-11-12:all')
 if url in rows: rows[url].update({k:item.get(k) for k in ('clicks','impressions','ctr','position')})
for path in ('/','/gioi-thieu','/boy-love','/phim-tong-hop','/tong-mon','/da-luu','/chinh-sach-quyen-rieng-tu','/dieu-khoan-su-dung'):
 add(BASE+path,'core_route')
def family(url):
 p=urllib.parse.urlparse(url).path
 return next((f for f in ('phim','blv','ntt','phim-tong-hop','boy-love','the-loai') if p.startswith('/'+f+'/')),'core')
ordered=[]; seen=set()
def choose(item):
 if item['url'] not in seen: ordered.append(item);seen.add(item['url'])
for item in rows.values():
 if family(item['url'])=='core' or any(x.startswith('sitemap:') and 'sitemap-trang' in x for x in item['sources']): choose(item)
for item in sorted(rows.values(),key=lambda r:(-(r['clicks'] or 0),-(r['impressions'] or 0),r['url'])):
 if item['impressions'] is not None: choose(item)
remaining={}
for item in rows.values():
 if item['url'] not in seen: remaining.setdefault(family(item['url']),[]).append(item)
for key in remaining: remaining[key].sort(key=lambda r:(r['lastmod'],r['url']),reverse=True)
while any(remaining.values()):
 for key in ('ntt','blv','phim','phim-tong-hop','boy-love','the-loai','core'):
  if remaining.get(key): choose(remaining[key].pop(0))
  if len(ordered)>=2000: break
 if len(ordered)>=2000: break
for i,item in enumerate(ordered): item['inspection_priority']=i+1
inventory={'built_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'property':source['property'],'sitemap_fetches':[{k:v for k,v in m.items() if k!='entries'} for m in maps],'sitemap_failures':[m for m in maps if m.get('error')],'url_count':len(rows),'urls':sorted(rows.values(),key=lambda x:x['url']),'inspection_candidates':len(ordered),'inspection_limit':2000}
(ROOT/'inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
for shard in range(4):
 items=ordered[shard::4]
 (ROOT/('shard-'+str(shard)+'.json')).write_text(json.dumps({'property':source['property'],'shard':shard,'urls':[x['url'] for x in items]},ensure_ascii=False,indent=2))
print(json.dumps({'url_count':len(rows),'sitemaps_fetched':len(maps),'sitemap_errors':[{k:v for k,v in m.items() if k!='entries'} for m in maps if m.get('error')],'inspection_candidates':len(ordered),'shards':4,'shard_sizes':[len(ordered[i::4]) for i in range(4)]},ensure_ascii=False))
