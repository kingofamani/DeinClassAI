# 🚀 DeinClassAI 快速開始指南

## 📋 系統需求

- Docker Desktop (Windows/Mac) 或 Docker Engine (Linux)
- docker-compose
- 8GB+ 記憶體
- 5GB+ 可用磁碟空間

## ⚡ 快速啟動

### Windows 用戶
```powershell
# 1. 建立環境變數檔案
Copy-Item .env.litellm.example .env.litellm

# 2. 編輯環境變數 (使用記事本或 VS Code)
notepad .env.litellm

# 3. 啟動系統
.\start.ps1
```

### macOS/Linux 用戶
```bash
# 1. 建立環境變數檔案
cp .env.litellm.example .env.litellm

# 2. 編輯環境變數
nano .env.litellm
# 或使用其他編輯器: code .env.litellm

# 3. 設定執行權限並啟動
chmod +x start.sh
./start.sh
```

### 手動啟動 (所有平台)
```bash
# 建立並啟動所有服務
docker-compose up -d

# 查看服務狀態
docker-compose ps

# 查看日誌
docker-compose logs -f
```

## 🔧 必要設定

### 1. 環境變數設定

編輯 `.env.litellm` 檔案，設定以下重要變數：

```env
# OpenAI API 設定 (必填)
OPENAI_API_KEY=sk-your-openai-api-key-here

# LiteLLM 管理金鑰 (必填)
LITELLM_MASTER_KEY=your-secure-master-key-here

# UI 登入憑證 (必填)
UI_USERNAME=admin
UI_PASSWORD=your-admin-password-here

# 資料庫連線 (已預設，通常不需修改)
DATABASE_URL=postgresql://litellm_user:litellm_password@postgres:5432/litellm

# 鹽值金鑰 (設定後勿更改)
LITELLM_SALT_KEY=your-unique-salt-key-here
```

### 2. OpenAI API 金鑰取得

1. 前往 [OpenAI Platform](https://platform.openai.com/)
2. 註冊或登入帳號
3. 前往 API Keys 頁面
4. 建立新的 API 金鑰
5. 複製金鑰並貼到 `.env.litellm` 檔案中

## 🌐 服務網址

啟動成功後，可以存取以下服務：

| 服務 | 網址 | 說明 |
|------|------|------|
| 🧑‍🏫 教師管理面板 | http://localhost:5000 | 建立學生通行證、管理預算 |
| 🎓 學生 AI 教室 | http://localhost:8080 | 學生使用的 AI 對話介面 |
| ⚙️ LiteLLM 管理 | http://localhost:4000 | 系統管理和監控 |

## 📱 使用流程

### 教師操作流程

1. **開啟教師管理面板**: http://localhost:5000
2. **建立學生通行證**:
   - 輸入學生姓名
   - 選擇權限套餐 (基礎班/進階班/專業班)
   - 點擊「生成通行證」
3. **分享給學生**:
   - 讓學生掃描 QR Code
   - 或複製金鑰直接分享

### 學生設定流程

1. **掃描 QR Code** 或開啟老師提供的連結
2. **複製專屬金鑰** (點擊複製按鈕)
3. **進入 AI 教室** (點擊「進入 AI 教室」按鈕)
4. **登入設定**:
   - 使用 Google 帳號登入
   - 點擊右上角設定圖示 ⚙️
   - 貼上剛才複製的金鑰
   - 設定 API Base URL: `http://localhost:4000`
   - 點擊儲存
5. **開始學習** 🎉

## 🛠️ 常見問題

### Q: 服務啟動失敗怎麼辦？

1. **檢查 Docker 是否運行**:
   ```bash
   docker --version
   docker-compose --version
   ```

2. **檢查連接埠是否被佔用**:
   ```bash
   # Windows
   netstat -an | findstr "5000\|8080\|4000\|5432"
   
   # macOS/Linux
   lsof -i :5000 -i :8080 -i :4000 -i :5432
   ```

3. **查看詳細錯誤日誌**:
   ```bash
   docker-compose logs [服務名稱]
   ```

### Q: 學生無法存取 AI 教室？

1. **確認服務運行狀態**:
   ```bash
   docker-compose ps
   ```

2. **檢查防火牆設定** (允許 8080 連接埠)

3. **確認 API 金鑰設定正確**

### Q: 教師面板無法建立金鑰？

1. **檢查 OpenAI API 金鑰是否有效**
2. **確認 LiteLLM 服務正常運行**
3. **檢查 `.env.litellm` 設定**

### Q: 如何重置系統？

```bash
# 停止所有服務
docker-compose down

# 清除資料庫資料 (注意：會刪除所有學生金鑰)
docker-compose down -v

# 重新啟動
docker-compose up -d
```

## 🔒 安全建議

1. **定期更換 API 金鑰**
2. **設定強密碼** (UI_PASSWORD)
3. **限制網路存取** (生產環境)
4. **定期備份資料庫**
5. **監控使用量和費用**

## 📞 支援

如遇到問題，請：

1. 查看本指南的常見問題
2. 檢查 GitHub Issues
3. 查看服務日誌找出錯誤原因
4. 聯繫技術支援

---

**🎉 祝您使用愉快！讓 AI 為教育帶來更多可能性！** 