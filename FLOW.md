# 系統流程圖

本系統涉及兩個主要的角色流程：教師的管理流程和學生的使用流程。

## 系統架構流程圖

```mermaid
graph TD
    A["教師"] --> B["Flask 管理面板<br/>(localhost:5000)"]
    C["學生"] --> D["學生輔助頁面<br/>(setup.html)"]
    D --> E["Open WebUI<br/>(localhost:8080)"]
    
    B --> F["LiteLLM API<br/>(localhost:4000)"]
    E --> F
    F --> G["PostgreSQL<br/>資料庫"]
    F --> H["OpenAI API"]
    
    I["自訂回調函數<br/>(時段控制)"] --> F
    
    subgraph "Docker 容器環境"
        B
        F
        G
        E
    end
    
    subgraph "外部服務"
        H
        J["Google OAuth"]
    end
    
    E --> J
```

## 1. 教師管理流程（生成通行證）

```mermaid
sequenceDiagram
    participant T as 教師
    participant F as Flask 管理面板
    participant L as LiteLLM API
    participant P as PostgreSQL
    
    T->>F: 1. 訪問管理面板 (localhost:5000)
    T->>F: 2. 填寫學生資訊和權限套餐
    T->>F: 3. 點擊「生成」按鈕
    F->>L: 4. POST /key/generate<br/>(使用 LITELLM_ADMIN_KEY)
    L->>P: 5. 儲存虛擬金鑰和權限設定
    P-->>L: 6. 確認儲存成功
    L-->>F: 7. 返回新的虛擬金鑰
    F-->>T: 8. 生成 QR Code 並顯示
    T->>T: 9. 投影展示 QR Code
```

## 2. 學生使用流程（登入並設定）

```mermaid
sequenceDiagram
    participant S as 學生
    participant H as 輔助頁面
    participant O as Open WebUI
    participant G as Google OAuth
    participant L as LiteLLM
    
    S->>H: 1. 掃描 QR Code 開啟 setup.html
    S->>H: 2. 點擊「複製金鑰」
    H-->>S: 3. 金鑰複製到剪貼簿
    S->>O: 4. 點擊「進入 AI 教室」
    O->>G: 5. 重導向到 Google 登入
    G-->>O: 6. 驗證成功，返回使用者資訊
    S->>O: 7. 進入設定頁面
    S->>O: 8. 貼上 API 金鑰
    S->>O: 9. 設定 API Base URL (localhost:4000)
    O-->>S: 10. 設定完成，可開始對話
```

## 3. 學生 API 請求流程

```mermaid
sequenceDiagram
    participant S as 學生
    participant O as Open WebUI
    participant L as LiteLLM
    participant C as 自訂回調
    participant P as PostgreSQL
    participant AI as OpenAI API
    
    S->>O: 1. 發送訊息
    O->>L: 2. POST /chat/completions<br/>(附帶虛擬金鑰)
    L->>P: 3. 驗證金鑰有效性
    P-->>L: 4. 返回金鑰資訊和權限
    L->>C: 5. 觸發 pre_call_callback
    C->>C: 6. 檢查時段限制
    C->>P: 7. 檢查預算使用量
    P-->>C: 8. 返回預算資訊
    C-->>L: 9. 權限檢查結果
    
    alt 權限檢查通過
        L->>AI: 10. 轉發請求到 OpenAI
        AI-->>L: 11. 返回 AI 回應
        L->>P: 12. 記錄使用量和費用
        L-->>O: 13. 返回回應給前端
        O-->>S: 14. 顯示 AI 回應
    else 權限檢查失敗
        L-->>O: 15. 返回錯誤訊息
        O-->>S: 16. 顯示錯誤提示
    end
```

## 4. 資料庫操作流程

```mermaid
graph TD
    A["LiteLLM 服務啟動"] --> B["連接 PostgreSQL"]
    B --> C["初始化資料庫表格"]
    
    D["教師生成金鑰"] --> E["INSERT 虛擬金鑰記錄"]
    E --> F["設定權限和預算"]
    
    G["學生發起請求"] --> H["SELECT 金鑰資訊"]
    H --> I["UPDATE 使用量統計"]
    I --> J["INSERT 請求日誌"]
    
    K["權限檢查"] --> L["SELECT 預算餘額"]
    L --> M["SELECT 時段限制"]
    
    subgraph "PostgreSQL 資料表"
        N["virtual_keys<br/>(虛擬金鑰)"]
        O["usage_logs<br/>(使用記錄)"]
        P["budgets<br/>(預算管理)"]
        Q["permissions<br/>(權限設定)"]
    end
    
    E --> N
    I --> O
    F --> P
    F --> Q
```

## 重要特性說明

### 🔐 安全性
- **金鑰隔離**: 學生只能取得虛擬金鑰，真實的 OpenAI Key 完全隔離
- **權限控制**: 每個虛擬金鑰都有獨立的權限設定和預算限制
- **環境變數分離**: LiteLLM 使用獨立的 `.env.litellm` 檔案

### 📊 監控與控制
- **即時預算追蹤**: 每次 API 請求都會更新使用量到 PostgreSQL
- **時段控制**: 透過自訂回調函數實現上課時間限制
- **使用記錄**: 完整的請求日誌供教師查看和分析

### 🚀 效能與擴展性
- **PostgreSQL**: 支援高並發和複雜查詢
- **Docker 容器化**: 易於部署和擴展
- **微服務架構**: 各服務獨立運作，易於維護

### 📱 使用者體驗
- **QR Code**: 簡化學生設定流程
- **Google 登入**: 整合現有教育帳號系統
- **響應式介面**: 支援各種裝置存取