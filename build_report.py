from collections import Counter
import csv,datetime as dt,json,pathlib,re,zipfile
from urllib.parse import urlsplit
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment

ROOT=pathlib.Path('/workspace/gsc-export-2026-11-12')
inv=json.loads((ROOT/'inventory.json').read_text()); source=json.loads((ROOT/'source-data.json').read_text())
records=[]
for path in sorted(ROOT.glob('inspections-*.json')):
 data=json.loads(path.read_text()); records.extend(data if isinstance(data,list) else data.get('records',[]))
def inspection_time(r):
 try:return dt.datetime.fromisoformat(r.get('inspected_at_utc','').replace('Z','+00:00'))
 except Exception:return dt.datetime.min.replace(tzinfo=dt.timezone.utc)
byurl={}
for r in records:
 if r['url'] not in byurl or inspection_time(r)>=inspection_time(byurl[r['url']]):byurl[r['url']]=r
expected={'/tong-mon','/da-luu','/chinh-sach-quyen-rieng-tu','/dieu-khoan-su-dung','/Admin838282'}
def inspect_response(raw):
 if isinstance(raw,dict) and isinstance(raw.get('inspection_result'),dict): return raw['inspection_result']
 if isinstance(raw,dict) and isinstance(raw.get('structuredContent'),dict): return inspect_response(raw['structuredContent'])
 if isinstance(raw,dict) and isinstance(raw.get('content'),list):
  for c in raw['content']:
   if c.get('type')=='text':
    try:
     result=inspect_response(json.loads(c['text']))
     if result:return result
    except Exception: pass
 return {}
def normalize(item):
 r=byurl.get(item['url']); response=(r or {}).get('response',{})
 result=inspect_response(response); status=result.get('indexStatusResult',{})
 verdict=status.get('verdict',''); state='UNINSPECTED'
 if r:
  if not status: state='INSPECTION_ERROR'
  elif verdict=='PASS': state='INDEXED'
  elif verdict in ('FAIL','NEUTRAL'):state='NOT_INDEXED'
  else:state='UNKNOWN_VERDICT'
 canon=status.get('googleCanonical',''); mismatch=bool(canon and canon.rstrip('/')!=item['url'].rstrip('/'))
 coverage=status.get('coverageState',''); fetch=status.get('pageFetchState',''); indexing=status.get('indexingState','')
 intentional=urlsplit(item['url']).path.rstrip('/') in expected
 action=''; priority=''
 if state in ('UNINSPECTED','INSPECTION_ERROR','UNKNOWN_VERDICT'):
  action='Kiểm tra URL Inspection; chưa suy ra trạng thái chỉ mục'; priority='CHECK'
 elif state=='INDEXED':
  action='Giữ URL ổn định; kiểm truy vấn/hiển thị riêng nếu cần'; priority='MONITOR'
 else:
  priority='REVIEW'
  if intentional:
   action='Đối chiếu chính sách noindex có chủ đích; không tự gỡ noindex';priority='POLICY'
  elif mismatch:
   action='Kiểm URL đích/canonical/redirect, sitemap và link nội bộ; có thể là loại trừ hợp lệ'
  elif 'NOINDEX' in indexing.upper() or 'noindex' in coverage.lower():
   action='Kiểm meta/header noindex và lỗi nguồn tạm thời; xác minh ý định trước sửa'
  elif fetch in ('NOT_FOUND','SOFT_404','REDIRECT_ERROR'):
   action='Kiểm HTTP thật, dữ liệu phim, URL cũ/đã gỡ và chuyển hướng phù hợp'
  elif status.get('robotsTxtState')=='DISALLOWED':
   action='Kiểm robots.txt và ý định chặn crawl'
  else:action='Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt'
 return {'url':item['url'],'status':state,'verdict':verdict,'coverage':coverage,'inspection_time_utc':(r or {}).get('inspected_at_utc',''),'last_crawl_utc':status.get('lastCrawlTime',''),'page_fetch':fetch,'robots':status.get('robotsTxtState',''),'indexing_state':indexing,'google_canonical':canon,'user_canonical':status.get('userCanonical',''),'canonical_mismatch':mismatch,'inspection_link':result.get('inspectionResultLink',''),'policy_review':intentional,'action_priority':priority,'suggested_action':action,'clicks':item.get('clicks'),'impressions':item.get('impressions'),'ctr':item.get('ctr'),'position':item.get('position'),'sitemap_lastmod':item.get('lastmod',''),'sources':' | '.join(item['sources']),'inspection_priority':item.get('inspection_priority'),'raw_error':json.dumps(response,ensure_ascii=False)[:500] if r and not status else ''}
rows=[normalize(r) for r in inv['urls']]
counts=Counter(r['status'] for r in rows)
groups={'all_urls':rows,'indexed_confirmed':[r for r in rows if r['status']=='INDEXED'],'not_indexed_confirmed':[r for r in rows if r['status']=='NOT_INDEXED'],'uninspected':[r for r in rows if r['status']=='UNINSPECTED'],'inspection_errors':[r for r in rows if r['status'] in ('INSPECTION_ERROR','UNKNOWN_VERDICT')],'fix_review_queue':[r for r in rows if r['status']=='NOT_INDEXED' or r['canonical_mismatch']]}
headers=list(rows[0])
def literal(value):
 if isinstance(value,str):value=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',' ',value)
 if isinstance(value,str) and value.startswith(('=','+','-','@','\t','\r')):return "'"+value
 return value
def save_csv(name,headers,data):
 with (ROOT/(name+'.csv')).open('w',newline='',encoding='utf-8-sig') as f:
  writer=csv.DictWriter(f,fieldnames=headers,extrasaction='ignore');writer.writeheader();writer.writerows({k:literal(v) for k,v in row.items()} for row in data)
for name,data in groups.items():save_csv(name,headers,data)
daily=source.get('previous_report',{}).get('rows',[])
daily_rows=[{'date':r['keys'][0],**{k:r.get(k) for k in ('clicks','impressions','ctr','position')}} for r in daily]
save_csv('performance_daily',['date','clicks','impressions','ctr','position'],daily_rows)
for kind in ('pages','queries'):
 data=[{'page' if kind=='pages' else 'query':r['keys'][0],**{k:r.get(k) for k in ('clicks','impressions','ctr','position')}} for r in source[kind].get('rows',[])]
 save_csv('performance_'+kind,['page' if kind=='pages' else 'query','clicks','impressions','ctr','position'],data)
reason=Counter(r['coverage'] or '(không có coverage)' for r in groups['not_indexed_confirmed'])
quota=[json.loads(p.read_text()) for p in ROOT.glob('quota-stop-*.json')]
summary={'exported_at_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'property':source['property'],'total_inventory':len(rows),'status_counts':dict(counts),'raw_records':len(records),'unique_inspected_urls':len(byurl),'nonindexed_reasons':dict(reason),'sitemaps_fetched':len(inv['sitemap_fetches']),'sitemap_failures':inv['sitemap_failures'],'quota_stops':quota,'analytics_pages':source['pages'].get('row_count'),'analytics_pages_truncated':source['pages'].get('truncated'),'analytics_queries':source['queries'].get('row_count'),'analytics_queries_truncated':source['queries'].get('truncated'),'inspection_limit':inv['inspection_limit']}
(ROOT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
book=Workbook();book.remove(book.active)
about=[['Mục','Giải thích'],['Ngày','12/11/2026; xem timestamp UTC từng inspection'],['Property',source['property']],['URL inventory',len(rows)],['Đã index',counts['INDEXED']],['Chưa index được Google xác nhận',counts['NOT_INDEXED']],['Chưa inspection',counts['UNINSPECTED']],['Lỗi inspection/không rõ',counts['INSPECTION_ERROR']+counts['UNKNOWN_VERDICT']],['Phân biệt','UNINSPECTED không có nghĩa NOT_INDEXED; INDEXED không bảo đảm hiện cho mọi truy vấn'],['Nguồn inventory','Union sitemap hiện tại + URL hiệu suất Google trả + tuyến chính; không phải mọi URL có thể tồn tại'],['Lý do loại trừ','Redirect/canonical/noindex có chủ đích có thể hợp lệ, không tự coi mọi NOT_INDEXED là lỗi'],['Giới hạn Google','URL Inspection mặc định 2000/site/ngày; bảng không phải export toàn bộ Page Indexing report'],['Hiệu suất','16/10–12/11, Web, all; ngày12 chưa có hàng, ngày11 tạm thời; query hiếm có thể bị ẩn']]
sheet=book.create_sheet('READ_ME')
for row in about:sheet.append(row)
for name,data in groups.items():
 sheet=book.create_sheet(name[:31]);sheet.append(headers)
 for row in data:sheet.append([literal(row.get(k)) for k in headers])
for name in ('performance_daily','performance_pages','performance_queries'):
 sheet=book.create_sheet(name[:31])
 first='date' if name=='performance_daily' else 'page' if name=='performance_pages' else 'query'
 columns=[first,'clicks','impressions','ctr','position'];sheet.append(columns)
 if name=='performance_daily':data=daily_rows
 else:data=[{first:r['keys'][0],**{k:r.get(k) for k in columns[1:]}} for r in source['pages' if first=='page' else 'queries'].get('rows',[])]
 for row in data:sheet.append([literal(row.get(k)) for k in columns])
 for row in sheet.iter_rows(min_row=2):row[3].number_format='0.00%';row[4].number_format='0.00'
for sheet in book:
 sheet.freeze_panes='A2';sheet.auto_filter.ref=sheet.dimensions
 for cell in sheet[1]:cell.font=Font(bold=True,color='FFFFFF');cell.fill=PatternFill('solid',fgColor='17365D')
 sheet.column_dimensions['A'].width=75
 for column in range(2,min(sheet.max_column+1,25)):
  from openpyxl.utils import get_column_letter
  sheet.column_dimensions[get_column_letter(column)].width=24
 if sheet.title in groups:
  for row in sheet.iter_rows(min_row=2):
   row[headers.index('ctr')].number_format='0.00%';row[headers.index('position')].number_format='0.00'
book.save(ROOT/'GSC-URL-REPORT-2026-11-12.xlsx')
pending=sorted(groups['inspection_errors']+groups['uninspected'],key=lambda r:(0 if r['status']=='INSPECTION_ERROR' else 1,r.get('inspection_priority') or 999999,-(r.get('impressions') or 0),r['url']))
queue_dir=ROOT/'remaining-batches';queue_dir.mkdir(exist_ok=True)
for p in queue_dir.glob('*.csv'):p.unlink()
for i in range(0,len(pending),1000):save_path=queue_dir/('batch-'+str(i//1000+1).zfill(2)+'.csv');save_path.write_text('url\n'+'\n'.join('"'+r['url'].replace('"','""')+'"' for r in pending[i:i+1000])+'\n',encoding='utf-8-sig')
labels={'INDEXED':'Google xác nhận đã lập chỉ mục','NOT_INDEXED':'Google báo chưa lập chỉ mục/đang bị loại trừ','UNINSPECTED':'Chưa gọi URL Inspection','INSPECTION_ERROR':'Đã gọi nhưng API lỗi, chưa biết trạng thái','UNKNOWN_VERDICT':'Phản hồi chưa đủ để phân loại'}
status_table='\n'.join('| '+labels[k]+' | '+str(counts[k])+' |' for k in labels)
reason_table='\n'.join('| '+k.replace('|','/')+' | '+str(v)+' |' for k,v in reason.most_common()) or '| Chưa có | 0 |'
quota_note='Có marker dừng quota/giới hạn trong dữ liệu gốc; xem quota-stop-*.json để biết phản hồi thực tế.' if quota else 'Không có marker quota-stop ở thời điểm dựng báo cáo. Số inspection có giới hạn lấy mẫu/candidate và không đại diện toàn bộ inventory.'
daily_table='\n'.join('| '+r['date']+' | '+str(r['clicks'])+' | '+str(r['impressions'])+' | '+format(r['ctr']*100,'.2f')+'% | '+format(r['position'],'.2f')+' |' for r in daily_rows)
brand=source.get('brand_daily',{}).get('rows',[])
brand_table='\n'.join('| '+r['keys'][0]+' | '+str(r['clicks'])+' | '+str(r['impressions'])+' | '+format(r['position'],'.2f')+' |' for r in brand)
sample_bad=sorted(groups['not_indexed_confirmed'],key=lambda r:(-(r['clicks'] or 0),-(r['impressions'] or 0),r['url']))[:20]
bad_table='\n'.join('| `'+r['url']+'` | '+r['coverage'].replace('|','/')+' | '+r['suggested_action']+' |' for r in sample_bad)
report=f'''# Báo cáo Google Search Console và danh sách URL — 12/11/2026

Property: `{source['property']}`. Snapshot xuất: **{summary['exported_at_utc']}**. Timestamp inspection/crawl là UTC; ngày hiệu suất là nhãn ngày Search Console, không tự chuyển sang ngày VN.

## 1. Kết quả và mức độ đầy đủ

Đã lập inventory **{len(rows):,} URL** từ toàn bộ sitemap tải được, URL hiệu suất Google trả trong cửa sổ 16/10–12/11 và các tuyến chính. Đã đọc **{len(inv['sitemap_fetches'])} sitemap**, lỗi tải/parse **{len(inv['sitemap_failures'])}**. Một URL có thể nằm trong nhiều nguồn; đã gộp đúng chuỗi URL, không ép gộp query/path làm mất URL cần kiểm.

| Trạng thái | Số URL |
|---|---:|
{status_table}

Tổng URL có ít nhất một lần gọi inspection: **{len(byurl):,}**. Các số trên là số URL trong inventory có bằng chứng tương ứng, **không phải tổng số index toàn website** và không phải ước lượng tỷ lệ index toàn bộ site.

**Không gán UNINSPECTED thành NOT_INDEXED. Không dùng lịch sử click hoặc việc có trong sitemap làm bằng chứng đã index ở hiện tại.** INDEXED cũng không bảo đảm URL đang hiện cho mọi truy vấn hoặc ở một vị trí cụ thể.

URL Inspection của Google có hạn mức mặc định **2.000 lượt/site/ngày, 600/phút** ([nguồn Google](https://developers.google.com/webmaster-tools/limits)). Inventory lớn hơn hạn mức một ngày. Lượt xuất này chọn tối đa 2.000 URL ưu tiên: tuyến chính, các URL có hiệu suất, rồi lấy thêm từ các kho. Không suy rộng tỷ lệ của nhóm ưu tiên sang toàn bộ inventory. {quota_note}

Inventory là tập URL tìm được từ các nguồn đã nêu, **không phải toàn bộ URL Google biết**, mọi URL ngoài sitemap, hoặc mọi biến thể tham số có thể được website phục vụ. Công cụ hiện có không cung cấp export toàn bộ báo cáo Page Indexing của tài sản.

## 2. Các tệp cần gửi AI agent

| Tệp | Nội dung |
|---|---|
| `GSC-URL-REPORT-2026-11-12.xlsx` | Workbook có README, toàn bộ inventory, từng nhóm chỉ mục, hàng chờ và hiệu suất |
| `all_urls.csv` | Toàn bộ inventory, trạng thái, nguyên nhân, canonical, thời gian crawl/inspection, traffic và nguồn URL |
| `indexed_confirmed.csv` | Những URL được URL Inspection trả verdict PASS |
| `not_indexed_confirmed.csv` | Những URL có verdict FAIL/NEUTRAL và có indexStatusResult; gồm cả loại trừ hợp lệ |
| `inspection_errors.csv` | API lỗi hoặc verdict chưa hiểu; chưa được coi là biết trạng thái index |
| `uninspected.csv` | URL chưa inspection trong lượt xuất này |
| `fix_review_queue.csv` | URL chưa index hoặc canonical khác URL kiểm; cần review trước khi sửa, không phải danh sách tất cả đều lỗi |
| `remaining-batches/` | Hàng chờ inspection tiếp theo, tối đa 1.000 URL mỗi tệp; ưu tiên lỗi gọi và URL còn thiếu trong nhóm ưu tiên |
| `performance_pages.csv` | {source['pages'].get('row_count')} hàng URL có số liệu Web được API trả |
| `performance_queries.csv` | {source['queries'].get('row_count')} hàng truy vấn công khai được API trả |
| `performance_daily.csv` | Click/impressions/CTR/vị trí theo ngày |
| `source-data.json`, `inventory.json` | Dữ liệu nguồn, ngữ cảnh truy vấn, trạng thái tải sitemap, nguồn từng URL |
| `inspections-*.json` | Phản hồi URL Inspection gốc theo URL, có thời điểm gọi |
| `summary.json` | Số đếm và nguyên nhân, có thể kiểm lại bằng máy |
| `AI-AGENT-HANDOFF.md` | Hướng dẫn agent kiểm chứng, phân loại và sửa theo bằng chứng |

CSV dùng UTF-8 BOM để mở bằng Excel; CTR trong CSV/JSON là tỷ lệ 0–1, workbook hiển thị dạng phần trăm. Chuỗi có thể bị Excel hiểu thành công thức được thêm dấu nháy đơn để giữ dạng văn bản; giá trị gốc giữ trong JSON. Workbook có filter/freeze header. Dữ liệu là của website này; không có password/token trong gói xuất.

## 3. Cách đọc trạng thái URL

- **INDEXED:** Google trả verdict PASS ở dữ liệu chỉ mục của URL. Đọc kèm lastCrawlTime; đây không phải phép test live của HTTP/HTML ngày hôm nay.
- **NOT_INDEXED:** Google báo URL chưa index hoặc đang bị loại trừ. Giữ nguyên coverageState, indexingState, pageFetchState và Google canonical để phân biệt nguyên nhân.
- **UNINSPECTED:** chưa gọi. Không có kết luận index.
- **INSPECTION_ERROR/UNKNOWN_VERDICT:** thiếu kết quả dùng được (kể cả VERDICT_UNSPECIFIED); đưa lại vào hàng chờ. Không sửa code dựa trên lỗi gọi API.

Loại trừ có thể là **đúng thiết kế**: URL redirect cũ, bản thay thế canonical đúng, trang cá nhân/noindex có chủ đích. Không tự gỡ noindex hoặc ép index mọi URL. Những route được đánh dấu policy_review là gợi ý đối chiếu chính sách hiện hành, không phải bằng chứng lỗi.

## 4. Nguyên nhân Google báo ở nhóm chưa index

| Nguyên nhân nguyên văn | Số URL đã kiểm |
|---|---:|
{reason_table}

Các ví dụ ưu tiên theo traffic lịch sử, tối đa 20 URL; danh sách đầy đủ trong CSV/Excel:

| URL | Coverage Google báo | Hướng kiểm tiếp |
|---|---|---|
{bad_table}

Hướng kiểm là triage, không phải nguyên nhân gốc đã được chứng minh. Phải kiểm HTTP/HTML/render/canonical trên main và production mới nhất trước khi sửa.

## 5. Hiệu suất mới nhất và thương hiệu

Đã yêu cầu đến 12/11; snapshot chưa có hàng ngày12. Ngày11 còn tạm thời. Số liệu ngày gần nhất có thể tiếp tục cập nhật; query hiếm được Google ẩn. Phản hồi pages/queries có truncated={source['pages'].get('truncated')}/{source['queries'].get('truncated')}; điều đó không bảo đảm API công khai mọi hàng.

| Ngày | Click | Hiển thị | CTR | Vị trí TB |
|---|---:|---:|---:|---:|
{daily_table}

Từ khoá exact `hoathinhai`:

| Ngày | Click | Hiển thị | Vị trí TB |
|---|---:|---:|---:|
{brand_table}

Kết quả indexed và vị trí TB của những lần được hiển thị không giải thích toàn bộ việc người dùng tìm không thấy kết quả “Giới thiệu”. Không dùng bảng này để phủ nhận trải nghiệm đó hoặc kết luận Google phạt. Bộ từ khoá mục tiêu còn lại chưa có đủ hàng exact công khai; không được bịa số lượng tìm kiếm/thứ hạng.

## 6. Quy trình dành cho agent sửa

1. Đọc `AI-AGENT-HANDOFF.md`, kiểm timestamp và chỉ lấy trạng thái từ indexStatusResult.
2. Fetch main mới nhất, đọc AGENTS.md và skill seo-audit; không coi audit ngày11/11 là mã hiện hành chưa sửa.
3. Ưu tiên URL có traffic lịch sử nhưng hiện bị loại, URL chính và những mẫu lỗi lặp theo template.
4. Phân biệt canonical/redirect hợp lệ với lỗi; nội dung chủ động gỡ không tự khôi phục chỉ để có index.
5. Với crawled/discovered-not-indexed: kiểm nội dung thật sau render, liên kết nội bộ, tính riêng biệt, HTTP/canonical và độ ổn định nguồn. Không chỉ bấm yêu cầu index hàng loạt.
6. Với noindex: xác minh chính sách và nhánh lỗi tạm thời trước khi thay. Với lỗi HTTP: xác minh URL đã mất hay chỉ API/source chậm.
7. Ghi tiêu chí nghiệm thu và bằng chứng trước/sau. Index có độ trễ; deploy thành công không đồng nghĩa Google lập chỉ mục ngay.

## 7. Phần chưa có bằng chứng

Chưa có inspection của những URL trong `uninspected.csv`. Chưa có export đầy đủ các báo cáo Xóa tạm thời, Thao tác thủ công, Vấn đề bảo mật hoặc Page Indexing theo toàn tài sản qua plugin. Không kết luận các mục đó sạch.

Không tăng polling, không thay cấu hình, không sửa mã hay dữ liệu production trong lượt xuất. URL Inspection đọc dữ liệu chỉ mục được Google lưu; không phải tự động submit index hoặc phát sinh chiến đấu/thể lực trong game.
'''
(ROOT/'REPORT.md').write_text(report,encoding='utf-8')
handoff='''# Câu lệnh giao AI agent kiểm tra và sửa SEO

Repository: https://github.com/Winnyzzzz/phimtonghop-copy
Website: https://hoathinhai.com/
Property đã đọc: sc-domain:hoathinhai.com

Hãy dùng gói dữ liệu này để review và đề xuất/sửa các vấn đề SEO có bằng chứng. Fetch main mới nhất, đọc AGENTS.md, .agents/skills/seo-audit/SKILL.md và phần tham chiếu khớp công việc. Không làm lại báo cáo bằng suy đoán.

Đọc REPORT.md, summary.json, READ_ME trong workbook, rồi indexed_confirmed.csv, not_indexed_confirmed.csv, fix_review_queue.csv. Dùng inspections-*.json khi cần kiểm nguyên văn Google. Mỗi trạng thái gắn với inspection_time_utc và last_crawl_utc; không coi là HTTP live hiện tại.

QUY TẮC BẮT BUỘC
- INDEXED có bằng chứng verdict PASS. NOT_INDEXED có indexStatusResult với verdict FAIL hoặc NEUTRAL và coverageState. UNINSPECTED/INSPECTION_ERROR/UNKNOWN_VERDICT (kể cả VERDICT_UNSPECIFIED) chưa phải kết luận chưa index.
- URL có traffic quá khứ hoặc có trong sitemap không chứng minh đang index. Indexed không bảo đảm hiện cho mọi truy vấn.
- Không ép index URL redirect cũ, canonical thay thế hợp lệ, trang cá nhân/noindex cố ý, hoặc URL đã chủ động gỡ. Trước khi đổi chính sách, xác minh chủ đích và yêu cầu của chủ web.
- Với URL chưa index, kiểm rawHTML lẫn DOM sau JavaScript, HTTP, canonical, robots, sitemap và liên kết nội bộ. Phân biệt lỗi nguồn tạm thời và nội dung không tồn tại.
- Không tạo schema/ngày upload/rating giả, không nhồi từ khoá, không tạo hàng loạt trang giống nhau chỉ đổi tên.
- Lịch sử audit 11/11 chỉ là giả thuyết cũ cần tái hiện trên main mới; không sửa lại lỗi đã được giải quyết.
- Đề xuất sửa theo mẫu lỗi/template trước, không thay hàng nghìn URL/301 chỉ để đổi tên. Giữ URL và link cũ có giá trị.
- Tôn trọng quy trình test/deploy trong AGENTS khi được giao sửa. Không tự chạy toàn bộ test nếu repo cấm. Báo rõ việc đã đo/chưa đo; không gọi index phục hồi chỉ vì deploy xong.

KIỂM NỐT DANH SÁCH CHƯA BIẾT
- remaining-batches/ chứa URL chưa có kết quả dùng được. Dùng URL Inspection theo hạn mức còn lại, không chạy lại toàn bộ URL đã được kiểm cùng ngày.
- Google mặc định giới hạn 2000 inspection/site/ngày,600/phút. Không tự suy giờ reset theo giờ VN. Khi quota hoặc tín dụng plugin hết, dừng, lưu checkpoint và giữ các URL còn lại là chưa biết.
- Tìm property bằng công cụ listsites trước; giữ đúng site_url công cụ trả. Không tự đoán property.
- Nếu có export Page Indexing bổ sung của chủ web, hợp nhất theo URL và timestamp; lưu ý export danh sách ví dụ của Google cũng có thể không đầy đủ.

ĐẦU RA
1. Danh sách đã xác nhận đúng/loại trừ hợp lệ/lỗi cần sửa/chưa đủ dữ kiện.
2. Mỗi lỗi: URL cụ thể, coverage gốc, codefile:line, cách tái hiện, nguyên nhân có bằng chứng, sửa tối thiểu và tiêu chí nghiệm thu.
3. Những thay đổi có thể ảnh hưởng traffic và cách giữ đường dẫn hiện hữu.
4. Bằng chứng kiểm sau sửa; phần còn chờ Google crawl và phần chưa kiểm vì quota.

Ưu tiên truy vấn thương hiệu hoathinhai/hhai/hoạt hình ai và các landing page đúng nội dung: phim ai/xem phim ai, boylove/đam mỹ/phim gay/phim gay Thái Lan. Với hhpanda, xác minh ý định và quan hệ thương hiệu; không nhận thương hiệu bên khác là của website này. Không cam kết vị trí Google.
'''
(ROOT/'AI-AGENT-HANDOFF.md').write_text(handoff,encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
