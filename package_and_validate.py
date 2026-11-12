from pathlib import Path
from collections import Counter
import csv,hashlib,json,zipfile
from openpyxl import load_workbook

ROOT=Path('/workspace/gsc-export-2026-11-12')
summary=json.loads((ROOT/'summary.json').read_text())
def read(name):
 with (ROOT/(name+'.csv')).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
allrows=read('all_urls'); actual=Counter(r['status'] for r in allrows)
assert len(allrows)==summary['total_inventory']
assert len({r['url'] for r in allrows})==len(allrows)
assert dict(actual)==summary['status_counts']
groups={name:read(name) for name in ('indexed_confirmed','not_indexed_confirmed','uninspected','inspection_errors')}
assert sum(map(len,groups.values()))==len(allrows)
assert all(r['verdict']=='PASS' for r in groups['indexed_confirmed'])
assert all(r['verdict'] in ('NEUTRAL','FAIL') for r in groups['not_indexed_confirmed'])
assert all(r['inspection_time_utc'] for r in groups['indexed_confirmed']+groups['not_indexed_confirmed'])
ids=[r['url'] for g in groups.values() for r in g]
assert len(ids)==len(set(ids))
pending={r['url'] for r in groups['uninspected']+groups['inspection_errors']}
batch_urls=[]
for path in sorted((ROOT/'remaining-batches').glob('*.csv')):
 with path.open(encoding='utf-8-sig',newline='') as f:batch_urls.extend(r['url'] for r in csv.DictReader(f))
assert set(batch_urls)==pending and len(batch_urls)==len(pending)
raw=[]
for path in ROOT.glob('inspections-*.json'):
 data=json.loads(path.read_text());raw.extend(data if isinstance(data,list) else data.get('records',[]))
rawurls={r['url'] for r in raw}
assert len(rawurls)==summary['unique_inspected_urls']
assert rawurls.issubset({r['url'] for r in allrows})
assert all(r['url'] in rawurls for r in groups['indexed_confirmed']+groups['not_indexed_confirmed'])
book=load_workbook(ROOT/'GSC-URL-REPORT-2026-11-12.xlsx',read_only=True,data_only=False)
assert book['all_urls'].max_row==len(allrows)+1
for name,data in groups.items():assert book[name].max_row==len(data)+1
for sheet_name in ('performance_pages','performance_queries','performance_daily'):
 sheet=book[sheet_name]
 if sheet.max_row>1:
  row=next(sheet.iter_rows(min_row=2,max_row=2))
  assert all(c.data_type=='n' for c in row[1:5]),sheet_name
book.close()
include=[p for p in ROOT.iterdir() if p.is_file() and (p.suffix in ('.csv','.xlsx','.md','.json','.py')) and not p.name.startswith(('shard-','progress-')) and p.name!='MANIFEST.json']+list((ROOT/'remaining-batches').glob('*.csv'))
manifest={'files':[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(include)]}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
include.append(ROOT/'MANIFEST.json')
archive=ROOT/'GSC-EXPORT-2026-11-12.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in include:z.write(p,arcname=str(p.relative_to(ROOT)))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(include)
print(json.dumps({'validation':'PASS','inventory':len(allrows),'status_counts':dict(actual),'inspection_records':len(raw),'pending':len(pending),'archive_files':len(include),'archive_bytes':archive.stat().st_size},ensure_ascii=False))
