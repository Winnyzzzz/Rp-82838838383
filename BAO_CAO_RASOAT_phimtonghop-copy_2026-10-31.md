# Báo cáo rà soát phimtonghop-copy

Ngày kiểm tra: **31/10/2026, theo giờ Việt Nam**.

Repo: https://github.com/Winnyzzzz/phimtonghop-copy

Phiên bản chốt: **main — dd694d3bdfc49d979146b8df13d7db4589cc710a**, commit lúc 10:09:22 ngày 31/10/2026.

**Không sửa mã nguồn, không commit, không push, không deploy. Không gửi email thật, giao dịch thật, tặng quà thật, nhận thưởng thật hay thay đổi kho phim Production.** Các phép thử có ghi dữ liệu đều dùng dữ liệu giả và database cục bộ.

## 1. Kết quả chính

Xác nhận **18 vấn đề về hành vi và luồng dữ liệu**, trong đó 5 vấn đề được xếp P1 cần ưu tiên. Ngoài ra có các vấn đề về lockfile, test và khả năng chạy lại migration.

Không cộng số cảnh báo dependency hoặc số test đỏ vào số lỗi hành vi. Không coi tính năng đã chủ động khóa hoặc gỡ giao diện là lỗi chỉ vì người chơi không mở được.

| Mã | Mức | Phát hiện |
|---|---|---|
| F01 | P1 | API Đạo Lữ còn được giữ sau khi gỡ giao diện; tặng quà đồng thời sinh thêm Linh Thạch |
| F02 | P1 | Quét tối đa 12 mùa nhưng kết luận cả phim đã hỏng, dù mùa 13 còn xem được |
| F03 | P1 | Cửa dừng khi hơn 40% phim bị coi là hỏng không hoạt động với lô 8 phim của giao diện |
| F04 | P1 | Luồng báo nguồn bất thường bị chặn bởi quyền mới của `/api/mirror/diag` |
| F05 | P1 | Hai người mua đồng thời có thể làm người bán vượt trần giao dịch ngày |
| F06 | P2 | Thư viện phim và lịch sử xem của A được gửi lên tài khoản B trên cùng trình duyệt |
| F07 | P2 | Đăng xuất ở tab khác nhưng tab đã đăng nhập vẫn giữ phiên trong bộ nhớ |
| F08 | P2 | Giao diện yêu cầu mật khẩu 6 ký tự, backend yêu cầu 8 ký tự |
| F09 | P2 | Thương Hội cho Luyện Khí giao dịch dù điều kiện được mô tả là Trúc Cơ |
| F10 | P2 | Xóa tài khoản để lại tin Thương Hội; mua tin cũ có thể tạo lại dữ liệu tu luyện của tài khoản đã xóa |
| F11 | P2 | Một số hành động game ghi nhiều bước rời nhau: lỗi giữa chừng làm mất đồ hoặc nhận lặp tiền |
| F12 | P2 | Hai yêu cầu quên mật khẩu đồng thời vượt được khoảng chờ gửi mã |
| F13 | P2 | Gửi mail hàng loạt quá hạn chờ 12 giây của frontend dù server vẫn xử lý |
| F14 | P2 | Đơn thanh toán cũ không tự hết trạng thái pending, có thể khóa việc tạo đơn mới |
| F15 | P2 | Lịch sử Cống Hiến lấy 8 mã đơn lớn nhất thay vì 8 đơn mới nhất |
| F16 | P2 | Kiểm tra nguồn của Tông Chủ mất nhật ký nhưng vẫn báo thành công |
| F17 | P2 | Bộ giới hạn kiểm video song song không thực sự giới hạn số fetch |
| F18 | P2 | Hai lần nhập/gộp catalog đồng thời có thể ghi đè mất phim vừa thêm |

P1: có thể làm sai dữ liệu kinh tế game, gỡ nhầm phim hoặc vô hiệu hóa một cơ chế bảo vệ. P2: lỗi đúng trong điều kiện nêu ở từng mục, cần xử lý theo mức sử dụng của tính năng.

## 2. Phiên bản và phạm vi kiểm

Lần đầu lấy mã ở `f2c9e129519ca07eebd90e71912b0d71097852f3`. Sau khi người dùng hỏi về độ mới, đã đối chiếu trực tiếp `main`, cập nhật lên `d82f1b8`, rồi kiểm lại trước khi chốt và cập nhật tiếp lên `dd694d3`.

GitHub xác nhận hai commit từ bản đầu đến `d82f1b8` chỉ thay README và CHANGELOG. Ba commit tiếp theo đến bản chốt thay AGENTS, CHANGELOG, README, GDD_NHAT_NIEM, TU_TIEN_BUILD và `web/vite.config.ts`. Thay đổi cấu hình duy nhất là tắt HMR khi phát triển; không thay logic nghiệp vụ của các phát hiện. Đã tải lại đủ các tệp thay đổi, đọc luật AGENTS mới, đối chiếu diff và chạy lại typecheck/build frontend trên bản chốt.

Việc lấy mã dùng kết nối GitHub, không phải một lần `git pull` thành công: lần clone Git ban đầu không xác thực được. Đã kiểm SHA blob của **457 tệp văn bản** trong bản sao so với cây Git ở commit chốt: **457 khớp, 0 lệch**.

Repo có **623 tệp**: 457 tệp văn bản, gồm mã, cấu hình, SQL, test, tài liệu và SVG; 166 tệp ảnh/video/ZIP. Với các tài nguyên nhị phân, đã đối chiếu tên tham chiếu và sự tồn tại trong cây Git; **không tuyên bố đã xem trực quan toàn bộ ảnh, video hoặc nội dung ZIP**.

Các phần được rà gồm:

- React: nguồn phim, chi tiết phim, lưu/xem tiếp, đăng nhập, Tông Môn, Luận Đạo và trang quản trị.
- Pages Functions: proxy HHAI/BLV, middleware SEO, sitemap, cache và header bảo mật.
- Worker game: phiên, tài khoản, quyền Tông Chủ, game, vật phẩm, Boss, nhiệm vụ, Thương Hội, phần backend Đạo Lữ còn giữ, Cống Hiến, thông báo và thống kê.
- Mirror: catalog, snapshot, sao lưu/khôi phục, thời lượng, quét/gỡ phim, quyền quản trị và dispatch collector.
- Collector, GitHub Actions, script deploy và migrations.

Các phát hiện bên dưới được kiểm bằng hàm thật hoặc router thật. Với lỗi đồng thời, lịch đọc/ghi được điều khiển để tái hiện đúng cửa sổ cạnh tranh; đây là kiểm thử lỗi cạnh tranh trên dữ liệu giả, không phải bằng chứng rằng đã có người khai thác Production.

## 3. Chi tiết lỗi đã xác nhận

### F01 — P1 — API Đạo Lữ còn giữ có lỗi sinh thêm Linh Thạch

**Phạm vi chính xác:** Đạo Lữ đã được gỡ khỏi giao diện ngày 30/10. Không có nhận định rằng nút/hộp Đạo Lữ hiện còn trên web. [CHANGELOG](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/CHANGELOG.md#L182-L187) ghi rõ backend và database được giữ lại.

Route [POST /api/friend/gift](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/index.ts#L2595) vẫn được đăng ký. Trong [sendFriendGift](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/friends.ts#L469), `INSERT ... DO NOTHING` và phần cộng quà cùng batch, nhưng phần cộng quà không bị ràng buộc vào việc INSERT có thắng hay không. Sau batch, lượt thua được hoàn tiền cho người gửi, trong khi người nhận đã được cộng quà.

**Đã chạy:** toàn bộ router không sửa của Worker trên Workerd, D1 cục bộ thật, hai tài khoản giả đã có quan hệ. Điều khiển để hai request đều hoàn tất lượt SELECT kiểm tra quà trước khi tiếp tục.

| Dữ liệu | Trước | Sau |
|---|---:|---:|
| Ví người gửi | 10.000 | 9.900 |
| Ví người nhận | 0 | 200 |
| Tổng hai ví | 10.000 | 10.100 |
| Số dòng quà trong lịch sử | 0 | 1 dòng, ghi 100 |

Một response `200`, một response `409 gift-sent`. Lượt bị từ chối vẫn làm người nhận được cộng tiền. `total_points` của người gửi cũng tăng do đường hoàn dùng `addStones`.

**Kiểm đọc Production:** `GET /api/friend/list` không kèm phiên trả `401 unauthorized` với thông báo Đạo Lữ, xác nhận route vẫn tồn tại. Không gọi tặng quà trên Production.

### F02 — P1 — Có thể xếp phim còn mùa sống vào nhóm mặc định gỡ

Vị trí: [mirror/src/video-scan.ts:269](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/mirror/src/video-scan.ts#L269), [điều kiện kết luận ở dòng 311](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/mirror/src/video-scan.ts#L311).

Danh sách video bị cắt còn 12 phần tử trước khi kiểm. Khi 12 phần tử đó đều hỏng, hàm trả `dead`; những mùa YouTube bị cắt bỏ không được tính là chưa kiểm.

**Đã chạy:** một phim 13 mùa; 12 mùa đầu trả các tín hiệu hỏng, mùa 13 được cấu hình trả thành công. Hàm thật trả `state: "dead", checked: 12`; không hề hỏi video mùa 13. Giao diện [mặc định tích chọn mọi dòng dead](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/admin/pages/MirrorScanDialog.tsx#L238).

**Ảnh hưởng:** chủ web có thể xác nhận gỡ cả phim dựa trên kết luận thiếu dữ liệu. Phép thử không thực hiện gỡ phim thật.

### F03 — P1 — Cửa dừng 40% không bao giờ bật trong lượt quét thông thường của UI

Vị trí: [SCAN_BATCH_SIZE = 8](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/admin/api/mirror-backup.ts#L162); [SCAN_SUSPECT_MIN = 10](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/mirror/src/video-scan.ts#L40); [điều kiện suspect](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/mirror/src/video-scan.ts#L320).

Backend chỉ xét tỷ lệ khi đã kiểm ít nhất 10 phim **trong một lô**. Frontend gửi 8 phim/lô; chạy 3 lô song song không làm số mẫu của từng request tăng lên 10. Frontend chỉ dừng theo `batch.suspect`, không tự tính lại ngưỡng trên tổng các lô.

**Đã chạy:** 8/8 phim trong một lô được kết luận `dead`, nhưng `suspect: false`.

**Ảnh hưởng:** cửa bảo vệ trước một đợt kết luận hỏng bất thường không có tác dụng với cấu hình quét đang dùng.

### F04 — P1 — Báo nguồn bất thường bị gãy sau khi khóa quyền diag

Vị trí: [worker/src/index.ts:2291](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/index.ts#L2291); [mirror/src/index.ts:814](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/mirror/src/index.ts#L814).

Worker game xác minh dấu bất thường bằng service binding gọi `/api/mirror/diag`, chỉ kèm `accept`, không kèm phiên. Mirror hiện yêu cầu phiên Tông Chủ cho đường này. Service binding không tự thay thế bước kiểm quyền do ứng dụng viết.

**Đã chạy:** nối Worker game thật và mirror thật bằng service binding trong Workerd. Gọi `/api/alerts/anomaly` với `dryRun: true`: mirror từ chối trước khi đọc dấu; game biến response không thành công thành `null`, rồi trả `409 no-anomaly`.

**Ảnh hưởng:** kể cả khi collector đã ghi dấu, đường xác minh không đọc được dấu, nên bước bật bảo trì/gửi mail qua luồng này không chạy. Collector vẫn có phần dừng ghi kho riêng; không kết luận toàn bộ cơ chế chống dữ liệu bất thường bị mất.

**Đọc Production:** diag không kèm phiên hiện trả `403`, phù hợp với cửa chặn trong mã.

### F05 — P1 — Trần Thương Hội bị vượt khi nhiều người khớp tin của cùng một chủ

Vị trí: [kiểm budget](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/market.ts#L463), [cộng budget sau giao dịch](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/market.ts#L496), [khóa chỉ danh tính đang gọi](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/service.ts#L808).

Hai người mua có hai khóa khác nhau. Cả hai có thể đọc budget cũ của cùng người bán, cùng qua kiểm tra rồi cùng tăng số tiền giao dịch. Việc giành dòng tin chỉ chống hai người mua **cùng một tin**, không bảo vệ tổng budget của nhiều tin.

**Đã chạy:** hai tin của một người bán, mỗi tin 2.000 Linh Thạch; hai người mua khác nhau cùng khớp sau khi đọc budget của người bán là 0. Cả hai thành công, `market_daily.stones` của người bán thành **4.000**, dù trần là **3.000**.

### F06 — P2 — Thư viện của tài khoản trước bị nhập vào tài khoản sau

Vị trí: [web/src/features/phim/api/library-sync.ts:167](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/phim/api/library-sync.ts#L167).

Kho favorites/watch dùng chung ở trình duyệt và được giữ sau đăng xuất. Khi B đăng nhập lần đầu trên máy, luồng đồng bộ gửi toàn bộ kho hiện tại lên B, kể cả kho vừa tải xuống từ tài khoản A.

**Đã chạy:** A nhận từ server một phim lưu và lịch sử xem `film-private-A`; A đăng xuất; B đăng nhập lần đầu. Request mang token B có cả `saved: ["film-private-A"]` và bản xem dở của A.

**Ảnh hưởng:** lẫn dữ liệu giữa tài khoản, có thể mang lịch sử xem của A lên tài khoản B. Không cần sửa localStorage thủ công để xảy ra.

### F07 — P2 — Đăng xuất giữa các tab không xóa phiên trong bộ nhớ của tab còn lại

Vị trí: [readSession:39](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/game/auth/session.ts#L39), [subscribeSession:83](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/game/auth/session.ts#L83).

`writeSession` giữ cả bản trong biến `memory`. Khi tab khác xóa localStorage, listener chỉ gọi lại người nghe, không xóa `memory`. `readSession` thấy không có giá trị lưu thì trả lại chính bản cũ trong bộ nhớ.

**Đã chạy:** ghi phiên A, mô phỏng tab khác xóa khóa phiên và phát đúng sự kiện `storage`; subscriber vẫn đọc ra A, `readSessionToken()` vẫn khác rỗng.

**Ảnh hưởng:** giao diện tiếp tục tưởng còn đăng nhập và gửi token cũ. Nếu token đã bị server xóa thì request bị từ chối; không kết luận đây là cách vượt xác thực server.

### F08 — P2 — Mật khẩu tối thiểu không đồng bộ

Vị trí: [AuthGate:95](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/game/components/AuthGate.tsx#L95), [AuthGate:116](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/game/components/AuthGate.tsx#L116), [bản dịch lỗi:214](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/game/api/request.ts#L214), [worker/src/auth.ts](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/auth.ts#L29).

Frontend cho mật khẩu 6–7 ký tự đi qua bước kiểm tra; backend yêu cầu ít nhất 8. Khi server trả `weak-password`, giao diện vẫn nói “Mật khẩu cần ít nhất 6 ký tự”. Placeholder đăng ký cũng nói 6.

**Đã chạy:** mật khẩu 7 ký tự bị hàm backend từ chối, nhưng hàm dịch lỗi trả đúng thông báo “ít nhất 6 ký tự”. Ảnh hưởng cả đăng ký và đặt lại mật khẩu.

### F09 — P2 — Thương Hội mở sớm một cảnh giới

Vị trí: [MARKET.minRealm = 1](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/market.ts#L62), [marketBlock](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/market.ts#L271), [thứ tự REALMS](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/cultivation.ts#L13).

Trong thang hiện tại, 0 là Phàm Nhân, 1 là Luyện Khí, 2 mới là Trúc Cơ. Mã, giao diện và tài liệu mô tả điều kiện Trúc Cơ, nhưng số ngưỡng là 1.

**Đã chạy:** tài khoản hơn 24 giờ, `realmIndex = 1`; `realmName(1)` là “Luyện Khí”, nhưng `marketBlock` trả chuỗi rỗng, cho giao dịch.

### F10 — P2 — Xóa tài khoản không xử lý tin Thương Hội còn mở

Vị trí: [deleteAccount](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/admin.ts#L89), [buyListing](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/market.ts#L446).

Xóa tài khoản bỏ ví, hồ sơ và túi, nhưng giữ `market_listings`. Người khác vẫn có thể khớp tin bán đó; đường mua không yêu cầu chủ tin vẫn còn tài khoản. Câu cộng tiền người bán tạo lại dòng cultivation.

**Đã chạy:** tạo tin bán 100 của A; xóa A qua hàm thật; tin vẫn còn; B mua thành công. Bảng accounts vẫn không có A, nhưng bảng cultivation được tạo lại cho A với **95 Linh Thạch**.

**Ảnh hưởng:** dữ liệu mồ côi và tin của người đã bị xóa vẫn giao dịch. Các bảng quan hệ bạn bè cũng không nằm trong danh sách dọn hiện tại; phần đó được ghi nhận bằng đọc mã, không dùng để suy ra thêm số lỗi đã tái hiện.

### F11 — P2 — Ghi nhiều bước rời nhau làm thao tác game không trọn vẹn khi có lỗi

Vị trí: [actionCraft](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/service.ts#L1196), [actionMeditate](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/game/service.ts#L1266).

Đã dùng trigger SQLite để buộc **đúng lượt ghi sau** thất bại, thay vì giả định mọi SQL đều hỏng:

| Trường hợp chạy hàm thật | Kết quả thực đo |
|---|---|
| Luyện Tu Vi Đan, có 3 Yêu Đan và 1.000 Linh Thạch; ghi vật phẩm thành phẩm thất bại | Còn 940 Linh Thạch, hết 3 Yêu Đan, không có thành phẩm; hàm báo lỗi |
| Nhận Đạo Ẩn của 10 phút, cộng ví thành công nhưng lưu game_flags thất bại; thử lại trong cùng điều kiện | Ví được cộng tổng 4 thay vì 2 Linh Thạch, mốc đã nhận vẫn chưa đổi |

**Ảnh hưởng:** lỗi DB ở giữa hành động có thể làm mất nguyên liệu/tiền hoặc cộng lặp. Khóa chống request đồng thời không thay thế transaction cho các lượt ghi trong cùng một hành động.

Đây là lỗi có điều kiện **ghi bước sau thất bại**; không nói rằng thao tác bình thường luôn làm mất đồ.

### F12 — P2 — Khoảng chờ gửi mã quên mật khẩu có cửa cạnh tranh

Vị trí: [worker/src/password-reset.ts:202](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/password-reset.ts#L202), [lưu mã:215](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/password-reset.ts#L215), [đánh dấu đã gửi:225](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/password-reset.ts#L225).

Hai lượt cùng đọc trạng thái chưa gửi trước khi lượt nào lưu/đánh dấu, nên cùng qua điều kiện 60 giây. Mỗi lượt tạo mã riêng và gửi mail riêng; bảng chỉ giữ một mã.

**Đã chạy:** hai yêu cầu cùng email và cùng thời điểm, điều khiển lượt đọc cũ; cả hai trả `sent: true`, transport giả ghi nhận **2 mail**. Không gửi email thật.

**Ảnh hưởng:** vượt khoảng chờ, làm người dùng nhận nhiều mã và có thể dùng nhầm mã đã bị thay; tốn quota mail. Không kết luận từ phép thử này rằng có thể vượt trần thử mã hoặc chiếm tài khoản.

### F13 — P2 — Gửi mail hàng loạt tự vượt timeout frontend

Vị trí: [khoảng nghỉ 250 ms](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/broadcast.ts#L60), [API mail của frontend](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/admin/api/mail.ts#L60), [timeout mặc định 12.000 ms](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/src/features/game/api/request.ts#L60).

50 địa chỉ cần ít nhất `49 × 250 = 12.250 ms` chỉ cho thời gian nghỉ, chưa tính mạng. Server chờ gửi xong mới trả response, frontend đã hủy sau 12 giây.

**Đã chạy:** nối hàm client và hàm broadcast thật, toàn bộ transport mail được chặn bằng bản giả. Client báo `GameApiError / timeout` ở **12.001 ms**; server hoàn tất **50/50** ở **12.285 ms**.

**Ảnh hưởng:** trang quản trị báo thất bại trong khi một phần hoặc toàn bộ mail đã xử lý; bấm gửi lại có thể gửi trùng. Không có email nào được gửi ra ngoài trong phép kiểm.

### F14 — P2 — Đơn pending cũ có thể khóa việc tạo đơn mới

Vị trí: [đếm pending khi tạo đơn](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/cong-hien.ts#L455), [xử lý hết hạn chỉ trong refresh](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/cong-hien.ts#L534).

Tạo đơn đếm mọi dòng `pending`, không lọc tuổi hoặc cập nhật đơn cũ. Hết hạn chỉ được xử lý khi gọi refresh cho đúng đơn; đọc state không làm việc này. Đóng hộp Cống Hiến dừng vòng refresh; lịch sử chỉ hiển thị đơn, không có nút refresh từng đơn cũ.

**Đã chạy:** 5 đơn chưa thanh toán tạo từ hai ngày trước, đều còn pending; tạo đơn mới trả **429 too-many-orders**, cả 5 vẫn pending. Không gọi payOS thật.

**Ảnh hưởng:** lời nhắc “chờ đơn cũ hết hạn” không tự giải quyết được tình trạng này nếu không có một đường cập nhật trạng thái khác.

### F15 — P2 — Lịch sử thanh toán sắp theo mã ngẫu nhiên

Vị trí: [worker/src/cong-hien.ts:418](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/src/cong-hien.ts#L418).

Mã đơn là số ngẫu nhiên 6 chữ số, nhưng state dùng `ORDER BY order_code DESC LIMIT 8`.

**Đã chạy:** 8 đơn cũ mã 900000–900007 và một đơn vừa tạo mã 100000. State chỉ trả 8 đơn cũ; đơn mới nhất biến khỏi danh sách.

**Ảnh hưởng:** lịch sử không theo thời gian, đơn mới có thể không xuất hiện sau khi đóng/mở lại hộp thoại.

### F16 — P2 — Kiểm tra nguồn trả thành công nhưng bỏ mất nhật ký

Vị trí: [proxy gọi diag:608](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/functions/lls-api/%5B%5Bpath%5D%5D.ts#L608), [nuốt lỗi diag thành mảng rỗng:628](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/web/functions/lls-api/%5B%5Bpath%5D%5D.ts#L628).

Proxy xác minh token Tông Chủ với `/api/auth/me`, nhưng không chuyển token sang lượt hỏi diag. Mirror trả 403; proxy coi như không có nhật ký và vẫn trả `ok: true` nếu bootstrap đọc được.

**Đã chạy:** database mirror có một dòng runner thật theo schema; nối proxy thật với mirror thật. Response kiểm tra nguồn là **200, ok: true, lastRuns: []**, kèm lời nhắc “Chưa có nhật ký lượt gom nào”. Đã ghi nhận lượt gọi diag không có Authorization.

F04 và F16 có chung thay đổi quyền ở diag, nhưng là hai caller độc lập và hai hành vi hỏng khác nhau.

### F17 — P2 — Pool nhận promise đã chạy nên không giới hạn concurrency

Vị trí: [mirror/src/video-scan.ts:287](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/mirror/src/video-scan.ts#L287).

`videoIsGone(...)` đã được gọi và bắt đầu fetch khi đẩy vào mảng. Đưa những promise đó vào các hàm của `pool` chỉ giới hạn việc chờ, không giới hạn lúc khởi chạy.

**Đã chạy:** 10 phim, mỗi phim 12 mùa, đo số fetch đang hoạt động đồng thời. Đỉnh là **120**, dù `PROBE_CONCURRENCY` khai **16**. Với lô UI 8 phim, cùng cấu trúc dữ liệu có thể khởi chạy 96 probe trước khi pool kiểm soát.

**Ảnh hưởng:** tải dồn lên nguồn và Worker, làm cơ chế tránh dồn request không đạt mục đích. Không dùng phép thử này để khẳng định Production đã vượt một hạn mức nền tảng cụ thể.

### F18 — P2 — Gộp catalog không bảo vệ lượt đọc–ghi đồng thời

Vị trí: [saveCatalog](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/mirror/src/backups.ts#L112).

Hàm đọc catalog cũ, gộp trong bộ nhớ rồi ghi thay snapshot, không có khóa hoặc điều kiện so phiên bản vừa đọc. Batch của `writeSnapshot` bảo vệ các chunk của một lần ghi, không bảo vệ cả chuỗi đọc–gộp–ghi.

**Đã chạy:** kho ban đầu `[old]`; hai lời gọi cùng đọc bản đó, một lời gọi thêm `new-A`, một lời gọi thêm `new-B`. Cả hai hoàn tất, nhưng kho cuối là `[old, new-B]`, mất `new-A`.

**Điều kiện:** có hai lượt ghi catalog cùng lúc, ví dụ hai lần nhập qua API quản trị. Không nói một lượt gom đơn lẻ tự làm mất phim. Kho không giảm số lượng so với bản mỗi lượt đã đọc vẫn có thể mất một id do lượt khác vừa thêm.

## 4. Cài đặt, test và migration

### M01 — Lockfile frontend không cài sạch được bằng npm ci

`npm ci --ignore-scripts --no-audit --no-fund` trong `web` thất bại với `EUSAGE`, báo thiếu `fsevents@2.3.3`, các package nền tảng của `lightningcss`, `@rolldown/binding` và một số dependency liên quan.

Đây là vấn đề đã được workflow hiện tại nhận biết: [ranking-checks.yml](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/.github/workflows/ranking-checks.yml#L34) dùng `npm install` cho web để đi tiếp. Vì vậy **không suy ra rằng pipeline đang dùng workaround chắc chắn thất bại**. Vấn đề là môi trường cài sạch theo lockfile không tái tạo được.

Để tiếp tục audit đã cài dependency với `--package-lock=false`; không sửa package.json/lockfile. Build quan sát được dùng Vite 8.3.5. Kết quả build/typecheck bên dưới không được trình bày là một lần frontend npm ci thành công.

### M02 — Có test chưa đồng bộ với hành vi hoặc fixture hiện tại

Các nhóm test được chọn để kiểm những luồng đã đọc, không chạy lệnh toàn bộ suite không chỉ định tệp.

| Nhóm | Tệp test | Tổng test | Qua | Đỏ |
|---|---:|---:|---:|---:|
| Web: API game, proxy, phim, BLV, thư viện | 6 | 157 | 157 | 0 |
| Web: admin API, duration, SEO, version, visits, favorites | 9 | 112 | 110 | 2 |
| Worker: auth, owner, alerts, Cống Hiến | 4 | 74 | 74 | 0 |
| Worker: backend Đạo Lữ, market, game, API, Luận Đạo, library | 6 | 166 | 166 | 0 |
| Worker: cultivation, balance, Bí Cảnh, monster, visits, delete account, film | 7 | 102 | 98 | 4 |
| Mirror: video scan, durations, backup | 3 | 36 | 34 | 2 |
| Mirror: dispatch, handshake, mirror, scheduled | 4 | 42 | 40 | 2 |
| **Tổng các lượt kiểm đã ghi nhận** | **39** | **689** | **679** | **10** |

Phân loại 10 test đỏ:

- `web/src/features/admin/api/visits.test.ts`: 2 test thiếu trường `conn` trong expected object, trong khi parser hiện trả trường đó.
- `worker/test/bican.test.ts`: 4 test dùng tài khoản thường và chờ mở Bí Cảnh; mã hiện chủ động khóa Bí Cảnh cho tài khoản thường. **Không coi việc khóa này là lỗi sản phẩm.**
- `mirror/test/scheduled.test.ts`: 2 test hỏi diag không kèm phiên, còn expected theo hợp đồng công khai cũ.
- `mirror/test/backup.test.ts`: 1 test expected câu “request không kèm vé Tông Chủ” nhưng mã hiện nói “request không kèm phiên Tông Môn”; 1 test còn dòng mục lục backup của ca trước. `mirror/test/helpers.ts` xóa chunks/meta nhưng không xóa `mirror_backups`, nên fixture có thể phụ thuộc thời điểm/id sao lưu giữa các ca.

**Ý nghĩa:** các test hiện có chưa bao phủ đủ các lịch xen kẽ và các caller liên dịch vụ đã nêu. Nhiều test nghiệp vụ qua không bác bỏ các lỗi cạnh tranh mới tái hiện.

### M03 — Migration 0016 có thể cộng bù hai lần sau lượt deploy bị ngắt

Vị trí: [worker/migrations/0016_bon_bac.sql](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/migrations/0016_bon_bac.sql#L34), [script chạy từng statement và đánh dấu cuối tệp](https://github.com/Winnyzzzz/phimtonghop-copy/blob/dd694d3bdfc49d979146b8df13d7db4589cc710a/worker/scripts/deploy.mjs#L177).

**Đã chạy SQL thật**, được tách bằng chính hàm `splitStatements` của script deploy:

1. Dòng cũ có realm 2, tier 2, 1.000 Linh Thạch.
2. Chạy statement cộng bù đầu tiên: thành 1.125, tier còn 2.
3. Dừng trước các statement sau và trước dấu hoàn tất migration.
4. Chạy lại cả migration: thành **1.250**, tier đổi về 1.

Một lần bù phải cho 1.125; chạy lại trong trạng thái áp dở cộng thêm lần nữa.

**Phạm vi:** chỉ khi migration này chưa được đánh dấu hoàn tất và bị ngắt giữa những bước trên. Không nói database Production hiện đang bị cộng bù lặp; không chạy migration lên Production.

## 5. Kiểm tra đã qua và các giới hạn thực tế

| Kiểm tra | Kết quả |
|---|---|
| Web `npx tsc -b --noEmit` | Qua |
| Worker `npm run check` | Qua |
| Mirror `npm run check` | Qua |
| `npm ci` Worker và mirror | Qua |
| Build frontend bằng Vite, output vào thư mục kiểm riêng | Qua, 1.994 module được biến đổi |
| Kiểm cú pháp 9 script `.mjs` của collector/deploy/web | Qua |
| SHA blob của 457 tệp văn bản so với commit chốt | 457 khớp, 0 lệch |
| Tham chiếu asset dạng đường dẫn cố định | Không thấy thiếu tệp thật; hai kết quả regex còn lại nằm trong comment mẫu/glob |
| GET trang chủ Production | HTTP 200 |
| GET health Worker game | HTTP 200 |
| GET health mirror | HTTP 200 |
| GET diag không kèm phiên | HTTP 403 đúng cửa khóa hiện tại |
| GET friend/list không kèm phiên | HTTP 401, endpoint còn tồn tại |

Đã kiểm tra giả thuyết PBKDF2 600.000 vòng có thể không được runtime hỗ trợ: **hàm hash và verify chạy được trên Workerd**, nên không báo nó là lỗi. Đã đối chiếu GitHub: tag `actions/checkout@v7` và `actions/setup-node@v7` tồn tại; không báo workflow hỏng vì tên tag.

**Browser test/UI trực quan chưa chạy được:** không có Chromium sẵn; cài Playwright Chromium thất bại do nội dung tải về không phải ZIP hợp lệ. Vì vậy báo cáo không khẳng định đã kiểm mọi khung hình mobile, thao tác DOM hoặc mọi player nhúng trong trình duyệt.

**Không chạy collector thật:** collector có đường ghi thẳng D1 và có thể tự gỡ phim. Chỉ kiểm mã, cú pháp, workflow, SQL và những thành phần được cô lập an toàn. Không bấm Gom ngay, không khôi phục/xóa backup, không gửi webhook thanh toán thật.

Các endpoint health trả 200 chỉ chứng minh đường health đang trả lời; không dùng nó để suy ra mọi chức năng Production đều đúng hoặc Worker đang phục vụ chắc chắn đúng một Git SHA, vì response health không công bố SHA đó.

## 6. Quan sát bổ sung — không cộng thành lỗi đã khai thác

### Dependency

`npm audit --package-lock-only --omit=dev --json` trên lockfile web trả 8 nhóm package cảnh báo: 4 high, 4 moderate; không có critical trong kết quả đó.

Các tên là `@remix-run/router`, `react-router`, `react-router-dom`, `nanoid`, `picomatch`, `postcss`, `postcss-selector-parser`, `source-map-js`. Có package nằm trong chuỗi công cụ build hoặc nhiều bản lồng nhau; mức npm gán cho package không đồng nghĩa website có đường khai thác tương ứng.

**Chưa xác minh reachability của từng advisory trong ứng dụng này, không gọi đây là 8 lỗ hổng Production đã xác nhận.** Không chạy `npm audit fix` và không nâng dependency.

### Tải hỏi thông báo

`NOTICE_REFRESH_MS` hiện là 10 giây; endpoint đọc thông báo không có cache ở tầng handler này, mỗi lượt đọc một dòng settings.

Kịch bản giả định: `30 phút × 60 / 10 = 180 lượt/người`; 500 người cùng dùng tổng cộng 30 phút/ngày tạo khoảng **90.000 request/ngày chỉ cho polling thông báo**, chưa tính mở đầu, CORS và các API khác. Đây là phép tính từ nhịp trong mã, **không phải lưu lượng Production đã đo**. Tab ẩn được dừng hỏi theo cấu hình React Query.

### Payload frontend

Trong lần build kiểm tra: bundle chính khoảng **1.001,77 kB**, gzip **279,04 kB**; HLS được tách riêng, gzip khoảng 180,38 kB. Vite phát cảnh báo chunk lớn. Đây là quan sát dung lượng, chưa có đo LCP/INP trên thiết bị người dùng trong đợt audit này.

### Tài liệu mới có mô tả hash chưa khớp mã

CHANGELOG 31/10 nói hash `sha256$…` cũ tự được nâng sau đăng nhập. Mã `verifyPassword` hiện nhận định dạng `pbkdf2$…`, và `handleLogin` không gọi cập nhật password hash. Lịch sử commit auth được kiểm cũng mô tả đổi PBKDF2 từ 100.000 lên 600.000 vòng. Vì vậy câu ghi trong changelog cần được đối chiếu lại; **không suy ra mọi tài khoản cũ bị mất khả năng đăng nhập** — hash PBKDF2 cũ vẫn được verify theo số vòng lưu trong chuỗi.

## 7. Thứ tự nên xử lý khi có yêu cầu sửa riêng

1. F01, F05: các đường làm sai tiền và hạn mức game; lưu ý F01 nằm ở backend của tính năng đã gỡ giao diện.
2. F02, F03: tránh để kết luận quét dẫn tới chọn gỡ nhầm phim.
3. F04, F16: đồng bộ quyền của caller với diag để khôi phục khả năng báo bất thường và đọc trạng thái.
4. F06, F07, F08: dữ liệu theo tài khoản và trải nghiệm đăng nhập.
5. F10, F11, F12–F15, F17–F18: dọn dữ liệu liên quan, transaction, email, Cống Hiến và các lượt ghi đồng thời.
6. Lockfile/test/migration và các quan sát hiệu năng/dependency.

**Đợt này chỉ rà soát và báo cáo. Chưa có bản vá nào được áp dụng.**
