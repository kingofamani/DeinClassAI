# DeinClassAI 專案總結 (初始化完成)

## 專案概述

**DeinClassAI** 是一個專為教育場景設計的 AI 服務教師管理面板，旨在提供安全、可控、易用的 LLM 訪問權限管理方案。該專案解決了教師在課堂中引入 AI 工具時面臨的核心挑戰：如何有效管理學生的使用權限、控制成本，並確保 AI 的使用符合教學目標。

## 技術架構

專案採用微服務架構，包含三個主要服務：

### 1. Teacher Panel (flask_app/)
- **技術棧**: Python Flask
- **功能**: 教師管理後台，用於生成學生通行證
- **核心檔案**:
  - `app.py`: Flask 應用主程式，提供 API 端點
  - `templates/index.html`: 教師操作界面
  - `Dockerfile`: 容器化配置
  - `requirements.txt`: Python 依賴套件

### 2. Permission Core (litellm_config/)
- **技術棧**: LiteLLM 代理服務
- **功能**: 權限控制中樞，管理 API 金鑰和使用限制
- **核心檔案**:
  - `config.yaml`: LiteLLM 服務配置
  - `custom_callbacks.py`: 自定義時段控制邏輯

### 3. Student UI
- **技術棧**: Open WebUI
- **功能**: 學生聊天界面
- **支援功能**: Google 教育帳號登入 (OIDC)

### 4. Student Helper (student_helper_page/)
- **檔案**: `setup.html`
- **功能**: 協助學生複製 API 金鑰並跳轉至 AI 教室

## 系統流程

### 教師管理流程
1. 教師訪問 Flask 管理面板 (port 5000)
2. 輸入學生姓名和選擇權限套餐
3. 系統調用 LiteLLM API 生成虛擬金鑰
4. 生成包含金鑰的 QR Code
5. 投影展示給學生

### 學生使用流程
1. 掃描 QR Code 開啟 setup.html
2. 複製個人專屬 API 金鑰
3. 進入 Open WebUI (port 8080)
4. 使用 Google 教育帳號登入
5. 設定 API 金鑰和 Base URL
6. 開始 AI 對話

### API 請求控制流程
1. 學生在 Open WebUI 發送訊息
2. 請求傳送至 LiteLLM 服務
3. LiteLLM 執行多重檢查：
   - 金鑰有效性驗證
   - 模型權限檢查
   - 預算額度檢查
   - 時段控制檢查 (custom_callbacks.py)
4. 通過檢查後轉發至 OpenAI
5. 回傳結果給學生

## 權限控制機制

### 預算控制
- 每個學生金鑰預設 $5 美元額度
- 可依權限套餐調整

### 模型限制
- 預設允許 `gpt-4o-mini`
- 可根據套餐開放 `gpt-4o` 等進階模型

### 時段控制
- 預設允許台灣時間 08:00-22:00 使用
- 透過 `custom_callbacks.py` 實現
- 可依學生 metadata 自訂時段

### 身份認證
- 學生端使用 Google 教育帳號 (OIDC)
- 教師端使用 LiteLLM 主控金鑰

## 部署架構

### 容器化部署
- 使用 Docker Compose 編排
- 三個主要服務：
  - `teacher_panel`: Flask 教師面板
  - `litellm`: 權限控制核心
  - `open_webui`: 學生前端界面

### 資料持久化
- `litellm_data`: 儲存金鑰和預算資料
- `open_webui_data`: 儲存用戶帳號和對話歷史

### 網路配置
- 內部橋接網路 `deinclassai_net`
- 服務間通過容器名稱通信

## 環境變數配置

專案需要以下關鍵環境變數：
- `OPENAI_API_KEY`: OpenAI API 金鑰
- `LITELLM_ADMIN_KEY`: LiteLLM 主控金鑰
- `GOOGLE_CLIENT_ID`: Google OAuth 客戶端 ID
- `GOOGLE_CLIENT_SECRET`: Google OAuth 客戶端密鑰

## 開發狀態

根據 TODO.md，主要開發任務包括：
- ✅ 基礎架構設計完成
- ✅ Docker 容器化配置完成
- ✅ Flask 應用核心功能完成
- ✅ LiteLLM 權限控制配置完成
- ✅ 學生輔助頁面完成
- ⚠️ 需要配置真實的 API 金鑰
- ⚠️ 需要部署測試和調優

## 特色功能

1. **QR Code 一鍵分發**: 透過 QR Code 簡化學生 onboarding 流程
2. **精細權限控制**: 支援模型、預算、時段多維度限制
3. **教育友善設計**: 整合 Google 教育帳號，無需記憶新密碼
4. **微服務架構**: 各組件獨立，易於維護和擴展
5. **容器化部署**: 支援本地開發和雲端部署

## 技術亮點

- **Flask + LiteLLM + Open WebUI** 的三層架構
- **自定義 callback 機制**實現靈活的時段控制
- **Docker Compose 編排**實現一鍵部署
- **OIDC 整合**提供企業級身份認證
- **SQLite 資料庫**提供輕量級資料持久化

這個專案為教育場景中的 AI 工具使用提供了完整的管理解決方案，兼顧了安全性、易用性和教學需求。 