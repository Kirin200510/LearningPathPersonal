---
id: "career-backend-developer"
title: "Lập trình viên Backend"
document_type: "career_guidance"
role_group: "web_development"
language: "vi"
audience: "sinh viên ngành công nghệ thông tin"
level: "beginner_to_intermediate"
updated_at: "2026-08-05"
aliases:
  - "Backend Developer"
  - "Server-side Developer"
  - "API Developer"
source_urls:
  - "https://www.onetonline.org/link/summary/15-1254.00"
  - "https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works"
  - "https://fastapi.tiangolo.com/tutorial/"
  - "https://owasp.org/www-project-top-ten/"
---

# Lập trình viên Backend


> Tài liệu này dùng để định hướng học tập và xây dựng lộ trình cá nhân hóa. 
> Nó không phải cam kết về tuyển dụng, mức lương hoặc thời gian chắc chắn để có việc.


## Nghề này làm gì?

Backend Developer xây dựng phần xử lý phía máy chủ của ứng dụng. Backend tiếp nhận yêu cầu từ client, kiểm tra dữ liệu, thực thi nghiệp vụ, đọc ghi cơ sở dữ liệu, xác thực người dùng và trả kết quả qua API. Một backend tốt cần đúng chức năng, an toàn, dễ bảo trì, có khả năng quan sát lỗi và đáp ứng được tải phù hợp.

## Công việc thường gặp

- Thiết kế và phát triển REST API.
- Viết logic nghiệp vụ và validation.
- Thiết kế bảng, quan hệ và truy vấn database.
- Xây dựng đăng nhập, phân quyền và quản lý phiên hoặc token.
- Xử lý lỗi, logging, caching và tác vụ nền.
- Viết unit test, integration test và tài liệu API.
- Đóng gói, triển khai và theo dõi dịch vụ.

## Phù hợp với ai?

Hướng này phù hợp với người thích logic, dữ liệu, kiến trúc hệ thống và các vấn đề không nhất thiết nhìn thấy trực tiếp trên giao diện. Người học cần kiên nhẫn khi debug request, database, xác thực và cấu hình môi trường.

## Nền tảng cần có

1. Một ngôn ngữ backend, với dự án hiện tại nên ưu tiên Python.
2. HTTP, request, response, status code, header và JSON.
3. SQL, khóa chính, khóa ngoại, index và transaction.
4. Git, terminal và quản lý môi trường.
5. Cấu trúc dữ liệu, OOP và xử lý lỗi.
6. Kiến thức bảo mật web căn bản.

## Lộ trình học đề xuất

### Giai đoạn 1: Python nền tảng

Học cú pháp, hàm, module, class, exception, typing và virtual environment. Viết các chương trình xử lý dữ liệu nhỏ trước khi học framework.

### Giai đoạn 2: Web và HTTP

Hiểu client-server, DNS ở mức tổng quan, URL, phương thức HTTP, status code, cookie, header, CORS và JSON. Thực hành gọi API bằng Postman hoặc công cụ tương đương.

### Giai đoạn 3: FastAPI căn bản

Tạo route, path parameter, query parameter, request body, schema Pydantic, dependency và xử lý lỗi. Dùng Swagger để thử API.

### Giai đoạn 4: Database

Học SQL và mô hình dữ liệu trước, sau đó dùng SQLAlchemy. Thực hành CRUD, relationship, migration, transaction, eager loading và pagination.

### Giai đoạn 5: Authentication và security

Học hash mật khẩu, access token, refresh token, role, permission và nguyên tắc không tin dữ liệu đầu vào. Tham khảo OWASP Top 10 để nhận diện nhóm rủi ro web phổ biến.

### Giai đoạn 6: Chất lượng và triển khai

Viết test, logging, cấu hình bằng biến môi trường, Docker hóa ứng dụng và triển khai một bản chạy được. Sau đó mới học caching, message queue, background worker và kiến trúc phân tán.

## Dự án portfolio nên làm

1. API quản lý lộ trình học có người dùng, khóa học và tiến độ.
2. Hệ thống thương mại nhỏ có giỏ hàng, đơn hàng và phân quyền.
3. API đặt lịch có kiểm tra xung đột thời gian, gửi thông báo và test.

## Tiêu chí tự đánh giá

Bạn nên có khả năng thiết kế schema, giải thích quan hệ bảng, xây API có xác thực, trả lỗi hợp lý, viết test cho luồng chính và triển khai được ứng dụng. Bạn cũng cần giải thích vì sao chọn một giải pháp thay vì chỉ mô tả code.

## Sai lầm thường gặp

- Học framework trước khi hiểu HTTP và SQL.
- Lưu mật khẩu hoặc secret trực tiếp trong source code.
- Để LLM tự tạo toàn bộ code nhưng không kiểm tra luồng nghiệp vụ.
- Không kiểm soát quyền truy cập tài nguyên theo người dùng.
- Tối ưu hiệu năng quá sớm khi chức năng và test chưa ổn định.

## Nghề liên quan

Software Engineer, API Developer, Platform Engineer, DevOps Engineer, Data Engineer và Security Engineer.

## Nguồn tham khảo

- O*NET OnLine — Web Developers: https://www.onetonline.org/link/summary/15-1254.00
- MDN — How the web works: https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works
- FastAPI — Tutorial: https://fastapi.tiangolo.com/tutorial/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
