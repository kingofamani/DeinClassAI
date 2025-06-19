# 專案任務列表 (TODO)

## ✅ 已完成項目

- [x] **Docker & 部署基礎設定**:
    - [x] 編寫 `docker-compose.yaml`，用於本地開發環境的編排
    - [x] 配置 PostgreSQL 資料庫服務
    - [x] 設定 LiteLLM 服務與 PostgreSQL 整合
    - [x] 建立 `.gitignore` 檔案，保護敏感資訊

- [x] **LiteLLM 配置**:
    - [x] 編寫 `litellm_config/config.yaml`，配置模型列表和資料庫連線
    - [x] 編寫 `litellm_config/custom_callbacks.py`，實現時段控制邏輯
    - [x] 建立 `.env.litellm.example` 範本檔案
    - [x] 配置 LiteLLM UI 登入憑證

- [x] **環境變數管理**:
    - [x] 建立 `.env.example` 範本檔案
    - [x] 分離 LiteLLM 專用環境變數檔案 (`.env.litellm`)
    - [x] 解決 SSO 授權衝突問題

## 🔄 進行中項目

- [ ] **Flask 應用開發**:
    - [x] 設置 `flask_app/` 目錄結構
    - [x] 創建 `requirements.txt`
    - [ ] 完善 `app.py`，實現後端 API 邏輯
    - [ ] 完善 `templates/index.html`，優化前端界面

- [ ] **學生輔助頁面**:
    - [x] 創建 `student_helper_page/setup.html`
    - [ ] 將 `setup.html` 託管到一個公開可訪問的靜態網站服務（如 GitHub Pages）

## 📋 待完成項目

- [ ] **環境設定**: 
    - [ ] 獲取 OpenAI API 金鑰
    - [ ] 配置實際的環境變數值

- [ ] **Google Cloud 設定**: 
    - [ ] 創建 OAuth 2.0 憑證，用於 Open WebUI 的 Google 登入
    - [ ] 配置 OIDC 回調 URL

- [ ] **生產環境部署**:
    - [ ] 在 Railway 或 VPS 上進行部署測試
    - [ ] 配置 HTTPS 憑證
    - [ ] 設定網域名稱和 DNS

- [ ] **功能完善**:
    - [ ] 實現 QR Code 生成功能
    - [ ] 加入預算管理介面
    - [ ] 實現時段控制管理

- [ ] **測試**:
    - [ ] 端到端測試教師管理流程
    - [ ] 端到端測試學生使用流程
    - [ ] 驗證預算、模型、時段控制規則是否生效

- [ ] **文檔完善**:
    - [x] 更新 `README.md`，加入詳細的部署步驟和環境變數說明
    - [ ] 建立使用者手冊
    - [ ] 建立部署指南

## 🚨 重要注意事項

1. **資料庫遷移**: 已從 SQLite 改為 PostgreSQL，需確保舊資料的遷移
2. **環境變數安全**: 確保 `.env.litellm` 檔案不被提交到版本控制
3. **LITELLM_SALT_KEY**: 一旦設定就不能更改，請妥善保管
4. **HTTPS 需求**: 手機客戶端需要 HTTPS 才能存取動作感應器 API