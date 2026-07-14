# PHẦN 1: PHÂN TÍCH VÀ ĐỀ XUẤT ĐA GIẢI PHÁP

## 6.1. Phân tích đầu vào và đầu ra

- **Dữ liệu nào phải được kiểm tra đầu tiên?**
  Kiểm tra sự tồn tại của Course (Khóa học). Nếu khóa học không tồn tại trong hệ thống, cần phải ném ra lỗi 404. Nếu khóa học có tồn tại, tiếp tục xử lý việc lấy danh sách.

- **Điều kiện nào dùng để lọc Enrollment?**
  Lọc Enrollment (Đăng ký) có trạng thái là `STUDYING` hoặc `COMPLETED`. Loại bỏ các đăng ký có trạng thái `CANCELLED`.

- **Điều kiện nào dùng để lọc Student?**
  Chỉ lấy những Student (Sinh viên) có trạng thái là `ACTIVE`. Loại bỏ `INACTIVE`.

- **Làm thế nào để loại bỏ sinh viên trùng?**
  Vì một sinh viên có thể có nhiều `Enrollment` cho cùng một `Course` (dù hiếm nhưng theo thiết kế, ta cần cẩn thận), ta có thể sử dụng `DISTINCT` trong SQL (khi dùng JOIN) hoặc dùng kiểu dữ liệu kiểu `Set` (hoặc kiểm tra mảng id đã xử lý trong code) để đảm bảo sinh viên chỉ xuất hiện một lần trong kết quả.
  
- **Trường hợp nào trả về danh sách rỗng?**
  Trường hợp khóa học tồn tại (qua vòng kiểm tra 404 ban đầu) nhưng không có sinh viên nào đăng ký thỏa mãn điều kiện lọc (chưa có ai đăng ký, hoặc tất cả đều bị `CANCELLED`, hoặc tất cả sinh viên đăng ký đều `INACTIVE`).

## 6.2. Đề xuất tối thiểu hai giải pháp

- **Giải pháp 1: Truy vấn Enrollment rồi dùng vòng lặp**
  - **B1**: Lấy chi tiết Course. Nếu không có, ném 404.
  - **B2**: Truy vấn tất cả `Enrollment` có `course_id` tương ứng và `status IN ('STUDYING', 'COMPLETED')`.
  - **B3**: Tạo một vòng lặp duyệt qua các Enrollment, trích xuất `student_id`.
  - **B4**: Truy vấn `Student` cho từng `student_id`, kiểm tra `status == 'ACTIVE'` và thêm vào danh sách (đảm bảo không trùng bằng cách kiểm tra ID). Sắp xếp danh sách ở cấp độ code (Python list.sort()).

- **Giải pháp 2: Sử dụng JOIN giữa Student và Enrollment**
  - **B1**: Lấy chi tiết Course. Nếu không có, ném 404.
  - **B2**: Dùng SQLAlchemy để tạo một query sử dụng JOIN giữa bảng `Student` và `Enrollment` trên điều kiện `Student.id == Enrollment.student_id`.
  - **B3**: Thêm các filter `Enrollment.course_id == id_khoa_hoc`, `Enrollment.status.in_(['STUDYING', 'COMPLETED'])`, `Student.status == 'ACTIVE'`.
  - **B4**: Sử dụng `distinct()` và `order_by(Student.full_name)` ngay trong câu lệnh SQL. Trả về kết quả một lần duy nhất.

---

# PHẦN 2: SO SÁNH VÀ LỰA CHỌN

## 6.3. Lập bảng so sánh

| Tiêu chí | Giải pháp dùng vòng lặp | Giải pháp dùng JOIN |
| --- | --- | --- |
| **Độ dễ hiểu** | Dễ hiểu cho người mới tiếp cận lập trình vì logic tuần tự rõ ràng. | Cần kiến thức về SQL JOIN và cách thiết kế query của ORM, có thể khó với người mới. |
| **Số câu truy vấn** | N + 2 (1 query lấy Course, 1 query lấy Enrollment, N query lấy từng Student tương ứng). Gây ra bài toán N+1 query. | 2 câu truy vấn (1 query kiểm tra Course, 1 query lấy tất cả Student bằng JOIN). |
| **Tốc độ khi dữ liệu nhỏ** | Khá nhanh vì số lượng bản ghi thấp, chênh lệch không đáng kể. | Rất nhanh. |
| **Tốc độ khi dữ liệu lớn** | Rất chậm vì gọi N query liên tục tới cơ sở dữ liệu (Database Overhead). Tốn thời gian tạo I/O kết nối mạng. | Rất nhanh và tối ưu, RDBMS tự động thực hiện thuật toán join hiệu quả bằng Index. |
| **Bộ nhớ sử dụng** | Tốn nhiều RAM ở cấp độ ứng dụng (Application level) để chứa dữ liệu tạm và thực hiện vòng lặp/lọc/sắp xếp. | Tối ưu vì đẩy tác vụ lọc, loại bỏ trùng, sắp xếp xuống Database Engine. |
| **Khả năng bảo trì** | Logic phân mảnh (vừa DB vừa Code), dài dòng, dễ sinh lỗi khi thêm tính năng. | Ngắn gọn, chuẩn hóa theo API của ORM, dễ quản lý. |
| **Khả năng mở rộng** | Khó mở rộng, khi lượng sinh viên lên đến 1,000, 10,000 thì API sẽ chết (Timeout). | Dễ dàng mở rộng. Có thể dễ dàng thiết lập Pagination kết hợp Index của CSDL. |

- **Giải pháp nào dễ hiểu hơn với người mới?**: Giải pháp dùng vòng lặp.
- **Giải pháp nào tạo nhiều câu truy vấn hơn?**: Giải pháp dùng vòng lặp (gây lỗi N+1 query).
- **Khi có 1.000 sinh viên, giải pháp nào phù hợp hơn?**: Giải pháp dùng JOIN. Vòng lặp sẽ tạo ra 1,000 câu query tới Database gây thắt cổ chai.
- **Giải pháp nào dễ thêm điều kiện lọc?**: Giải pháp dùng JOIN (chỉ việc `.where(...)` bằng SQLAlchemy).
- **Giải pháp nào có nguy cơ gây chậm API?**: Giải pháp dùng vòng lặp do chi phí kết nối mạng mỗi lần query.

## 6.4. Lựa chọn giải pháp

- **Giải pháp được chọn**: **Giải pháp dùng JOIN**
- **Lý do lựa chọn**:
  Trong thực tế, một khóa học có thể có từ vài trăm đến hàng ngàn học viên. Nếu dùng vòng lặp, hiện tượng "N+1 query" sẽ gây quá tải Database Server, tắc nghẽn đường truyền mạng và khiến API Timeout. Sử dụng `JOIN` giúp tận dụng sức mạnh xử lý của hệ quản trị CSDL, xử lý logic (Lọc, Sort, Distinct) tối ưu bằng Index. Code cũng sẽ ngắn gọn và dễ bảo trì.
- **Bối cảnh mà giải pháp còn lại phù hợp**:
  Giải pháp dùng vòng lặp chỉ phù hợp khi chúng ta cần truy vấn lấy dữ liệu từ hai Database riêng biệt hoàn toàn (không liên kết với nhau được) hoặc gọi từ các Third-party API khác nhau không hỗ trợ filter nội bộ.
- **Sự đánh đổi**: Đòi hỏi kỹ năng tối ưu truy vấn SQL (ORM Query) thay vì chỉ dùng logic Python đơn thuần.

---

# PHẦN 3: THIẾT KẾ VÀ TRIỂN KHAI

## 6.5. Thiết kế các bước thực hiện (Lưu đồ logic)

1. `Nhận Request`: `GET /courses/{course_id}/students`
2. `Query`: Lấy `Course` theo `course_id`.
   - `Nếu (Course không tồn tại)` -> Trả về lỗi `404 Not Found`.
   - `Nếu (Course tồn tại)` -> Tiếp tục Bước 3.
3. `Query (JOIN)`: Tìm các `Student` join với `Enrollment`.
   - Điều kiện 1: `Enrollment.course_id == course_id`
   - Điều kiện 2: `Enrollment.status IN ('STUDYING', 'COMPLETED')`
   - Điều kiện 3: `Student.status == 'ACTIVE'`
   - Xử lý trùng lắp: Dùng `DISTINCT(Student.id)`
   - Sắp xếp: Tăng dần theo `Student.full_name`
4. `Đếm`: Lấy số lượng sinh viên trong danh sách.
5. `Response`: Trả về chuẩn JSON cấu trúc với thông tin `course_id`, `course_name`, `total_students`, danh sách `students` (nếu rỗng thì trả về mảng rỗng `[]`).
