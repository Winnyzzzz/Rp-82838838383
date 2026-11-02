# GIẢI TRÍ — THIẾT KẾ, KỊCH BẢN VÀ CÂU LỆNH TRIỂN KHAI

Ngày: 02/11/2026, giờ Việt Nam. Trạng thái: đề xuất sản phẩm; chưa sửa hoặc triển khai mã nguồn.

## 1. Hướng sản phẩm

Thay ô **Bí Cảnh** trong lưới chức năng Tông Môn bằng **Giải Trí**. Giữ tổng số 12 ô và vị trí của ô được thay. Khi bấm, mở một sảnh chơi riêng, ưu tiên toàn màn hình và bố cục ngang trên mobile.

Tên hiển thị chính: **Giải Trí**. Tên trang trí bên trong: **Hội Quán Đạo Hữu**. Dòng giới thiệu: **Một ván giao hữu, thêm một tri kỷ.**

Đây là khu trò chơi quen thuộc tại Việt Nam, gồm cả trò dân gian và các môn cờ phổ biến. Mỗi ô game có sảnh, phòng, bàn chơi, bộ luật, thành tích và bảng xếp hạng riêng; dùng chung tài khoản, bộ khung giao diện và hạ tầng kết nối.

Mặc định dùng thành tích, danh hiệu và vật phẩm trang trí riêng cho khu Giải Trí. Kết quả chơi không tự cộng/trừ Tu Vi, Thể lực hoặc Linh Thạch. Giai đoạn đầu chưa cần một loại tiền mới: huy hiệu và điểm thành tích là đủ.

## 2. Bối cảnh đã đối chiếu trong repo

Repo: https://github.com/Winnyzzzz/phimtonghop-copy, đọc các tệp từ nhánh mặc định main ngày 02/11/2026. Đây là đối chiếu có phạm vi, không phải rà soát toàn bộ repo.

- `web/src/features/game/pages/TongMon.tsx`: ô Bí Cảnh dùng key `bican`, slug `bi-canh`, mở `BicanDialog`; hiện có chặn tài khoản thường, chỉ Tông Chủ mở được. Tệp được đọc có blob SHA `2dd026ee7f092250a23020def6ddd21c3d39b6ad`.
- `web/src/features/game/components/BicanDialog.tsx`: phó bản bảy tầng theo tuần; có hệ thống thưởng và chiến đấu cũ.
- `worker/src/game/bican.ts`: luật Bí Cảnh cũ có phí Thể lực và tiến độ riêng.
- `web/package.json`: React, TypeScript, Vite, React Router, Tailwind, Lucide và Vitest/Playwright.
- `AGENTS.md`, `ARCHITECTURE.md`, `worker/README.md`, `worker/package.json`: có Worker, D1 và Durable Object hiện hữu.

Hệ quả khi triển khai:

1. Thay đúng điểm vào của Bí Cảnh, bỏ badge tiến độ tầng và thông báo chỉ Tông Chủ ở điểm vào mới.
2. Đặt tên miền chức năng mới riêng, ví dụ `entertainment`; không tái sử dụng API phó bản để xử lý chơi cờ hoặc đánh bài.
3. Không xóa bảng tiến độ, phần thưởng hay dữ liệu Bí Cảnh cũ khi đổi giao diện. Chỉ dọn mã cũ sau khi rà đủ nơi sử dụng, không dọn dữ liệu như một tác dụng phụ.
4. Không lấy tài liệu ý tưởng cũ làm căn cứ đổi toàn bộ cấu trúc website.
5. Trước khi code phải cập nhật remote, đọc lại hướng dẫn và xác minh đường dẫn thực tế. Không mặc định nội dung hôm nay vẫn nguyên khi dùng câu lệnh sau này.
6. Trước deploy, đọc scripts/config thực tế để xác nhận đúng Worker và D1 của môi trường cần sửa. Các tệp hướng dẫn đang có mô tả đích deploy chưa thống nhất; không chọn đích bằng suy đoán.

## 3. Giao diện và trải nghiệm mobile

### 3.1. Ô Giải Trí ngoài Tông Môn

- Huy hiệu tròn cùng kích thước, viền, kiểu chữ với các chức năng hiện tại.
- Biểu tượng gợi ý: quân cờ và hai lá bài trên nền ngọc bích; tên đặt bằng chữ giao diện, không vẽ chữ vào ảnh.
- Mô tả ngắn: **Cờ, bài và trò vui cùng đạo hữu**.
- Giữ vị trí ô Bí Cảnh trong thứ tự lưới hiện tại.

### 3.2. Sảnh chung

- Phong cách hội quán Việt pha cổ phong của website; nền gỗ nâu, xanh ngọc, ánh vàng ấm.
- Thanh trên: trở về Tông Môn, tên sảnh, hồ sơ Giải Trí, âm thanh, toàn màn hình.
- Khu chính: các thẻ game có tranh riêng, tên, số người/ván và trạng thái thực tế.
- Bộ lọc: **Tất cả / Cờ trí tuệ / Bài & vui / Dân gian / Yêu thích**.
- Có mục **Tiếp tục ván đang chơi** khi máy chủ xác nhận còn ván hợp lệ.
- Bố cục thường: 3 cột trên điện thoại nằm ngang, 4 cột khi đủ rộng; màn hình thấp được cuộn. Không ép 8 ô vào một khung làm chữ và nút quá nhỏ.
- Không hiển thị số người online hoặc phòng giả như số liệu thật. Nếu chỉ biết số phòng trong danh sách hiện tại, gọi đúng là số phòng đang hiển thị.
- Chỉ dùng trạng thái **Chơi ngay** khi game đã có luật và luồng chơi hoạt động. Game chưa làm hiển thị **Sắp ra mắt**.

### 3.3. Toàn màn hình và xoay ngang

Web chỉ có thể yêu cầu khóa hướng khi API, trình duyệt và ngữ cảnh cho phép; không cam kết mọi thiết bị tự xoay.

- Trong thao tác bấm mở Giải Trí, gọi yêu cầu toàn màn hình trên phần tử đã tồn tại; tránh chờ fetch hoặc lazy import làm mất user activation.
- Sau khi vào toàn màn hình, thử `screen.orientation.lock("landscape")` khi có hỗ trợ.
- Bắt cả lỗi toàn màn hình và khóa hướng. Không coi sự tồn tại của API là bảo đảm lời gọi thành công.
- Nếu cần thêm thao tác, có nút **Vào toàn màn hình** trong sảnh để thử lại bằng thao tác của người dùng.
- Nếu máy còn dọc, hiện hướng dẫn có thể đóng: **Xoay ngang điện thoại để bàn chơi rộng và dễ thao tác hơn.** Có nút **Tiếp tục ở màn hình dọc**.
- Trên desktop không ép khóa hướng.
- Dùng chiều cao viewport động và safe area. Có phương án cho thanh địa chỉ, bàn phím ảo, tai thỏ và màn hình ngang thấp.
- Không quay cả trang 90 độ bằng CSS để giả lập xoay thiết bị.
- Thoát fullscreen không đồng nghĩa rời hoặc xử thua ván.
- Khi rời khu Giải Trí, tháo listener, mở khóa hướng nếu khu này đã khóa và thoát fullscreen nếu chính khu này sở hữu phiên fullscreen. Không ép máy trở về dọc bằng một lời gọi khóa mới.

### 3.4. Sảnh riêng và bàn chơi

Mỗi ô dẫn đến sảnh riêng có: **Chơi nhanh / Tạo phòng / Nhập mã phòng / Luyện tập / Luật chơi / Thành tích / Xếp hạng**. Chỉ hiện chế độ đã triển khai; không để nút giả.

Bàn chơi có vùng trung tâm lớn, avatar và đồng hồ quanh bàn, thanh thao tác chính ở dưới. Tin nhắn nhanh và emote không che quân/bài. Hỗ trợ chọn rồi xác nhận; thao tác quan trọng không phụ thuộc hoàn toàn vào kéo thả.

## 4. Danh mục 8 game và hệ thống riêng

| Game | Người/ván | Không gian | Hệ thống riêng cần có |
|---|---:|---|---|
| Tiến Lên Miền Nam | 2–4 | Bàn bài xanh ngọc, ghế quanh bàn | 13 lá/người, sẵn sàng, sắp bài, chọn bộ, đánh/bỏ lượt, luật chặt, thứ hạng kết thúc, thống kê vị trí |
| Caro | 2 | Bàn gỗ, giấy sáng, quân X/O rõ | Luật năm quân có phiên bản, đồng hồ, gợi ý ô hợp lệ, lịch sử nước, phòng giao hữu và hạng riêng |
| Cờ Vua | 2 | Bàn cờ sáng tối trang nhã | Nước hợp lệ, chiếu, chiếu hết, hòa, phong cấp, nhập thành, bắt tốt qua đường, đồng hồ và kỳ phổ |
| Cờ Tướng | 2 | Gỗ trầm, quân đỏ/đen | Đúng luật từng quân, cản mã/mắt tượng, lộ mặt tướng, chiếu/hết nước, quy tắc lặp và biên bản |
| Ô Ăn Quan | 2 | Sân đình, sỏi và nền đất ấm | Chọn ô, hướng rải, ăn quân, quy đổi quan/dân, kết thúc và tính điểm |
| Cờ Gánh | 2 | Bàn tre gỗ, quân hai màu | Luật di chuyển, gánh, vây; đánh dấu quân chuyển phe và bài luyện chiến thuật |
| Cờ Cá Ngựa | 2–4 | Bàn nhiều màu, vui tươi | Xúc xắc, xuất chuồng, chọn ngựa, đá/về đích, thứ tự hoàn thành |
| Oẳn Tù Tì | 2 | Sân đấu vui, hoạt ảnh ngắn | Khóa lựa chọn, công bố đồng thời, đấu ba hoặc năm lượt thắng, chuỗi thành tích |

Mở rộng sau khi 8 game ổn định: **Cờ Đam**, **Đố Vui Việt Nam**, **Đuổi Hình Bắt Chữ**. Hai game đố vui cần kho nội dung biên tập riêng; không để AI bịa đáp án rồi đưa vào xếp hạng.

### 4.1. Phân tách thành tích

- Caro, Cờ Vua, Cờ Tướng có rating riêng; phân biệt luật và nhóm thời gian khi cần.
- TLMN dùng điểm theo thứ hạng của ván nhiều người, không lấy công thức Elo hai người áp thẳng cho bốn người.
- Ô Ăn Quan lưu thắng/thua, điểm ăn quân và thành tích theo luật đã chọn.
- Cờ Gánh lưu thắng/thua và bài luyện hoàn thành.
- Cờ Cá Ngựa lưu thứ hạng và số ván hoàn thành.
- Oẳn Tù Tì lưu trận thắng, chuỗi thắng và số trận; không gắn danh hiệu kỳ thủ.
- Luyện tập với máy và ván chơi trên cùng thiết bị không cộng hạng online.
- Một tài khoản có thể đứng cao ở Caro nhưng chưa có hạng Cờ Vua. Mọi bảng đều hiển thị đúng game, chế độ, luật và mùa nếu có.
- Mặc định v1 dùng bảng tích lũy; hệ thống mùa giải chỉ bật khi đã có luật kết mùa và xử lý phần thưởng rõ ràng.

### 4.2. Luật và phạm vi cần chốt trong đặc tả trước khi viết engine

Mỗi game có `gameId`, `rulesVersion`, cấu hình phòng và tài liệu luật tiếng Việt. Cấu hình khóa khi ván bắt đầu. Luật giao hữu khác xếp hạng phải được phân nhóm dữ liệu.

- **TLMN:** công bố thứ tự chất, quyền đi đầu khi ít hơn bốn người, bộ hợp lệ, so sánh bộ, bảng chặt, bỏ lượt/quyền vào lại vòng, cách kết thúc ván và xử lý mất kết nối. Bản đầu có thể là **TLMN cơ bản v1**, tắt các biến thể tới trắng, đền và chặt trái lượt; phải ghi rõ trong luật phòng, không quảng bá như đã có mọi biến thể. Không tự pha luật miền Bắc. Các biến thể nâng cao bật sau khi có luật và kiểm chứng riêng.
- **Caro:** mặc định đề xuất bàn 15×15, đúng năm quân liên tiếp; không thắng nếu hai đầu bị quân đối phương chặn; mép bàn không tự coi là quân đối phương; chuỗi từ sáu quân không thắng theo bộ luật này. Đặt tên **Caro Việt v1**. Nếu thêm luật năm-quân-trở-lên thì đặt phiên bản/phòng khác.
- **Cờ Vua:** dùng engine luật đã kiểm chứng và kiểm tra giấy phép; engine luật và engine AI là hai trách nhiệm khác nhau. Cần phân biệt hòa tự động và quyền yêu cầu hòa theo bộ luật áp dụng. Không dùng cách “bắt vua” để kết thúc.
- **Cờ Tướng:** công bố bộ quy tắc lặp, chiếu dai và đuổi dai. Không đưa vào hạng chính thức khi các trường hợp này chưa được đặc tả và kiểm chứng.
- **Ô Ăn Quan:** ghi rõ bố trí ban đầu, giá trị quan, hướng rải, ăn nối, vay quân và cách kết thúc. Đây là những chỗ có thể khác nhau theo địa phương.
- **Cờ Gánh:** công bố biến thể v1, vị trí xuất phát, điều kiện gánh/vây và việc có áp dụng luật “mở” hay không. Không tự thêm luật địa phương vào giữa ván.
- **Cờ Cá Ngựa:** ghi rõ số ngựa, số nút xuất chuồng, lượt gieo thêm, xử lý nhiều lần ra sáu và quy tắc về đích.
- **Oẳn Tù Tì:** lựa chọn của một người không gửi cho người kia trước khi cả hai đã chốt hoặc hết hạn. Hòa một lượt không được tính thành thắng.

AI chơi theo cùng luật với người. TLMN AI chỉ dùng dữ liệu mà ghế đó được phép biết, không đọc bài kín của người khác.

## 5. Kịch bản người chơi

### 5.1. Vào sảnh trên điện thoại

1. Người dùng ở Tông Môn bấm huy hiệu Giải Trí.
2. Khu chơi mở, yêu cầu fullscreen và thử khóa ngang.
3. Nếu được chấp nhận, sảnh tự chuyển ngang. Nếu bị từ chối, hiện hướng dẫn xoay máy có thể đóng; vẫn mở được các game.
4. Người chơi chọn một game và thấy đúng sảnh con, không vào ngay một phòng ngẫu nhiên.
5. Trở về Tông Môn bằng nút rõ ràng; các lớp giao diện và khóa hướng được dọn đúng.

### 5.2. Một ván TLMN với bạn

1. Chọn TLMN → Tạo phòng → bốn ghế → luật TLMN cơ bản v1 → Giao hữu.
2. Máy chủ tạo mã phòng; chủ phòng bấm sao chép mã/link rồi tự gửi cho bạn.
3. Người vào phòng thấy avatar, ghế, luật và nút Sẵn sàng.
4. Chủ phòng chỉ bắt đầu khi đủ điều kiện. Không tự thêm bot giả làm người thật.
5. Máy chủ chia bài; mỗi máy chỉ nhận bài của chính mình và số lượng bài đối thủ.
6. Người đến lượt chọn bài → Đánh; nút bị vô hiệu khi bộ không hợp lệ, có lý do dễ hiểu.
7. Đồng hồ chạy theo hạn do máy chủ xác định. Hết giờ thực hiện đúng luật đã công bố.
8. Kết thúc hiện thứ hạng từng người và lịch sử ván; giao hữu không cộng hạng.
9. Chọn Chơi lại; mọi người xác nhận sẵn sàng cho ván mới.

### 5.3. Một ván Caro xếp hạng

1. Chọn Caro → đọc luật mặc định → Chơi xếp hạng.
2. Dùng tài khoản hiện có. Máy chủ ghép đúng hàng chờ của game và luật.
3. Không đủ đối thủ thì hiện đang tìm và cho hủy; có nút chuyển sang luyện tập được ghi rõ.
4. Bàn chỉ chấp nhận nước đi từ ghế đang đến lượt, ô còn trống và ván chưa kết thúc.
5. Máy chủ chốt kết quả. Màn kết quả chỉ hiện hạng mới khi kết quả đã được lưu.
6. Không có xác nhận máy chủ thì không tự hiện “đã cộng điểm”.

### 5.4. Mất mạng, đổi ứng dụng và trở lại

- Hiển thị trạng thái đang kết nối lại; giữ hình bàn gần nhất nhưng không giả vờ đã gửi thành công.
- Sau khi nối lại, lấy snapshot và số thứ tự trạng thái mới nhất từ máy chủ.
- Không gửi lặp nước cũ như một nước mới.
- Đồng hồ của trận online vẫn theo máy chủ khi người chơi đổi ứng dụng.
- Thời hạn trở lại và kết quả bỏ cuộc được nêu trước ván. Khoảng 30–60 giây chỉ là gợi ý thiết kế, không tự kéo dài đồng hồ môn cờ.
- Thoát fullscreen hoặc xoay máy không bị coi là bỏ cuộc.

## 6. Kiến trúc đề xuất

### 6.1. Hạ tầng dùng chung

Dùng React/TypeScript và Worker hiện có. Một lớp Durable Object mới cho phòng Giải Trí có thể nằm trong cùng Worker; mỗi phòng là một instance, không phải mỗi game tạo một dịch vụ mới. Không dùng chung trạng thái phòng game với phòng chat Luận Đạo.

Đường dẫn gợi ý, phải đối chiếu router/middleware trước khi chốt:

- `/giai-tri`
- `/giai-tri/:gameId`
- `/giai-tri/:gameId/phong/:roomId`
- API dưới namespace mới, chẳng hạn `/api/entertainment/*`

Cần xử lý tải lại trực tiếp các URL mới, SEO/middleware không trả 404 nhầm, và metadata phù hợp. Phòng riêng không đưa vào sitemap, tránh lộ mã phòng qua URL preview hoặc chỉ mục công khai.

Dùng lại phiên đăng nhập hiện hữu. Đề xuất cho khách xem sảnh và luyện tập cục bộ; online/xếp hạng dùng tài khoản. Không dựng hệ thống đăng nhập thứ hai.

### 6.2. Mỗi game là một module

Mỗi module có:

- Metadata, trạng thái phát hành, luật và cấu hình phòng.
- Engine hàm thuần: khởi tạo, liệt kê/kiểm tra hành động, áp dụng hành động, xác định kết quả.
- Giao diện bàn, bộ thao tác và cách trình bày kết quả riêng.
- Bộ chuyển đổi trạng thái công khai/riêng tư.
- Cách lưu thống kê và tính hạng đúng game.
- AI luyện tập nếu đã có; không bắt buộc mọi game cùng một đợt đều có ba độ khó.

Có registry để thêm module mà không phải sửa một component khổng lồ. Tổ chức thư mục theo repo hiện tại, không tái cấu trúc cả dự án để phục vụ một tính năng.

### 6.3. Máy chủ quyết định trận online

- Máy chủ xác thực người chơi, ghế, lượt, luật, thời gian và kết quả.
- Dữ liệu gửi về từng ghế phải được lọc ngay phía server. Không gửi toàn bộ bài rồi chỉ ẩn bằng CSS.
- `matchId`, `actionId`, phiên bản trạng thái và thứ tự sự kiện ngăn thao tác lặp, trạng thái cũ và tranh chấp.
- Xáo bài/xúc xắc online dùng nguồn ngẫu nhiên mật mã phía server, không nhận kết quả do client tự gửi.
- WebSocket dùng vé ngắn hạn, giới hạn phòng/danh tính, có thời hạn và chống dùng lại. Không để token phiên đăng nhập dài hạn vào URL/log.
- Kết quả cuối và thay đổi hạng được ghi đúng một lần; cần xử lý retry hoặc lỗi ghi một phần bằng transaction/batch phù hợp và khóa duy nhất theo trận.
- Tách lỗi xác thực, hết hạn phòng, sai lượt, hành động không hợp lệ và mất kết nối bằng thông báo chính xác.

### 6.4. Realtime, bền dữ liệu và chi phí

- Dùng WebSocket theo sự kiện cho phòng đang tham gia. Không polling trạng thái bàn mỗi giây.
- Dùng Hibernation WebSocket API nếu môi trường hỗ trợ; kiểm tra export class, binding, migration và script deploy hiện có.
- Lưu trạng thái hoặc nhật ký đủ khôi phục vào storage bền của Durable Object sau hành động hợp lệ. Hibernation xóa trạng thái trong bộ nhớ; không được chỉ giữ trận trong RAM.
- Đồng hồ trên máy người chơi chỉ vẽ từ deadline; không fetch mỗi giây. Máy chủ kiểm tra deadline khi xử lý hành động và dùng alarm khi cần.
- Danh sách phòng/xếp hạng tải khi mở và cập nhật theo nhu cầu; dữ liệu ít đổi được cache. Không tạo kết nối nền cho cả tám game.
- Luyện tập cục bộ xử lý trong trình duyệt; không tự gửi từng nước luyện tập lên D1.
- D1 lưu kết quả trận, người tham gia và thống kê/hạng; phần trạng thái đang đánh nằm ở storage phòng.
- Chốt chính sách giữ replay, TTL phòng và dọn dữ liệu; không lưu replay vô hạn.

Ví dụ tải để thảo luận, không phải số đo thực tế hoặc cam kết chi phí:

- 100 ván/ngày × 80 hành động hợp lệ/ván = **8.000 hành động/ngày**.
- Nếu toàn bộ là ván bốn người, mỗi ván ghi 1 dòng trận + 4 dòng người tham gia + 4 dòng hồ sơ: khoảng **900 lần ghi dòng logic vào D1/ngày**, chưa tính ghi do chỉ mục, retry, mùa giải hoặc phần thưởng.
- Với phòng lưu mỗi hành động vào Durable Object, phải tính riêng số dòng đọc/ghi DO, snapshot, alarm và dung lượng replay; giảm ghi D1 không có nghĩa không tốn storage.
- Cần tính thêm tạo/vào phòng, bắt tay, xác thực, ghép trận, chat, kết nối lại, thời gian thực thi và dữ liệu gửi ra.
- Không đồng nhất hành động, HTTP request, WebSocket message, dòng D1 và request tính phí. Cloudflare có quy tắc đo/tính riêng cho các loại này.
- Trước khi code phần realtime, lập bảng theo mô hình 10 / 100 / 1.000 ván/ngày và đối chiếu hạn mức thực tế lẫn mục 11 của AGENTS.md. Nếu vượt ngưỡng cần lựa chọn theo hướng dẫn repo, nêu đánh đổi ở đúng bước; không mặc định gói miễn phí luôn đủ.

## 7. Triển khai theo đợt

| Đợt | Nội dung | Điều kiện hoàn thành |
|---|---|---|
| 1 | Thay điểm vào, shell, xoay ngang/fallback, registry; Caro và Ô Ăn Quan có luật và ván chơi thật | Mobile thao tác được, hai game chơi đến kết quả, có luyện tập hoặc giao hữu đã ghi rõ; dữ liệu game cũ không bị thay đổi |
| 2 | Hoàn thiện khung phòng online, ghép trận/kết quả; TLMN, Cờ Vua, Cờ Tướng | Các game mới có luật và tình huống đặc biệt đã kiểm; thông tin kín, đồng hồ, reconnect và lưu kết quả hoạt động |
| 3 | Cờ Gánh, Cờ Cá Ngựa, Oẳn Tù Tì; hoàn thiện thành tích/hạng riêng từng game | Đủ tám game; không còn nút/chế độ giả; từng bảng hạng đọc đúng dữ liệu |
| 4 | Tùy chọn: sự kiện giao hữu, giải đấu, xem lại ván, khán giả, trang trí | Chỉ thêm sau khi game lõi ổn định và có ngân sách vận hành |

Trong giai đoạn chuyển tiếp, chưa có hệ thống hạng hoặc online thì không hiện như đã có. Danh sách tám game có thể xuất hiện từ đợt 1 nhưng game chưa triển khai phải mang nhãn Sắp ra mắt. Tiếp tục các đợt đã giao tới khi đủ phạm vi, không coi hoàn thành shell là hoàn thành sản phẩm.

## 8. Tiêu chí nghiệm thu

### Sản phẩm và mobile

- Trong lưới Tông Môn có Giải Trí đúng vị trí Bí Cảnh, vẫn 12 ô.
- Tài khoản thường mở được Giải Trí; không thừa hưởng điều kiện chỉ Tông Chủ của phó bản.
- Android có hỗ trợ và trường hợp từ chối API đều hoạt động; iPhone/Safari và webview có đường dự phòng.
- Kiểm tra API không tồn tại, requestFullscreen reject, orientation lock reject, mở bằng URL trực tiếp, xoay máy giữa ván, Back và thoát fullscreen.
- Emulator chỉ chứng minh bố cục, không đủ để khẳng định thiết bị thật tự xoay.
- Kiểm bố cục 360×800, 390×844, 800×360, 844×390 và desktop; thiết bị thật được ghi rõ nếu đã có điều kiện kiểm.
- Nút chính dùng được bằng chạm/chọn-xác nhận; không bị tai thỏ, thanh trình duyệt hay lớp chat che.

### Luật và online

- TLMN: lá bài không trùng, bài người khác không lộ qua payload/snapshot, đi đầu khi thiếu ghế, so bộ, chặt, bỏ lượt, người hết bài và kết thúc ván.
- Caro: các hướng thắng, chuỗi dài, chặn hai đầu, mép bàn, hòa kín bàn và đánh vào ô đã dùng.
- Cờ Vua: nước làm vua mình bị chiếu, nhập thành qua ô bị tấn công, en passant, phong cấp, chiếu hết và các loại hòa.
- Cờ Tướng: mã bị cản, tượng bị chặn, giới hạn sông/cung, pháo, lộ mặt tướng, hết nước, lặp/chiếu dai theo luật đã chốt.
- Ô Ăn Quan: bảo toàn số quân sau rải/ăn, quy đổi điểm, vay và kết thúc đúng biến thể.
- Cờ Gánh: gánh/vây đổi quân đúng; không đổi quân chỉ vì hoạt ảnh.
- Cờ Cá Ngựa: nước theo xúc xắc, chặn/đá, về đích và thứ hạng.
- Oẳn Tù Tì: không biết lựa chọn đối thủ trước khi chốt, hòa, hết hạn, lượt thắng và kết quả cả trận.
- Kiểm hai thiết bị hoặc hai phiên độc lập; không chỉ kiểm một màn hình tự đổi cả hai bên.
- Kiểm hành động trùng, sai phiên bản, sai người/sai ghế, gửi sau kết thúc, reconnect và ghi kết quả lặp.
- Kiểm sau khi DO ngủ/khởi động lại và khi D1 ghi lỗi; không mất ván hoặc nhân đôi hạng.

### Kiểm kỹ thuật

Đọc lại AGENTS.md và chạy typecheck theo thư mục đã sửa, cùng các test có liên quan. Đây là tính năng có nhiều luật và trạng thái tranh chấp, nên cần test engine và luồng online có ý nghĩa. Không tự chạy toàn bộ test suite khi hướng dẫn repo yêu cầu chỉ chạy từng tệp. Báo trung thực phần nào đã kiểm, phần nào chưa có thiết bị hoặc môi trường.

## 9. Câu lệnh triển khai có thể sao chép

Đoạn dưới giao cho coding agent xây sản phẩm, khác với việc đang lên ý tưởng trong cuộc trao đổi này.

```text
Bạn là Senior Product Designer, Game Systems Designer và Full-stack Engineer.

Làm việc trên repo https://github.com/Winnyzzzz/phimtonghop-copy.
Hãy triển khai khu GIẢI TRÍ thay ô BÍ CẢNH trong Tông Môn, theo từng đợt có sản phẩm chơi được và tiếp tục tới khi hoàn tất phạm vi tám game bên dưới.

A. ĐỌC HIỆN TRẠNG TRƯỚC KHI SỬA
- Kiểm tra worktree, cập nhật remote và xác định HEAD/nhánh thực tế; giữ mọi thay đổi sẵn có. Không dựa vào bản checkout hoặc báo cáo cũ.
- Đọc AGENTS.md ở gốc và các thư mục liên quan, README, ARCHITECTURE, router/middleware, lớp request, auth, Worker/DO/D1 và scripts/config deploy.
- Tìm điểm vào Bí Cảnh thực tế. Các tệp từng liên quan là TongMon.tsx, BicanDialog.tsx và worker/src/game/bican.ts; phải xác minh lại bằng mã hiện tại.
- Đây là tính năng cho website hiện tại; không khởi động lại dự án theo tài liệu ý tưởng cũ.
- Xác minh đúng Worker/D1 đích từ mã cấu hình và script, không suy đoán từ một đoạn README. Làm git/deploy theo hướng dẫn repo hiện hành và phạm vi người dùng đã giao.

B. ĐIỂM VÀO VÀ THIẾT KẾ
- Thay ô Bí Cảnh bằng Giải Trí, giữ huy hiệu tròn, vị trí và tổng số 12 chức năng.
- Bỏ badge tiến độ tầng, tooltip phó bản và điều kiện chỉ Tông Chủ tại điểm vào mới. Người dùng thường mở được Giải Trí.
- Tạo namespace/module mới; không tái dùng API Bí Cảnh để xử lý game giải trí. Giữ dữ liệu cũ, không xóa bảng hay tự chuyển thưởng/thể lực sang game mới.
- Mở sảnh riêng “Giải Trí — Hội Quán Đạo Hữu”, phong cách hội quán Việt hòa với giao diện hiện có; gỗ ấm, xanh ngọc, ánh vàng, chữ rõ.
- Có thẻ game với hình riêng, tên, số người và trạng thái thật; bộ lọc và yêu thích; trở về Tông Môn, âm thanh và toàn màn hình.
- Mỗi game mở sảnh con riêng: Chơi nhanh, Tạo phòng, Nhập mã phòng, Luyện tập, Luật chơi, Thành tích, Xếp hạng. Chỉ bật các chế độ đã làm xong, không có nút giả.
- Không bịa phòng, người online, thành tích hoặc đối thủ rồi hiển thị như người thật. Bot phải được ghi rõ.

C. MOBILE: THỬ XOAY NGANG, CÓ FALLBACK
- Khi người dùng bấm vào Giải Trí, yêu cầu fullscreen bằng chính user gesture trên phần tử đã mount; tránh chờ fetch/lazy-load trước lời gọi làm mất activation.
- Khi được hỗ trợ và đúng điều kiện, thử screen.orientation.lock("landscape"); bắt mọi trường hợp bị từ chối.
- Nếu không được, vẫn mở sảnh; hiện hướng dẫn xoay máy có thể đóng, nút Tiếp tục màn hình dọc và nút Vào toàn màn hình để thử lại.
- Không cam kết web xoay được mọi điện thoại; không dùng CSS rotate toàn trang giả làm khóa hướng.
- Dùng viewport động, safe area; hỗ trợ màn hình ngang thấp, bàn phím và xoay giữa ván. Desktop không ép hướng.
- Thoát fullscreen không làm mất ván hoặc xử thua. Rời khu thì cleanup listener, unlock và exitFullscreen theo quyền sở hữu của khu.

D. TÁM GAME, MỖI GAME CÓ HỆ THỐNG RIÊNG
1. Tiến Lên Miền Nam: 2–4 ghế, 13 lá/người; chia và giữ kín bài; chọn/sắp bài, đánh/bỏ lượt, so bộ/chặt và thứ hạng. Viết rõ luật phòng có phiên bản, đặc biệt quyền đi đầu khi thiếu ghế và quyền tham gia lại vòng. Bản cơ bản được tắt biến thể nâng cao nhưng phải ghi rõ, không pha luật miền Bắc.
2. Caro: bàn 15×15; mặc định Caro Việt v1, đúng năm quân, hai đầu bị quân đối phương chặn thì chưa thắng, biên không tự tính là quân chặn, sáu quân trở lên không thắng. Có đồng hồ và lịch sử nước; biến thể khác phải tách luật và hạng.
3. Cờ Vua: đủ luật nước đi, chiếu, chiếu hết/hòa, nhập thành, en passant, phong cấp, đồng hồ và kỳ phổ. Ưu tiên engine luật đã kiểm chứng; đọc giấy phép. Không coi bắt vua là kết thúc. Phân biệt hòa tự động và yêu cầu hòa theo luật.
4. Cờ Tướng: đúng luật từng quân, cản mã/mắt tượng, cung/sông, pháo, lộ mặt tướng, hết nước; quy định lặp/chiếu dai/đuổi dai rõ trước khi bật xếp hạng.
5. Ô Ăn Quan: luật rải/ăn, giá trị quan/dân, vay quân và kết thúc có tài liệu; hoạt ảnh phản ánh đúng trạng thái.
6. Cờ Gánh: có bố trí ban đầu, di chuyển, gánh/vây và biến thể “mở” được công bố; không tự thay luật giữa ván.
7. Cờ Cá Ngựa: 2–4 người, xúc xắc server, xuất chuồng, chọn ngựa, đá/về đích và xếp thứ tự; công bố điều kiện lượt thêm.
8. Oẳn Tù Tì: chọn kín, khóa lựa chọn, công bố khi cả hai đã chốt/hết hạn, đấu theo số lượt thắng; không lộ lựa chọn trước.

- Mỗi module có metadata, rulesVersion, cấu hình phòng, engine hàm thuần, giao diện bàn, hành động, kết quả, thống kê và cách tính hạng riêng.
- Khóa luật khi bắt đầu. Tách hạng theo game/chế độ/luật phù hợp; không cộng hạng online cho luyện máy hoặc chơi cùng thiết bị.
- TLMN nhiều người cần mô hình điểm theo thứ hạng, không áp thẳng Elo hai người.
- Dùng danh hiệu và phần thưởng trang trí riêng. Kết quả không tự cộng/trừ Tu Vi, Thể lực hay Linh Thạch.
- Dùng lại tài khoản hiện có. Khách có thể xem sảnh/luyện tập cục bộ; online và hạng dùng đăng nhập hiện hữu.

E. ONLINE, DỮ LIỆU VÀ CHI PHÍ
- Dùng Worker và hạ tầng hiện có; registry cho từng game. Có thể thêm lớp DO phòng Giải Trí trong cùng Worker; mỗi phòng một instance, tách khỏi trạng thái chat Luận Đạo.
- Dùng WebSocket theo sự kiện, ưu tiên Hibernation API tương thích cấu hình. Không polling bàn mỗi giây hoặc mở kết nối cho tất cả game cùng lúc.
- Server giữ quyền quyết định: danh tính, ghế, lượt, nước hợp lệ, deadline, chia bài/xúc xắc, kết quả và hạng.
- Gửi trạng thái riêng đúng từng người; tuyệt đối không gửi bài người khác rồi chỉ ẩn bằng CSS. Bot không được biết bài kín ngoài ghế của nó.
- Có matchId, actionId, phiên bản/sequence, chống thao tác lặp và đồng bộ snapshot khi reconnect.
- WebSocket dùng vé ngắn hạn giới hạn phòng/danh tính và chống dùng lại; không đặt token đăng nhập dài hạn vào URL/log.
- Lưu bền trạng thái/journal trong DO để phục hồi sau hibernation/restart; không giữ ván chỉ trong RAM. Tính cả chi phí snapshot, alarm, replay và dọn dữ liệu.
- Đồng hồ client vẽ từ deadline server. Đổi ứng dụng/mất mạng không tự dừng thời gian của trận online.
- D1 lưu kết quả, người tham gia và thống kê/hạng với transaction/batch và khóa duy nhất phù hợp để retry không cộng hai lần.
- Tải danh sách phòng/hạng theo nhu cầu, có cache và phân trang. Luyện tập cục bộ không ghi từng nước lên D1.
- Trước phần realtime, ước lượng theo 10/100/1.000 ván mỗi ngày: HTTP, kết nối/WS message, thời gian DO, dòng đọc/ghi D1 và DO, replay. Phân biệt tải thực với đơn vị tính phí; đối chiếu tài liệu Cloudflare hiện hành và mục ngân sách AGENTS.md.
- Nếu cần chọn đánh đổi vượt ngưỡng repo, nêu con số và phương án tại đúng bước. Không khẳng định realtime miễn phí hoặc không dùng request.
- Có TTL phòng, giới hạn replay, rate limit thao tác/chat và thông báo lỗi chính xác.
- URL game/phòng tải lại được; xử lý router, middleware và metadata; không đưa phòng riêng vào sitemap.

F. THỨ TỰ HOÀN THÀNH
- Đợt 1: thay điểm vào, shell, landscape/fallback, registry; Caro và Ô Ăn Quan chơi thật tới kết quả.
- Đợt 2: phòng online, đồng bộ/kết quả; TLMN, Cờ Vua, Cờ Tướng.
- Đợt 3: Cờ Gánh, Cờ Cá Ngựa, Oẳn Tù Tì; hoàn thiện thành tích và hạng từng game.
- Tiếp tục các đợt trong phạm vi đã giao, không dừng sau bản UI. Game chưa xong ghi Sắp ra mắt; chế độ chưa xong không bật.
- Giải đấu, khán giả, replay nâng cao và mở rộng game làm sau phạm vi lõi này.

G. KIỂM CHỨNG VÀ BÀN GIAO
- Đọc lại AGENTS.md và chạy typecheck đúng phần sửa, test liên quan và build cần thiết; không tự chạy toàn bộ suite khi repo không cho phép.
- Viết test có ý nghĩa cho luật, thông tin kín, sai lượt, thao tác lặp, timeout, reconnect, khôi phục DO và ghi kết quả đúng một lần.
- Kiểm hai phiên độc lập; đầy đủ tình huống đặc biệt của từng game. Không chỉ kiểm giao diện hoặc cho cả hai bên chạy trên một state client.
- Kiểm mobile dọc/ngang, fullscreen/lock bị từ chối, API không tồn tại, Back, tải lại URL, xoay giữa trận và thoát fullscreen.
- Emulator không đủ chứng minh auto xoay trên máy thật; báo rõ thiết bị thật nào đã/chưa kiểm.
- Cập nhật tài liệu và changelog cùng thay đổi; tài liệu mô tả đúng bản đã hoàn thành.
- Bàn giao từng đợt: hành vi đã hoạt động, tệp/commit, kiểm đã chạy và kết quả, môi trường/đích deploy đã xác minh, số đo/ước lượng tài nguyên và phần còn lại. Không báo hoàn thành game khi mới có thẻ hoặc màn hình.
```

## 10. Nguồn kỹ thuật

Các nguồn dưới được đối chiếu ngày 02/11/2026. Cần kiểm tra lại khi triển khai.

- MDN, ScreenOrientation.lock(): https://developer.mozilla.org/en-US/docs/Web/API/ScreenOrientation/lock
- MDN, Element.requestFullscreen(): https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullscreen
- Cloudflare, WebSockets và Hibernation: https://developers.cloudflare.com/durable-objects/best-practices/websockets/
- Cloudflare, đo lường và giá Durable Objects: https://developers.cloudflare.com/durable-objects/platform/pricing/

Theo tài liệu Cloudflare, số message WebSocket gửi vào và request tính phí không cùng đơn vị; DO storage cũng có hạn mức/chi phí riêng. Thiết kế tiết kiệm D1 vẫn cần đo cả DO, không chỉ đếm các fetch từ trình duyệt.

