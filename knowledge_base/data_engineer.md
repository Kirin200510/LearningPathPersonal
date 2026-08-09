---
id: "career-data-engineer"
title: "Kỹ sư dữ liệu"
document_type: "career_guidance"
role_group: "data_engineering"
language: "vi"
audience: "sinh viên ngành công nghệ thông tin"
level: "beginner_to_intermediate"
updated_at: "2026-08-05"
aliases:
  - "Data Engineer"
  - "Data Warehouse Engineer"
  - "Analytics Engineer"
source_urls:
  - "https://www.onetonline.org/link/summary/15-1243.00"
  - "https://www.onetonline.org/link/summary/15-1243.01"
  - "https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/"
  - "https://spark.apache.org/docs/latest/index.html"
---

# Kỹ sư dữ liệu


> Tài liệu này dùng để định hướng học tập và xây dựng lộ trình cá nhân hóa. 
> Nó không phải cam kết về tuyển dụng, mức lương hoặc thời gian chắc chắn để có việc.


## Nghề này làm gì?

Data Engineer xây dựng hệ thống thu thập, biến đổi, lưu trữ và cung cấp dữ liệu cho phân tích, báo cáo hoặc machine learning. Mục tiêu là dữ liệu đúng, có thể truy vết, chạy ổn định và phục vụ được nhu cầu sử dụng.

## Công việc thường gặp

- Thiết kế pipeline ingest và biến đổi dữ liệu.
- Mô hình hóa dữ liệu trong warehouse hoặc lakehouse.
- Kiểm tra chất lượng và xử lý lỗi dữ liệu.
- Lập lịch workflow và giám sát job.
- Tối ưu truy vấn, lưu trữ và chi phí xử lý.
- Phối hợp với analyst, data scientist và backend.

## Phù hợp với ai?

Phù hợp với người thích backend, database, hệ thống và độ tin cậy. Nghề này thường ít tập trung vào giao diện, nhưng yêu cầu tư duy kỹ về luồng dữ liệu và vận hành.

## Nền tảng cần có

1. Python.
2. SQL vững.
3. Mô hình dữ liệu quan hệ.
4. Linux, Git và Docker.
5. Kiến thức cơ bản về API, file format và networking.
6. Kiểm thử và quan sát pipeline.

## Lộ trình học đề xuất

### Giai đoạn 1: Python và SQL

Viết script đọc API, CSV, JSON và database. SQL cần bao gồm join, CTE, window function, index và transaction ở mức sử dụng.

### Giai đoạn 2: Mô hình dữ liệu

Học chuẩn hóa cho hệ thống giao dịch và star schema cho phân tích. Hiểu fact, dimension, grain và lịch sử thay đổi dữ liệu.

### Giai đoạn 3: ETL/ELT

Xây pipeline extract, transform, load có idempotency, retry, logging và kiểm tra chất lượng.

### Giai đoạn 4: Orchestration

Dùng Airflow hoặc công cụ tương đương để mô tả DAG, dependency, schedule và retry. Không dùng orchestration để thay thế logic xử lý dữ liệu.

### Giai đoạn 5: Xử lý dữ liệu lớn

Học Spark khi dữ liệu hoặc khối lượng tính toán thực sự cần phân tán. Hiểu partition, shuffle và cách tránh xử lý dư thừa.

### Giai đoạn 6: Vận hành

Container hóa pipeline, quản lý secret, cảnh báo lỗi, backfill, lineage và tài liệu schema.

## Dự án portfolio nên làm

1. Pipeline lấy dữ liệu từ API, làm sạch và nạp vào warehouse.
2. Kho dữ liệu theo dõi học tập với fact tiến độ và dimension sinh viên, khóa học.
3. Workflow Airflow có retry, kiểm tra chất lượng và dashboard kết quả.

## Tiêu chí tự đánh giá

Bạn có thể xây pipeline chạy lặp lại mà không tạo dữ liệu trùng, giải thích mô hình dữ liệu, xử lý lỗi và theo dõi nguồn gốc dữ liệu.

## Sai lầm thường gặp

- Học công cụ big data trước khi vững SQL.
- Dùng Spark cho dữ liệu nhỏ chỉ vì công nghệ phổ biến.
- Pipeline không idempotent và không có kiểm tra chất lượng.
- Không ghi nhận schema, thời gian cập nhật và nguồn dữ liệu.
- Chỉ chạy thành công một lần nhưng không vận hành được lâu dài.

## Nghề liên quan

Database Engineer, Analytics Engineer, Backend Developer, Data Analyst và Machine Learning Engineer.

## Nguồn tham khảo

- O*NET OnLine — Database Architects: https://www.onetonline.org/link/summary/15-1243.00
- O*NET OnLine — Data Warehousing Specialists: https://www.onetonline.org/link/summary/15-1243.01
- Apache Airflow — Core Concepts: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/
- Apache Spark — Documentation: https://spark.apache.org/docs/latest/index.html
