# Báo cáo Google Search Console và danh sách URL — 12/11/2026

Property: `sc-domain:hoathinhai.com`. Snapshot xuất: **2026-11-12T07:27:21.020702+00:00**. Timestamp inspection/crawl là UTC; ngày hiệu suất là nhãn ngày Search Console, không tự chuyển sang ngày VN.

## 1. Kết quả và mức độ đầy đủ

Đã lập inventory **8,772 URL** từ toàn bộ sitemap tải được, URL hiệu suất Google trả trong cửa sổ 16/10–12/11 và các tuyến chính. Đã đọc **126 sitemap**, lỗi tải/parse **0**. Một URL có thể nằm trong nhiều nguồn; đã gộp đúng chuỗi URL, không ép gộp query/path làm mất URL cần kiểm.

| Trạng thái | Số URL |
|---|---:|
| Google xác nhận đã lập chỉ mục | 1116 |
| Google báo chưa lập chỉ mục/đang bị loại trừ | 879 |
| Chưa gọi URL Inspection | 6772 |
| Đã gọi nhưng API lỗi, chưa biết trạng thái | 5 |
| Phản hồi chưa đủ để phân loại | 0 |

Tổng URL có ít nhất một lần gọi inspection: **2,000**. Các số trên là số URL trong inventory có bằng chứng tương ứng, **không phải tổng số index toàn website** và không phải ước lượng tỷ lệ index toàn bộ site.

**Không gán UNINSPECTED thành NOT_INDEXED. Không dùng lịch sử click hoặc việc có trong sitemap làm bằng chứng đã index ở hiện tại.** INDEXED cũng không bảo đảm URL đang hiện cho mọi truy vấn hoặc ở một vị trí cụ thể.

URL Inspection của Google có hạn mức mặc định **2.000 lượt/site/ngày, 600/phút** ([nguồn Google](https://developers.google.com/webmaster-tools/limits)). Inventory lớn hơn hạn mức một ngày. Lượt xuất này chọn tối đa 2.000 URL ưu tiên: tuyến chính, các URL có hiệu suất, rồi lấy thêm từ các kho. Không suy rộng tỷ lệ của nhóm ưu tiên sang toàn bộ inventory. Không có marker quota-stop ở thời điểm dựng báo cáo. Số inspection có giới hạn lấy mẫu/candidate và không đại diện toàn bộ inventory.

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
| `performance_pages.csv` | 992 hàng URL có số liệu Web được API trả |
| `performance_queries.csv` | 814 hàng truy vấn công khai được API trả |
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
| Google không xác định được URL | 478 |
| Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | 244 |
| Đã phát hiện thấy – hiện chưa được lập chỉ mục | 145 |
| Bị loại trừ bởi thẻ 'noindex' | 6 |
| Trang thay thế có thẻ chính tắc thích hợp | 5 |
| Trang có lệnh chuyển hướng | 1 |

Các ví dụ ưu tiên theo traffic lịch sử, tối đa 20 URL; danh sách đầy đủ trong CSV/Excel:

| URL | Coverage Google báo | Hướng kiểm tiếp |
|---|---|---|
| `https://hoathinhai.com/the-loai/trong-sinh` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/phim-tong-hop/` | Trang có lệnh chuyển hướng | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/nguoi-co-cau-tra-loi-man-with-answer` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/vi-ky-egoist-2023` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/phim-tong-hop/nguoi-ngoai-toc-phan-7` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/tuong-phan-contrast-2026` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/choi-het-minh-playboyy-2023` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/phim-tong-hop/quai-dam-tran-tong-gia?f=kk` | Trang thay thế có thẻ chính tắc thích hợp | Kiểm URL đích/canonical/redirect, sitemap và link nội bộ; có thể là loại trừ hợp lệ |
| `https://hoathinhai.com/the-loai/hien-dai` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/phim-tong-hop/56-ngay` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/chang-tai-xe-cua-toi-my-ride-2022` | Bị loại trừ bởi thẻ 'noindex' | Kiểm meta/header noindex và lỗi nguồn tạm thời; xác minh ý định trước sửa |
| `https://hoathinhai.com/blv/tuoi-tre-yeu-roi-ram-gen-y-series-2020` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/cutie-pie-2-you-2-you-2023` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/uu-tu-phan-4-elite-season-4-2021` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/phim-tong-hop/hakone-ekiden-cuoc-dua-tiep-suc-cua-chung-ta?f=kk` | Trang thay thế có thẻ chính tắc thích hợp | Kiểm URL đích/canonical/redirect, sitemap và link nội bộ; có thể là loại trừ hợp lệ |
| `https://hoathinhai.com/the-loai/he-thong` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/giai-ma-tinh-yeu-anh-bang-trai-tim-em` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/the-loai/tinh-cam` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/blv/nguoi-yeu-toi-hoa-ra-vua-la-sep-vua-la` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |
| `https://hoathinhai.com/phim-tong-hop/sat-thu-xe-lan` | Đã thu thập dữ liệu – hiện chưa được lập chỉ mục | Kiểm chất lượng nội dung, render, liên kết nội bộ, canonical và nguồn dữ liệu; không yêu cầu index hàng loạt |

Hướng kiểm là triage, không phải nguyên nhân gốc đã được chứng minh. Phải kiểm HTTP/HTML/render/canonical trên main và production mới nhất trước khi sửa.

## 5. Hiệu suất mới nhất và thương hiệu

Đã yêu cầu đến 12/11; snapshot chưa có hàng ngày12. Ngày11 còn tạm thời. Số liệu ngày gần nhất có thể tiếp tục cập nhật; query hiếm được Google ẩn. Phản hồi pages/queries có truncated=False/False; điều đó không bảo đảm API công khai mọi hàng.

| Ngày | Click | Hiển thị | CTR | Vị trí TB |
|---|---:|---:|---:|---:|
| 2026-11-01 | 116 | 1107 | 10.48% | 6.44 |
| 2026-11-02 | 120 | 1054 | 11.39% | 6.56 |
| 2026-11-03 | 104 | 985 | 10.56% | 7.08 |
| 2026-11-04 | 137 | 882 | 15.53% | 7.22 |
| 2026-11-05 | 144 | 999 | 14.41% | 7.27 |
| 2026-11-06 | 158 | 1064 | 14.85% | 8.81 |
| 2026-11-07 | 141 | 931 | 15.15% | 9.10 |
| 2026-11-08 | 109 | 774 | 14.08% | 7.57 |
| 2026-11-09 | 111 | 645 | 17.21% | 7.87 |
| 2026-11-10 | 111 | 656 | 16.92% | 8.85 |
| 2026-11-11 | 126 | 551 | 22.87% | 7.27 |

Từ khoá exact `hoathinhai`:

| Ngày | Click | Hiển thị | Vị trí TB |
|---|---:|---:|---:|
| 2026-11-06 | 9 | 54 | 2.20 |
| 2026-11-07 | 10 | 65 | 2.43 |
| 2026-11-08 | 11 | 71 | 2.15 |
| 2026-11-09 | 1 | 6 | 2.00 |
| 2026-11-10 | 0 | 2 | 2.00 |
| 2026-11-11 | 1 | 2 | 2.00 |

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
