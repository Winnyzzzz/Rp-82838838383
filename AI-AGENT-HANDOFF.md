# Câu lệnh giao AI agent kiểm tra và sửa SEO

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
