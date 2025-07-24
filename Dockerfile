# Sử dụng image Python 3.9 (phiên bản nhẹ)
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép tệp requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các thư viện cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào thư mục làm việc
COPY . .

# Chỉ định lệnh chạy mặc định (chạy crawler.py từ thư mục /app)
CMD ["python", "app/crawler.py"]