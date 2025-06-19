FROM python:3.11-slim

# 安裝系統依賴（若需要可自行擴充）
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# 建立工作目錄
WORKDIR /app

# 複製並安裝依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式原始碼
COPY . .

# 預設環境變數
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# 啟動 Flask
CMD ["python", "app.py"]
