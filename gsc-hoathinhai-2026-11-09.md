# Báo cáo Google Search Console — hoathinhai.com

- **Ngày đọc dữ liệu:** 09/11/2026
- **Cửa sổ hiệu suất:** 11/08/2026 – 07/11/2026, `search_type=web`
- **Property:** `sc-domain:hoathinhai.com` (siteOwner), kèm `sc-domain:hoathinhai.bond`
- **Tài khoản đọc:** `google_search_console_rector-abroad`

> **Mục đích tài liệu:** ghi lại *nguyên văn* dữ liệu đọc được từ tích hợp Google Search Console, kèm phần đối chiếu HTTP thật, để chuyển cho một AI agent khác xử lý tiếp. Mọi con số dưới đây là số API trả về, không phải số ước lượng.

---

## 0. Kênh truy cập và giới hạn của tích hợp

| Mục | Giá trị |
|---|---|
| Công cụ đã gọi | `GOOGLE_SEARCH_CONSOLE_LIST_SITES`, `_LIST_SITEMAPS`, `_SEARCH_ANALYTICS_QUERY`, `_INSPECT_URL` |
| Tài khoản đọc | `google_search_console_rector-abroad` (tài khoản thứ hai `google_search_console_istle-remass` có cùng property và cùng quyền) |
| Property | `sc-domain:hoathinhai.com` — `permissionLevel: siteOwner`; kèm `sc-domain:hoathinhai.bond` — `siteOwner` |
| Lưu ý về property | Tích hợp **chỉ có property dạng domain**; ảnh chụp của chủ web là property URL-prefix. Cùng một domain nên số liệu coverage tương đương. |
| Không có trong tích hợp | Tool đọc **báo cáo Coverage theo lý do** (Page indexing), Crawl stats, Core Web Vitals, và **danh sách URL mẫu của từng lý do**. Vì vậy bảng 8 lý do trong ảnh là nguồn duy nhất cho phần đó — API không trả lại được. |

---

## 1. LIST_SITES (nguyên văn)

```json
{"siteEntry":[
  {"permissionLevel":"siteOwner","siteUrl":"sc-domain:hoathinhai.com"},
  {"permissionLevel":"siteOwner","siteUrl":"sc-domain:hoathinhai.bond"}
]}
```

---

## 2. LIST_SITEMAPS (nguyên văn số liệu)

| Sitemap | Index? | submitted web | submitted image | indexed | errors | warnings | lastSubmitted | lastDownloaded |
|---|---|---|---|---|---|---|---|---|
| `/sitemap.xml` | true | 6384 | 5360 | 0 | 0 | 0 | 2026-11-01T16:56:42Z | 2026-11-07T13:46:28Z |
| `/sitemap-tong-hop.xml` | true | 4104 | 4104 | 0 | 0 | 0 | 2026-11-01T16:56:21Z | 2026-11-07T12:49:45Z |
| `/sitemap-ntt.xml` | false | 228 | 228 | 0 | 0 | 0 | 2026-11-01T11:52:35Z | 2026-11-09T03:52:18Z |
| `/sitemap-blv.xml` | false | 1008 | — | 0 | 0 | 0 | 2026-11-01T11:52:18Z | 2026-11-07T21:25:27Z |
| `/sitemap-phim.xml` | false | 5137 | 5137 | 0 | 0 | 0 | 2026-11-01T11:51:59Z | 2026-11-09T06:30:48Z |
| `/sitemap-trang.xml` | false | 16 | — | 0 | 0 | 0 | 2026-11-01T11:51:45Z | 2026-11-06T04:25:22Z |

**Hai điểm phải nhớ:**

- `indexed: "0"` ở **mọi** sitemap và `errors/warnings = 0` → trường này vô dụng, **đừng** dùng để kết luận.
- Cộng các sitemap con: **16 + 5137 + 1008 + 228 + 4104 = 10.493** — trùng khít tổng coverage trong ảnh (4,36 N + 6,13 N khoảng 10,49 N). Con số `submitted: 6384` của sitemap index là số không dùng được.
- Đếm trực tiếp bằng `curl`: trang 15 · phim 5137 · blv 1009 · tổng hợp **4799** (200 trang × 24) · ntt 228. Lệch 695 URL ở `tong-hop` so với GSC báo 4104.

---

## 3. INSPECT_URL — 4 URL, nguyên văn các trường

### 3.1. `/phim/chan-dien-thap-dung-si`

| Trường | Giá trị |
|---|---|
| verdict | NEUTRAL |
| coverageState | **Google không xác định được URL** |
| indexingState / pageFetch / robotsTxt | UNSPECIFIED / UNSPECIFIED / UNSPECIFIED |

### 3.2. `/phim-tong-hop/chan-dien-thap-dung-si`

| Trường | Giá trị |
|---|---|
| verdict | **PASS** |
| coverageState | **Đã được gửi và lập chỉ mục** |
| indexingState / pageFetch / robotsTxt | INDEXING_ALLOWED / SUCCESSFUL / ALLOWED |
| canonical | google = user = tự trỏ |
| lastCrawlTime | 2026-11-01T15:24:08Z (MOBILE) |
| sitemap / referringUrls | `["…/sitemap-tong-hop.xml"]` / `["…/sitemap-tong-hop.xml?page=11"]` |
| rich results | Đường dẫn + Video (PASS) |

### 3.3. `/ntt/ntt-series-pham-nhan-tu-tien-di-luc`

| Trường | Giá trị |
|---|---|
| verdict | NEUTRAL |
| coverageState | **Đã thu thập dữ liệu – hiện chưa được lập chỉ mục** |
| indexingState / pageFetch / robotsTxt | INDEXING_ALLOWED / SUCCESSFUL / ALLOWED |
| canonical | google = user = tự trỏ |
| lastCrawlTime | 2026-11-03T13:53:51Z (MOBILE) |
| sitemap | `["…/sitemap-ntt.xml", "…/sitemap.xml"]` — không có referringUrls |

### 3.4. `/phim/tro-tan-cuu-chau-ta-xuyen-khong-ve-co-dai-dung-kien-thuc-hien-dai-xoay-chuyen-2f5ixd`

| Trường | Giá trị |
|---|---|
| verdict | **PASS** |
| coverageState | **Đã được gửi và lập chỉ mục** |
| indexingState / pageFetch / robotsTxt | INDEXING_ALLOWED / SUCCESSFUL / ALLOWED |
| canonical | google = user = tự trỏ |
| lastCrawlTime | 2026-11-07T20:12:13Z (MOBILE) |
| referringUrls | `["/the-loai/va-mat", "/phim/mat-the-nam-khong-cung-thang-anh-ket-nghia-voi-4-thi-vuong-than-phan-noi-gian-giesfz", "/the-loai/hien-dai"]` |
| rich results | Đường dẫn + Video (PASS) |

**Chi tiết bổ sung:** referringUrls của URL 3.4 chứng minh trang `/phim/…` **có link nội bộ** (Google thấy link sau khi render JS), không phải mồ côi tuyệt đối.

---

## 4. SEARCH_ANALYTICS_QUERY — top 30 trang theo click

| # | Trang | Click | Impressions | CTR | Vị trí |
|---:|---|---:|---:|---:|---:|
| 1 | `/gioi-thieu` | 112 | 686 | 16,3% | 2,51 |
| 2 | `/` | 68 | 163 | 41,7% | 2,34 |
| 3 | `/blv/chu-tich-dem-nay-kho-thoat-the-presidents-fatal-attraction-2026` | 56 | 215 | 26,0% | 3,89 |
| 4 | `/phim/tro-tan-cuu-chau-ta-xuyen-khong-ve-co-dai-dung-kien-thuc-hien-dai-xoay-chuyen-2f5ixd` | 51 | 486 | 10,5% | 6,12 |
| 5 | `/blv/co-tich-ngan-sao-tale-of-thousand-stars` | 49 | 251 | 19,5% | 7,00 |
| 6 | `/blv/chiec-ca-vat-roi-ram-twisted-tie-2026` | 43 | 200 | 21,5% | 8,16 |
| 7 | `/blv/chuyen-tinh-o-poongduck-roommates-of` | 37 | 139 | 26,6% | 5,80 |
| 8 | `/blv/tinh-yeu-thuc-giac-noi-thao-nguyen` | 34 | 138 | 24,6% | 4,04 |
| 9 | `/blv/lan-nay-cau-chu-dong-hon-toi-di-you-should-be-the-one-to-come-kiss-me-2026` | 30 | 186 | 16,1% | 4,60 |
| 10 | `/blv/quy-tac-thuan-duong-tamed-2026` | 29 | **1.206** | **2,4%** | 6,66 |
| 11 | `/blv/dam-chim-trong-tinh-yeu-voi-ban-ty-phu-cua-cha-falling-for-my-dads-billionaire-friend-2026` | 28 | 87 | 32,2% | 5,52 |
| 12 | `/blv/serizawa-luc-ben-toi-la-lam-popular-serizawa-acts-weird-around-me-2026` | 23 | 599 | 3,8% | 8,26 |
| 13 | `/phim/sau-khi-xuyen-thanh-phao-hoi-ro-rang-la-phan-dien-sao-lai-cu-nang-nac-doi-om-w83ptt` | 23 | 142 | 16,2% | 5,99 |
| 14 | `/blv/nguyet-ha-van-tinh-love-beneath-the-moon-2026` | 22 | 42 | 52,4% | 3,40 |
| 15 | `/blv/am-thanh-cua-nhung-vien-duong-the-sound-of-sugar-cubes-2026` | 19 | 533 | 3,6% | 7,65 |
| 16 | `/blv/o-khoa-cuoi-cung-mang-ten-em-last-lock` | 19 | 97 | 19,6% | 4,69 |
| 17 | `/blv/san-sang-yeu-em-jun-and-jun-2023` | 19 | 71 | 26,8% | 5,61 |
| 18 | `/blv/hanh-trinh-thu-tieu-anh-mua-2-the-journey-to-killing-you-season-2-2026` | 16 | 281 | 5,7% | 11,11 |
| 19 | `/blv/nong-nan-gap-doi-tren-dau-luoi-my-boss-orders-me-hot-2026` | 16 | 29 | 55,2% | 3,93 |
| 20 | `/blv/phoi-sang-kep-2024` | 13 | 21 | 61,9% | 3,86 |
| 21 | `/blv/giam-cam-trong-ngot-ngao-dangerous-sweet-2026` | 10 | 70 | 14,3% | 5,46 |
| 22 | `/blv/nghien-nhung-cai-cham-cua-anh-addicted-to-his-touch-2026` | 10 | 16 | 62,5% | 1,94 |
| 23 | `/blv/trai-bao-toi-thue-hoa-ra-la-chu-cua` | 10 | 82 | 12,2% | 7,67 |
| 24 | `/blv/khe-uoc-tron-doi-long-term-contract-2026` | 9 | 24 | 37,5% | 3,13 |
| 25 | `/blv/mot-em-ha-one-summer-night-2016` | 9 | 44 | 20,5% | 6,18 |
| 26 | `/blv/sau-khi-doi-cho-hinh-nhu-cau-chang-phia-sau-thich-toi-thi-phai-after-moving-seats-the-boy-behind-me-has-a-crush-on-me-2026` | 9 | 35 | 25,7% | 5,09 |
| 27 | `/blv/nhip-tim-vuot-gioi-han-off-limits-2026` | 8 | 19 | 42,1% | 8,47 |
| 28 | `/blv/project-xy-show-truyen-hinh-2026` | 8 | 33 | 24,2% | 5,15 |
| 29 | `/phim-tong-hop/chan-dien-thap-dung-si` | 8 | 37 | 21,6% | 9,43 |
| 30 | `/blv/our-skyy-2-season-2-2023` | 7 | 33 | 21,2% | 7,00 |

> 25/30 trang dẫn đầu là `/blv/…`; chỉ **3 trang `/phim/…`** và **1 trang `/phim-tong-hop/…`** lọt top 30.

---

## 5. SEARCH_ANALYTICS_QUERY — top 20 truy vấn

| Truy vấn | Click | Impressions | Vị trí |
|---|---:|---:|---:|
| hoathinhai | 118 | 632 | 2,38 |
| tro tàn cửu châu mùa 36 | 31 | 212 | 5,75 |
| hoathinhai.com | 23 | 33 | 1,15 |
| cổ tích ngàn sao | 21 | 128 | 6,68 |
| hoathinhai com | 20 | 29 | 1,55 |
| the president's fatal attraction | 20 | 52 | 3,23 |
| tình yêu thức giấc nơi thảo nguyên | 13 | 63 | 3,14 |
| chuyện tình ở poongduck 304 bl vietsub | 12 | 27 | 3,93 |
| serizawa lúc bên tôi lạ lắm | 12 | 271 | 8,84 |
| chiếc cà vạt rối rắn | 11 | 44 | 8,91 |
| quy tắc thuần dưỡng | 11 | **642** | 6,38 |
| lần này cậu chủ động hôn tôi đi | 10 | 70 | 5,07 |
| nguyệt hạ vấn tình | 10 | 15 | 2,73 |
| chiec ca vat roi ram | 9 | 26 | 6,31 |
| chủ tịch đêm nay khó thoát | 9 | 41 | 4,54 |
| chiếc cà vạt rắc rối bl | 7 | 40 | 8,85 |
| our skyy 2 | 7 | 27 | 6,96 |
| đắm chìm trong tình yêu với bạn tỷ phú của cha | 7 | 21 | 5,29 |
| ổ khoá cuối cùng mang tên em | 7 | 48 | 4,27 |
| trai bao tôi thuê hóa ra là chú của người yêu cũ tập 1 | 6 | 25 | 6,92 |

---

## 6. Hai truy vấn lọc riêng

### 6.1. `/ntt/` (10 dòng)

| Trang | Click | Impressions | Vị trí |
|---|---:|---:|---:|
| `/ntt/ntt-series-he-thong-hoan-tra-van-lan` | 6 | 150 | 4,47 |
| `/ntt/ntt-series-thao-thi-t-chi-t` | 1 | 11 | 9,09 |
| `/ntt/ntt-series-he-thong-nang-cap-van-vat-mat-the` | 0 | 9 | 8,11 |
| `/ntt/ntt-series-than-cap-thang-cap-he-thong` | 0 | 3 | 6,33 |
| `/ntt/ntt-series-sat-thu-duong-dan-tai-di-the-gioi` | 0 | 2 | 7,00 |
| `/ntt/ntt-series-dich-chuyen-mat-the-tan-sang-co-he-thong-xuyen-hai-the-gioi` | 0 | 1 | 8,00 |
| `/ntt/ntt-series-he-thong-bat-ta-lam-dai-phan-dien` | 0 | 1 | 9,00 |
| `/ntt/ntt-series-nh-n-ho-n-tr-v-n-l-n-ta-l-m-b-tu-ch-n-gi-i` | 0 | 1 | 3,00 |
| `/ntt/ntt-series-sieu-cap-dien-trang-thong-tu-nong-phu-khuay-dao-tu-tien-gioi` | 0 | 1 | 3,00 |
| `/ntt/ntt-series-t-nh-d-y-m-t-n-i-t-ng-b-k-o-v-o-tr-ch-i-c-a-th-n-linh` | 0 | 1 | 11,00 |

Tổng 10 trang mẫu: **7 click / 180 impressions**. Một trang đã xác nhận “Đã thu thập dữ liệu – hiện chưa được lập chỉ mục”.

### 6.2. `?f=` (biến thể tham số vẫn được index, không nằm trong sitemap)

| URL | Click | Impressions | Vị trí |
|---|---:|---:|---:|
| `/phim-tong-hop/hakone-ekiden-cuoc-dua-tiep-suc-cua-chung-ta?f=kk` | 1 | 1 | 8,00 |
| `/phim-tong-hop/quai-dam-tran-tong-gia?f=kk` | 1 | 16 | 6,81 |
| `/phim-tong-hop/chuyen-tinh-hai-phi-tan?f=kk` | 0 | 1 | 10,00 |
| `/phim-tong-hop/nguoi-tao-mua?f=kk` | 0 | 1 | 11,00 |
| `/phim-tong-hop/tran-chien-xuyen-vu-tru-phan-3?f=kk` | 0 | 2 | 8,00 |
| `/phim-tong-hop/van-co-chi-ton-ly-van-tieu-truyen?f=nc` | 0 | 2 | 8,50 |

---

## 7. Đối chiếu HTTP thật (curl, không qua GSC)

| Kiểm | Kết quả |
|---|---|
| 20 URL rải đều `sitemap-phim` | **18 × 200, 2 × 301** |
| 2 URL 301 đó | `/phim/tieng-long-bi-ca-trieu-dinh-nghe-thay-he-thong-an-dua-boc-tran-hang-loat-bi-mat-gipkvw` → `/phim/full-mua-1-…-gipkvw`; `/phim/100-tuoi-nhap-ngu-…-2rkozi` → `/phim/100-tuoi-nhap-ngu-…-kunupx` (**đổi cả id**) |
| 10 URL rải đều 10 trang `sitemap-tong-hop` | 10 × 200, canonical **tự trỏ** |
| `/phim/chan-dien-thap-dung-si` | **404, 10/10 lần**, title “Không tìm thấy trang”, 5.427 byte, **không có** trong `sitemap-phim` |
| `/phim/tro-tan-…-2f5ixd` | Lần đo trước: **404** (5.427 B). Đo lại 10/10 lần: **200**, 11.722 B, title đúng, `robots: index, follow, max-image-preview:large…`, vẫn nằm trong sitemap |
| `/gioi-thieu` | Lần đo trước: **301**. Đo lại: **200**, 7.355 B, TTFB 0,09 s |
| Robots meta trang 404 | trang 404 trả title “Không tìm thấy trang” (noindex theo thiết kế) |

### 7.1. TTFB (3 lần đo)

| Đường dẫn | Lần 1 | Lần 2 | Lần 3 |
|---|---:|---:|---:|
| `/` | 0,112 s | 0,096 s | 0,086 s |
| `/phim/sau-khi-xuyen-thanh-phao-hoi…` | 0,238 s | 0,284 s | 0,239 s |
| `/blv/co-tich-ngan-sao…` | **0,990 s** | **0,680 s** | **0,582 s** |
| `/phim-tong-hop/chan-dien-thap-dung-si` | 0,351 s | 0,420 s | 0,290 s |
| `/ntt/ntt-series-he-thong-hoan-tra-van-lan` | 0,205 s | 0,185 s | 0,241 s |

### 7.2. Link nội bộ trong HTML thô (chưa chạy JS)

- Trang chủ: `href="/phim/…"` = **0**; tổng link nội bộ: the-loai 12, phim-tong-hop 1, boy-love 1.
- `/the-loai/va-mat`, `/the-loai/hien-dai`, `/the-loai/trong-sinh`: `href="/phim/…"` = **0** mỗi trang.
- Nhưng `referringUrls` của GSC lại chỉ đúng 2 trang `/the-loai/…` ở trên → link tồn tại **sau khi render JS**, Google vẫn thấy.

---

## 8. Những chỗ phải sửa lại so với kết luận sơ bộ

1. **“URL `/phim/chan-dien-thap-dung-si` Google chưa từng crawl” — SAI cách hiểu.** URL đó **404 thật** (10/10) và không có trong sitemap. `coverageState = "Google không xác định được URL"` ở đây là Google không có bản ghi vì URL không tồn tại, **không phải** bằng chứng “5.137 URL phim chưa được crawl”. Đừng dùng ca này làm dẫn chứng.
2. **“URL top 51 click nay 404” — không tái lập được.** Đo lại 10/10 lần đều 200, Google còn ghi crawl 07/11 và index PASS. Khả năng cao là **404 tạm thời** ở một thời điểm (edge trả trang lỗi 5.427 B thay vì trang thật). `/gioi-thieu` cũng đổi 301 → 200 giữa hai lần đo. Đây là **giả thuyết cần kiểm**, chưa phải kết luận: nếu edge thỉnh thoảng trả 404/301 khi gọi nguồn lỗi, nó giải thích được phần lớn 205 “Không tìm thấy (404)” + 1 “5xx” và cả các ca “Google không xác định được URL”.
3. **“Trang `/phim/…` mồ côi” — cần nói chính xác hơn.** HTML thô không có link, nhưng Google thấy link từ `/the-loai/…` sau render. Nên gọi là **“chỉ lộ đường sau khi render JS + sitemap”**, không phải mồ côi tuyệt đối.
4. **Không dùng `indexed` của sitemap API** (luôn 0) và **không dùng `submitted` của sitemap index** (6384, không khớp 10.493 của các sitemap con).

---

## 9. Tổng hợp số liệu để agent khác dùng ngay

- Coverage: **4,36 N đã index / 6,13 N chưa** (ảnh) — API không trả lại được.
- Lý do chưa index (ảnh, không lấy được qua API): **4.398** Đã phát hiện–chưa index · **976** Đã thu thập–chưa index · **205** 404 · **23** canonical thay thế · **18** noindex · **5** chuyển hướng · **5** trùng lặp · **1** lỗi 5xx.
- **10.493** = tổng URL 5 sitemap con, khớp đúng tổng coverage.
- **87%** nhóm chưa index là hai nhóm “Google biết nhưng chưa thấy đáng index”.
- Tỷ lệ URL 301 trong `sitemap-phim`: 2/20 mẫu khoảng **10%** (một ca đổi cả id chứ không chỉ slug).
- 4 trang có tham số `?f=` vẫn được index, không nằm trong sitemap.
- 100% mẫu 10 trang `/phim-tong-hop` có canonical tự trỏ; 0 mẫu noindex; 0 mẫu 404.

---

## 10. Việc nên làm tiếp (đề xuất cho agent nhận báo cáo)

1. Đo **tỷ lệ lỗi tạm thời** của edge: gọi lặp 100–200 lần trên 20 URL `/phim/`, đếm 200/404/301/5xx để xác nhận hay bác bỏ giả thuyết ở mục 8.2 (nghi phạm số một cho 205 404 + 1 5xx).
2. Lọc URL 301/404 khỏi `sitemap-phim` trước khi xuất.
3. Kiểm tra crawl: 5.137 URL phim gửi Google nhưng chỉ 3 trang phim lọt top 30 click — đo tỷ lệ index thật bằng cách inspect thêm mẫu (quota `INSPECT_URL` giới hạn, gọi nhiều sẽ 429).
4. Cân nhắc noindex/bỏ khỏi sitemap 228 trang `/ntt/…` (1 ca đã xác nhận “đã thu thập – chưa index”, tổng 7 click/90 ngày cho 10 trang mẫu).

---

**Chi phí và phạm vi:** chỉ gọi API đọc + `curl`; không dùng tài khoản kiểm thử, không tiêu thể lực/lượt; **không sửa tệp mã nào** nên không có typecheck/commit/deploy. Skill đã đọc theo mục 13 của `AGENTS.md`: `.agents/skills/systematic-debugging/SKILL.md` — áp dụng Phase 1 (gom bằng chứng từng tầng, không đoán nguyên nhân); chính vì vậy mới phát hiện 2 kết luận sơ bộ ở mục 8 là sai.

*Báo cáo tạo ngày 09/11/2026 từ dữ liệu Google Search Console (window 11/08–07/11/2026) và các phép đo HTTP trực tiếp trên https://hoathinhai.com. Số liệu coverage theo lý do lấy từ ảnh chụp của chủ web vì tích hợp không có endpoint tương ứng.*
