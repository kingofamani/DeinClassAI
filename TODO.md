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

- [x] **Flask 應用開發**:
    - [x] 設置 `flask_app/` 目錄結構
    - [x] 創建 `requirements.txt`
    - [x] 完善 `app.py`，實現完整的後端 API 邏輯
        - [x] 統一的 LiteLLM API 請求函數
        - [x] 多層級權限套餐系統 (基礎班、進階班、專業班)
        - [x] 金鑰管理功能 (創建、列表、刪除、統計)
        - [x] 預算管理功能 (查詢、更新)
        - [x] 系統統計功能
        - [x] 完善的錯誤處理機制
    - [x] 完善 `templates/index.html`，打造現代化教師管理介面
        - [x] 響應式設計，支援桌面和行動裝置
        - [x] 即時系統統計儀表板
        - [x] 學生金鑰管理功能
        - [x] 預算監控和更新功能
        - [x] QR Code 生成和顯示
        - [x] 現代化 UI 設計

- [x] **學生輔助頁面**:
    - [x] 創建 `student_helper_page/setup.html`
    - [x] 完全重寫為現代化、響應式設計
        - [x] 自動偵測裝置類型
        - [x] 智慧型 API Base URL 設定
        - [x] 改進的金鑰複製功能 (支援多種瀏覽器)
        - [x] 清晰的步驟引導
        - [x] 鍵盤快捷鍵支援
        - [x] 錯誤處理和用戶回饋

- [x] **QR Code 功能實現**:
    - [x] 整合 QRCode.js 庫
    - [x] 自動生成包含學生資訊的 QR Code
    - [x] 響應式 QR Code 顯示
    - [x] 一鍵複製金鑰功能

## 🔄 進行中項目

- [ ] **預算管理介面**:
    - [x] 後端 API 實現 (預算查詢、更新)
    - [x] 前端預算監控介面
    - [x] 預算使用率視覺化
    - [ ] 預算警告和通知系統
    - [ ] 批量預算管理功能

- [ ] **時段控制管理**:
    - [x] LiteLLM 時段控制回調函數
    - [ ] 前端時段設定介面
    - [ ] 時段規則管理功能

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
    - [ ] 將 `setup.html` 託管到一個公開可訪問的靜態網站服務（如 GitHub Pages）

- [ ] **功能完善**:
    - [ ] 實現批量金鑰操作
    - [ ] 加入使用統計圖表
    - [ ] 實現金鑰有效期管理
    - [ ] 加入學生使用報告功能

- [ ] **測試**:
    - [ ] 端到端測試教師管理流程
    - [ ] 端到端測試學生使用流程
    - [ ] 驗證預算、模型、時段控制規則是否生效

- [ ] **文檔完善**:
    - [x] 更新 `README.md`，加入詳細的部署步驟和環境變數說明
    - [x] 建立快速開始指南 (`QUICK_START.md`)
    - [x] 建立啟動腳本 (`start.sh` 和 `start.ps1`)
    - [ ] 建立使用者手冊
    - [ ] 建立部署指南

## 🚨 重要注意事項

1. **資料庫遷移**: 已從 SQLite 改為 PostgreSQL，需確保舊資料的遷移
2. **環境變數安全**: 確保 `.env.litellm` 檔案不被提交到版本控制
3. **LITELLM_SALT_KEY**: 一旦設定就不能更改，請妥善保管
4. **HTTPS 需求**: 手機客戶端需要 HTTPS 才能存取動作感應器 API
5. **權限套餐**: 新增了三層級權限套餐系統，可根據需求調整預算和模型存取權限