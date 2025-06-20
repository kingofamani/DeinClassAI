# QA 指南 - 常見問題與解決方案

## 📚 目錄
- [OpenWebUI API 問題](#openwebui-api-問題)
- [環境設定問題](#環境設定問題)
- [Docker 服務問題](#docker-服務問題)

---

## OpenWebUI API 問題

### Q1: 使用 `/api/v1/users` 端點創建用戶時出現 "Method Not Allowed" 錯誤

**問題描述：**
```bash
curl -X POST \
  http://localhost:8080/api/v1/users \
  -H "Content-Type: application/json" \
  -H "Authorization: sk-e7b570d75ef3448e808227337e8a70d5" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpassword",
    "role": "user"
  }'
```

**錯誤回應：**
```json
{
  "detail": "Method Not Allowed"
}
```

**解決方案：**

1. **使用正確的端點**：
   - ❌ 錯誤：`/api/v1/users`
   - ✅ 正確：`/api/v1/auths/signup`

2. **正確的 API 調用**：
   ```bash
   curl -X POST \
     http://localhost:8080/api/v1/auths/signup \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -d '{
       "email": "test@example.com",
       "name": "Test User",
       "password": "testpassword123"
     }'
   ```

**說明：**
- `/api/v1/users` 端點主要用於查詢用戶，不支援 POST 方法創建用戶
- 用戶註冊應使用 `/api/v1/auths/signup` 端點
- 需要有效的 Bearer Token 進行認證

---

### Q2: 無法訪問 OpenWebUI Swagger API 文檔

**問題描述：**
訪問 `http://localhost:8080/docs` 時無法顯示 Swagger 文檔介面

**解決方案：**

1. **設置開發模式環境變數**：
   在 `docker-compose.yaml` 中的 `open_webui` 服務添加：
   ```yaml
   environment:
     # 啟用開發模式以顯示 Swagger API 文檔
     - 'ENV=dev'
     # ... 其他環境變數
   ```

2. **重新啟動服務**：
   ```bash
   docker-compose down open_webui
   docker-compose up -d open_webui
   ```

3. **驗證環境變數**：
   ```bash
   docker exec deinclassai-open-webui env | findstr ENV
   ```
   應該顯示：`ENV=dev`

4. **可訪問的 API 文檔端點**：
   - 主要文檔：`http://localhost:8080/docs`
   - WebUI API：`http://localhost:8080/api/v1/docs`
   - Ollama API：`http://localhost:8080/ollama/docs`

**注意事項：**
- 必須設置 `ENV=dev` 才能訪問 Swagger 文檔
- 服務需要完全啟動後才能訪問文檔（通常需要等待 10-30 秒）

---

### Q3: 如何獲取 OpenWebUI API Key

**問題描述：**
需要 API Key 來調用 OpenWebUI 的 API 端點

**解決方案：**

1. **通過 Web 介面獲取**：
   - 訪問 `http://localhost:8080`
   - 登入 OpenWebUI
   - 前往 `Settings > Account`
   - 生成或複製 API Key

2. **API Key 格式**：
   - 格式：`sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - 在 HTTP 標頭中使用：`Authorization: Bearer YOUR_API_KEY`

3. **測試 API Key 有效性**：
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        http://localhost:8080/api/v1/users
   ```

---

## 環境設定問題

### Q4: PowerShell 中執行 curl 命令出現錯誤

**問題描述：**
在 Windows PowerShell 中使用 `curl` 命令時出現參數錯誤

**解決方案：**

1. **使用 PowerShell 原生命令**：
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:8080/docs" -Method GET -UseBasicParsing
   ```

2. **或者使用 cmd 風格的 curl**：
   ```powershell
   curl.exe -X POST http://localhost:8080/api/v1/auths/signup `
     -H "Content-Type: application/json" `
     -H "Authorization: Bearer YOUR_API_KEY" `
     -d '{"email":"test@example.com","name":"Test User","password":"testpassword123"}'
   ```

3. **PowerShell 測試腳本範例**：
   ```powershell
   try {
       $response = Invoke-WebRequest -Uri "http://localhost:8080/docs" -Method GET -UseBasicParsing
       Write-Host "成功! 狀態碼: $($response.StatusCode)" -ForegroundColor Green
   } catch {
       Write-Host "失敗: $($_.Exception.Message)" -ForegroundColor Red
   }
   ```

---

## Docker 服務問題

### Q5: 如何檢查 OpenWebUI 服務狀態

**問題描述：**
需要確認 OpenWebUI 服務是否正常運行

**解決方案：**

1. **檢查容器狀態**：
   ```bash
   docker ps --filter name=deinclassai-open-webui
   ```
   應該顯示 `(healthy)` 狀態

2. **查看服務日誌**：
   ```bash
   docker logs deinclassai-open-webui --tail 10
   ```

3. **檢查端口綁定**：
   ```bash
   docker port deinclassai-open-webui
   ```
   應該顯示：`8080/tcp -> 0.0.0.0:8080`

4. **測試服務響應**：
   ```bash
   curl -I http://localhost:8080
   ```

---

### Q6: 重新啟動特定服務

**問題描述：**
需要重新啟動某個特定的 Docker 服務

**解決方案：**

1. **重新啟動 OpenWebUI**：
   ```bash
   docker-compose down open_webui
   docker-compose up -d open_webui
   ```

2. **重新啟動所有服務**：
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **檢查服務依賴**：
   ```bash
   docker-compose ps
   ```

---

## 🔧 故障排除檢查清單

當遇到 API 問題時，請按順序檢查：

1. ✅ **服務狀態**：容器是否正常運行？
2. ✅ **環境變數**：是否設置 `ENV=dev`？
3. ✅ **端點路徑**：是否使用正確的 API 端點？
4. ✅ **認證方式**：是否提供有效的 Bearer Token？
5. ✅ **網路連接**：是否可以訪問 `localhost:8080`？
6. ✅ **服務日誌**：是否有錯誤訊息？

---

## 📞 獲取更多幫助

- **Swagger 文檔**：`http://localhost:8080/docs`
- **OpenWebUI GitHub**：https://github.com/open-webui/open-webui
- **服務日誌**：`docker logs deinclassai-open-webui`

---

*最後更新：2025-06-20* 