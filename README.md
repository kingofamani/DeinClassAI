# DeinClassAI - AI 教室管理系統

一個為教育場景設計的 AI 服務教師管理面板，旨在提供安全、可控、易用的 LLM 訪問權限管理方案。

## 🎯 專案目標

本專案解決了教師在課堂中引入 AI 工具時面臨的核心挑戰：如何有效管理學生的使用權限，控制成本，並確保 AI 的使用符合教學目標。透過本系統，教師可以：

- **一鍵生成學生通行證**: 為每個學生創建帶有預設權限套餐的 API 金鑰
- **精準控制資源**: 限制學生可用的 AI 模型、每月花費上限，以及可使用的時間段
- **簡化學生 onboarding**: 利用 QR Code，讓低年級學生也能輕鬆完成設定
- **整合現有身份系統**: 學生端使用 Google 教育帳號登入，無需記憶新密碼
- **即時監控與分析**: 透過 PostgreSQL 資料庫提供詳細的使用統計和成本分析

## 🏗️ 技術架構

本專案採用微服務架構，由以下幾個獨立但協同工作的服務組成：

### 核心服務

- **🎓 Teacher Panel (`flask_app`)**: 基於 Python Flask 的教師管理後台
- **🔐 Permission Core (`litellm`)**: LiteLLM 服務，是整個系統的權限控制中樞
- **🗄️ Database (`postgres`)**: PostgreSQL 資料庫，儲存金鑰、預算、使用記錄
- **💬 Student UI (`open_webui`)**: Open WebUI 服務，供學生使用的聊天界面

### 關鍵特性

- **🔒 安全隔離**: 學生只能取得虛擬金鑰，真實 OpenAI Key 完全隔離
- **📊 即時監控**: PostgreSQL 提供高效能的即時使用量追蹤
- **⏰ 時段控制**: 自訂回調函數實現上課時間限制
- **💰 預算管理**: 精確的成本控制和預算追蹤
- **🐳 容器化部署**: 使用 Docker Compose 進行完整的服務編排

## 🚀 快速開始

### 前置需求

- Docker & Docker Compose
- OpenAI API 金鑰
- Google OAuth 2.0 憑證（用於學生登入）

### 1. 複製專案

```bash
git clone <repository-url>
cd DeinClassAI
```

### 2. 環境變數設定

複製環境變數範本：

```bash
cp .env.example .env
cp .env.litellm.example .env.litellm
```

編輯 `.env` 檔案：

```bash
# 主要環境變數
OPENAI_API_KEY=sk-your-openai-api-key-here
LITELLM_ADMIN_KEY=admin-your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

編輯 `.env.litellm` 檔案：

```bash
# LiteLLM 專用環境變數
OPENAI_API_KEY=sk-your-openai-api-key-here
LITELLM_ADMIN_KEY=admin-your-secret-key-here
LITELLM_MASTER_KEY=admin-your-secret-key-here
UI_USERNAME=admin
UI_PASSWORD=admin-your-secret-key-here
LITELLM_SALT_KEY=sk-salt-your-random-string-here
DATABASE_URL=postgresql://litellm_user:litellm_password@postgres:5432/litellm
PORT=4000
STORE_MODEL_IN_DB=True
```

### 3. 啟動服務

```bash
# 啟動所有核心服務
docker-compose up -d

# 啟動包含教師面板的完整服務
docker-compose --profile full up -d
```

### 4. 存取服務

- **LiteLLM 管理介面**: http://localhost:4000/ui/
- **教師管理面板**: http://localhost:5000 (需要 `--profile full`)
- **學生 AI 教室**: http://localhost:8080
- **PostgreSQL**: localhost:5432 (可選)

## 📋 服務說明

### LiteLLM 權限核心 (Port 4000)

- **功能**: API 代理、虛擬金鑰管理、權限控制
- **登入**: 使用者名稱 `admin`，密碼為您的 `LITELLM_ADMIN_KEY`
- **資料庫**: 連接到 PostgreSQL 進行資料持久化

### Flask 教師管理面板 (Port 5000)

- **功能**: 生成學生通行證、管理權限套餐、監控使用狀況
- **啟動**: 需要使用 `--profile full` 參數

### Open WebUI 學生前端 (Port 8080)

- **功能**: 學生聊天介面、Google 登入、API 金鑰設定
- **認證**: 整合 Google OAuth 2.0

### PostgreSQL 資料庫 (Port 5432)

- **功能**: 儲存虛擬金鑰、使用記錄、預算管理
- **憑證**: `litellm_user` / `litellm_password`

## 🔧 進階設定

### Google OAuth 設定

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用 Google+ API
4. 建立 OAuth 2.0 憑證
5. 設定授權重導向 URI：`http://your-domain:8080/oidc/callback`

### 生產環境部署

對於生產環境，建議：

1. **使用 HTTPS**: 手機客戶端需要 HTTPS 才能存取感應器 API
2. **設定網域**: 配置適當的網域名稱和 DNS
3. **環境變數安全**: 使用安全的密鑰管理服務
4. **資料庫備份**: 定期備份 PostgreSQL 資料
5. **監控設定**: 配置日誌和監控系統

### 自訂時段控制

編輯 `litellm_config/custom_callbacks.py` 來自訂時段控制邏輯：

```python
def pre_call_callback(kwargs, completion_response, start_time, end_time):
    # 實作您的時段控制邏輯
    pass
```

## 📁 專案結構

```
DeinClassAI/
├── .env                          # 主要環境變數 (不提交)
├── .env.litellm                  # LiteLLM 環境變數 (不提交)
├── docker-compose.yaml           # Docker 服務編排
├── flask_app/                    # 教師管理面板
│   ├── app.py                   # Flask 後端
│   ├── templates/index.html     # 前端介面
│   └── requirements.txt         # Python 依賴
├── litellm_config/              # LiteLLM 配置
│   ├── config.yaml             # 服務配置
│   └── custom_callbacks.py     # 自訂回調函數
└── student_helper_page/         # 學生輔助頁面
    └── setup.html              # 設定引導頁面
```

## 🛠️ 開發指南

### 本地開發

```bash
# 只啟動核心服務（LiteLLM + PostgreSQL + Open WebUI）
docker-compose up -d

# 開發 Flask 應用時，可以本地運行
cd flask_app
pip install -r requirements.txt
python app.py
```

### 除錯模式

```bash
# 查看服務日誌
docker-compose logs -f litellm
docker-compose logs -f postgres

# 進入容器除錯
docker exec -it deinclassai-litellm bash
docker exec -it deinclassai-postgres psql -U litellm_user -d litellm
```

## 🤝 貢獻

歡迎提交 Issue 和 Pull Request！請確保：

1. 遵循現有的程式碼風格
2. 更新相關文檔
3. 測試您的變更

## 📄 授權

本專案採用 MIT 授權條款。

## 🆘 常見問題

### Q: LiteLLM UI 顯示授權錯誤？
A: 確保 `.env.litellm` 檔案包含正確的 `UI_USERNAME` 和 `UI_PASSWORD`。

### Q: PostgreSQL 連線失敗？
A: 檢查 `DATABASE_URL` 設定是否正確，確保 PostgreSQL 容器已正常啟動。

### Q: 學生無法使用手機感應器？
A: 手機瀏覽器需要 HTTPS 連線才能存取動作和陀螺儀 API，請在生產環境中配置 SSL 憑證。

### Q: Google 登入失敗？
A: 檢查 Google OAuth 設定，確保回調 URL 正確配置。

---

更多詳細資訊請參考 `FRAMEWORK.md`、`FLOW.md` 和 `TODO.md` 檔案。