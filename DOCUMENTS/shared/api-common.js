/* API 測試工具共用 JavaScript 函數 */

// Local Storage 鍵值常數
const STORAGE_KEYS = {
    API_BASE_URL: 'openwebui_api_base_url',
    AUTH_TOKEN: 'openwebui_auth_token',
    REQUEST_TIMEOUT: 'openwebui_request_timeout',
    REQUEST_BODY: 'openwebui_request_body_'
};

// 全域變數
let currentEndpoint = null;

/**
 * 創建端點卡片 HTML
 * @param {Object} endpoint - 端點配置物件
 * @param {string} category - 分類名稱
 * @param {number} index - 端點索引
 * @returns {HTMLElement} 端點卡片元素
 */
function createEndpointCard(endpoint, category, index) {
    const card = document.createElement('div');
    card.className = 'endpoint-card p-3';
    card.innerHTML = `
        <div class="d-flex justify-content-between align-items-start">
            <div class="flex-grow-1">
                <div class="d-flex align-items-center mb-2">
                    <span class="method-badge method-${endpoint.method.toLowerCase()}">${endpoint.method}</span>
                    <code class="ms-2 text-primary">${endpoint.path}</code>
                    ${endpoint.auth ? '<i class="fas fa-lock auth-required" title="需要授權"></i>' : ''}
                </div>
                <h6 class="mb-1">${endpoint.summary}</h6>
                <p class="api-description mb-2">${endpoint.description}</p>
                ${endpoint.params && endpoint.params.length > 0 ? `
                    <div class="mb-2">
                        <small class="text-muted">參數: </small>
                        ${endpoint.params.map(p => `<span class="badge bg-light text-dark param-badge">${p.name}${p.required ? '*' : ''}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
            <div class="ms-3">
                <button class="btn test-button btn-sm" onclick="openTestModal('${category}', ${index})">
                    <i class="fas fa-play"></i> 測試
                </button>
            </div>
        </div>
    `;
    return card;
}

/**
 * 過濾端點列表
 * @param {string} category - 分類名稱
 * @param {string} searchTerm - 搜尋關鍵字
 */
function filterEndpoints(category, searchTerm) {
    const container = document.getElementById(`${category}-endpoints`);
    const cards = container.querySelectorAll('.endpoint-card');
    
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(searchTerm.toLowerCase())) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

/**
 * 打開測試模態框
 * @param {string} category - 分類名稱
 * @param {number} endpointIndex - 端點索引
 */
function openTestModal(category, endpointIndex) {
    try {
        // 獲取當前分類的端點數據
        const categoryVariableName = `${category}Category`;
        const categoryData = window[categoryVariableName];
        
        if (categoryData && categoryData.endpoints && categoryData.endpoints[endpointIndex]) {
            const endpoint = categoryData.endpoints[endpointIndex];
            
            // 使用 postMessage 發送訊息給主頁面
            const message = {
                action: 'openTestModal',
                category: category,
                endpointIndex: endpointIndex,
                endpoint: endpoint
            };
            
            if (window.parent && window.parent !== window) {
                window.parent.postMessage(message, '*');
                console.log(`發送測試請求到主頁面: ${category} - ${endpoint.path}`);
            } else {
                console.error('無法找到主頁面窗口');
            }
        } else {
            console.error(`找不到端點數據: ${categoryVariableName}[${endpointIndex}]`);
        }
    } catch (error) {
        console.error('打開測試模態框時發生錯誤:', error);
    }
}

/**
 * 顯示保存指示器
 * @param {string} indicatorId - 指示器元素 ID
 */
function showSavedIndicator(indicatorId) {
    const indicator = document.getElementById(indicatorId);
    if (indicator) {
        indicator.classList.add('show');
        setTimeout(() => {
            indicator.classList.remove('show');
        }, 2000);
    }
}

/**
 * 重置請求體為初始值
 */
function resetRequestBody() {
    if (!currentEndpoint) {
        alert('請先選擇一個 API 端點進行測試');
        return;
    }

    // 檢查是否有初始請求體
    if (!currentEndpoint.body) {
        alert('此 API 端點沒有預設的請求體，無法重置。');
        return;
    }

    const requestBodyTextarea = document.getElementById('requestBody');
    const currentValue = requestBodyTextarea.value.trim();
    
    // 獲取初始值
    const initialValue = JSON.stringify(currentEndpoint.body, null, 2);
    
    // 檢查是否已經是初始值
    if (currentValue === initialValue) {
        alert('請求體已經是初始值，無需重置。');
        return;
    }
    
    // 檢查是否有內容需要確認
    let needConfirm = currentValue !== '' && currentValue !== '{}';
    
    if (!needConfirm || confirm('確定要將請求體重置為初始值嗎？這將清除當前的修改內容。')) {
        // 設置初始值
        requestBodyTextarea.value = initialValue;
        
        // 清除該端點保存的請求體
        const key = STORAGE_KEYS.REQUEST_BODY + currentEndpoint.category + '_' + currentEndpoint.endpointIndex;
        localStorage.removeItem(key);
        
        // 顯示重置成功提示
        showResetIndicator();
        showResetButtonSuccess();
    }
}

/**
 * 顯示重置成功指示器
 */
function showResetIndicator() {
    const indicator = document.getElementById('bodySavedIndicator');
    if (indicator) {
        // 暫時改變指示器內容和顏色
        const originalContent = indicator.innerHTML;
        const originalColor = indicator.style.color;
        
        indicator.innerHTML = '<i class="fas fa-undo"></i> 已重置';
        indicator.style.color = '#17a2b8'; // 使用藍色表示重置
        indicator.classList.add('show');
        
        setTimeout(() => {
            // 恢復原始內容和顏色
            indicator.innerHTML = originalContent;
            indicator.style.color = originalColor || '#28a745';
            indicator.classList.remove('show');
        }, 2500); // 延長顯示時間到 2.5 秒
    }
}

/**
 * 顯示重置按鈕成功狀態
 */
function showResetButtonSuccess() {
    // 找到重置按鈕（通過事件查找更可靠）
    const resetButton = document.querySelector('button[onclick="resetRequestBody()"]');
    if (resetButton) {
        // 暫時改變按鈕內容和樣式
        const originalContent = resetButton.innerHTML;
        
        resetButton.innerHTML = '<i class="fas fa-check"></i> 完成';
        resetButton.classList.add('success');
        resetButton.disabled = true;
        
        setTimeout(() => {
            // 恢復原始內容和樣式
            resetButton.innerHTML = originalContent;
            resetButton.classList.remove('success');
            resetButton.disabled = false;
        }, 1500);
    }
}

/**
 * 保存請求體到 Local Storage
 */
function saveRequestBody() {
    if (currentEndpoint) {
        const requestBody = document.getElementById('requestBody').value;
        const key = STORAGE_KEYS.REQUEST_BODY + currentEndpoint.category + '_' + currentEndpoint.endpointIndex;
        localStorage.setItem(key, requestBody);
        
        // 顯示保存指示器
        showSavedIndicator('bodySavedIndicator');
    }
}

/**
 * 載入保存的請求體
 * @returns {boolean} 是否成功載入保存的請求體
 */
function loadSavedRequestBody() {
    if (currentEndpoint) {
        const key = STORAGE_KEYS.REQUEST_BODY + currentEndpoint.category + '_' + currentEndpoint.endpointIndex;
        const savedBody = localStorage.getItem(key);
        if (savedBody) {
            document.getElementById('requestBody').value = savedBody;
            return true;
        }
    }
    return false;
}

/**
 * 格式化 JSON 字串
 * @param {string} jsonString - JSON 字串
 * @returns {string} 格式化後的 JSON 字串
 */
function formatJSON(jsonString) {
    try {
        const parsed = JSON.parse(jsonString);
        return JSON.stringify(parsed, null, 2);
    } catch (error) {
        return jsonString;
    }
}

/**
 * 驗證 JSON 格式
 * @param {string} jsonString - JSON 字串
 * @returns {Object} 驗證結果 {valid: boolean, error: string}
 */
function validateJSON(jsonString) {
    try {
        JSON.parse(jsonString);
        return { valid: true, error: null };
    } catch (error) {
        return { valid: false, error: error.message };
    }
}

/**
 * 複製文字到剪貼簿
 * @param {string} text - 要複製的文字
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (error) {
        console.error('複製到剪貼簿失敗:', error);
        return false;
    }
}

/**
 * 建立端點搜尋框
 * @param {string} category - 分類名稱
 * @param {string} categoryDisplayName - 分類顯示名稱
 * @returns {HTMLElement} 搜尋框元素
 */
function createSearchBox(category, categoryDisplayName) {
    const searchBox = document.createElement('div');
    searchBox.className = 'search-box';
    searchBox.innerHTML = `
        <input type="text" class="form-control" placeholder="搜尋 ${categoryDisplayName} API..." onkeyup="filterEndpoints('${category}', this.value)">
    `;
    return searchBox;
}

/**
 * 建立端點列表容器
 * @param {string} category - 分類名稱
 * @returns {HTMLElement} 端點列表容器元素
 */
function createEndpointListContainer(category) {
    const container = document.createElement('div');
    container.className = 'endpoint-list';
    container.id = `${category}-endpoints`;
    return container;
}

/**
 * 初始化分類頁面
 * @param {string} category - 分類名稱
 * @param {Object} categoryData - 分類數據
 */
function initializeCategoryPage(category, categoryData) {
    // 尋找端點列表容器 - 支援兩種結構
    let endpointContainer = document.getElementById(`${category}-endpoints`);
    
    // 如果找不到新格式的容器，檢查是否有舊格式的 main-container
    if (!endpointContainer) {
        const mainContainer = document.getElementById('main-container');
        if (mainContainer) {
            // 為舊格式創建完整的結構
            mainContainer.innerHTML = `
                <div class="search-box">
                    <input type="text" class="form-control" placeholder="搜尋 ${categoryData.name} API..." onkeyup="filterEndpoints('${category}', this.value)">
                </div>
                <div class="endpoint-list" id="${category}-endpoints"></div>
            `;
            endpointContainer = document.getElementById(`${category}-endpoints`);
        }
    }
    
    if (!endpointContainer) {
        console.error(`找不到端點容器: ${category}-endpoints，也找不到 main-container`);
        return;
    }

    // 清空端點容器
    endpointContainer.innerHTML = '';

    // 載入端點
    categoryData.endpoints.forEach((endpoint, index) => {
        const endpointCard = createEndpointCard(endpoint, category, index);
        endpointContainer.appendChild(endpointCard);
    });

    console.log(`已初始化 ${category} 分類，載入 ${categoryData.endpoints.length} 個端點`);
    
    // 通知主頁面分類已初始化完成
    notifyParentCategoryReady(category, categoryData.endpoints.length);
}

/**
 * 通知主頁面分類已準備就緒
 * @param {string} category - 分類名稱
 * @param {number} endpointCount - 端點數量
 */
function notifyParentCategoryReady(category, endpointCount) {
    try {
        if (window.parent && window.parent !== window) {
            const message = {
                action: 'categoryReady',
                category: category,
                endpointCount: endpointCount
            };
            window.parent.postMessage(message, '*');
            console.log(`已通知主頁面 ${category} 分類準備就緒，包含 ${endpointCount} 個端點`);
        }
    } catch (error) {
        console.error('通知主頁面時發生錯誤:', error);
    }
}

// 匯出函數供其他檔案使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createEndpointCard,
        filterEndpoints,
        openTestModal,
        showSavedIndicator,
        resetRequestBody,
        saveRequestBody,
        loadSavedRequestBody,
        formatJSON,
        validateJSON,
        copyToClipboard,
        initializeCategoryPage,
        STORAGE_KEYS
    };
} 