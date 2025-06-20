import os
import uuid
import requests
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for

# 環境變數設定
LITELLM_ADMIN_URL = os.getenv("LITELLM_API_URL", "http://litellm:4000")
LITELLM_ADMIN_KEY = os.getenv("LITELLM_ADMIN_KEY", "changeme")

app = Flask(__name__)

# 預設權限套餐配置
PERMISSION_PACKAGES = {
    "basic": {
        "name": "基礎班",
        "budget": 5.0,
        "models": ["gpt-4o-mini"],
        "max_budget_per_user": 5.0,
        "description": "適合基礎學習，每月 $5 預算"
    },
    "advanced": {
        "name": "進階班", 
        "budget": 15.0,
        "models": ["gpt-4o-mini", "gpt-4o"],
        "max_budget_per_user": 15.0,
        "description": "適合進階學習，每月 $15 預算，可使用 GPT-4"
    },
    "premium": {
        "name": "專業班",
        "budget": 30.0,
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-4"],
        "max_budget_per_user": 30.0,
        "description": "專業級使用，每月 $30 預算，全模型存取"
    }
}

def make_litellm_request(endpoint, method="GET", data=None):
    """統一的 LiteLLM API 請求函數"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LITELLM_ADMIN_KEY}"
    }

    url = f"{LITELLM_ADMIN_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=15)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=15)
        else:
            raise ValueError(f"不支援的 HTTP 方法: {method}")
            
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

@app.route("/")
def index():
    """主頁面"""
    return render_template("index.html", packages=PERMISSION_PACKAGES)

@app.route("/student_helper_page/setup.html")
def student_helper():
    """學生設定助手頁面"""
    # 從查詢參數中獲取金鑰
    key = request.args.get('key', '')
    name = request.args.get('name', '')
    
    # 讀取學生助手頁面的 HTML 檔案
    try:
        import os
        # 構建學生助手頁面的路徑（現在在容器內的 /app/student_helper_page/）
        helper_path = os.path.join('/app', 'student_helper_page', 'setup.html')
        
        with open(helper_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 學生助手頁面已經有 JavaScript 處理 URL 參數，所以直接返回 HTML
        return html_content
    except FileNotFoundError as e:
        print(f"檔案未找到: {e}")
        return f"學生助手頁面檔案未找到: {e}", 404
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        return f"讀取檔案時發生錯誤: {e}", 500

@app.route("/api/create_key", methods=["POST"])
def create_key():
    """創建新的學生虛擬金鑰"""
    data = request.json or {}
    student_name = data.get("student_name", "").strip()
    package = data.get("package", "basic")
    
    # 驗證輸入
    if not student_name:
        return jsonify({"error": "學生姓名不能為空"}), 400
    
    if package not in PERMISSION_PACKAGES:
        return jsonify({"error": "無效的權限套餐"}), 400
    
    # 獲取套餐配置
    package_config = PERMISSION_PACKAGES[package]
    
    # 構建 LiteLLM API 請求
    payload = {
        "metadata": {
            "student_name": student_name,
            "package": package,
            "created_at": datetime.now().isoformat(),
            "created_by": "teacher_panel"
        },
        "budget": package_config["budget"],
        "models": package_config["models"],
        "max_budget": package_config["max_budget_per_user"],
        "duration": "30d"  # 30天有效期
    }
    
    result, error = make_litellm_request("/key/generate", "POST", payload)
    
    if error:
        return jsonify({"error": f"創建金鑰失敗: {error}"}), 500
    
    virtual_key = result.get("key")
    if not virtual_key:
        return jsonify({"error": "LiteLLM 未返回有效金鑰"}), 500
    
    return jsonify({
        "virtual_key": virtual_key,
        "student_name": student_name,
        "package": package_config["name"],
        "budget": package_config["budget"],
        "models": package_config["models"]
    })

@app.route("/api/list_keys", methods=["GET"])
def list_keys():
    """列出所有虛擬金鑰"""
    result, error = make_litellm_request("/key/list")
    
    if error:
        return jsonify({"error": f"獲取金鑰列表失敗: {error}"}), 500
    
    # 處理和格式化金鑰資訊
    keys = result.get("data", [])
    formatted_keys = []
    
    for key_info in keys:
        metadata = key_info.get("metadata", {})
        formatted_keys.append({
            "key_id": key_info.get("token", ""),
            "student_name": metadata.get("student_name", "未知"),
            "package": metadata.get("package", "basic"),
            "budget_used": key_info.get("spend", 0),
            "budget_limit": key_info.get("budget", 0),
            "created_at": metadata.get("created_at", ""),
            "models": key_info.get("models", []),
            "status": "active" if key_info.get("budget", 0) > key_info.get("spend", 0) else "expired"
        })
    
    return jsonify({"keys": formatted_keys})

@app.route("/api/delete_key/<key_id>", methods=["DELETE"])
def delete_key(key_id):
    """刪除指定金鑰"""
    if not key_id:
        return jsonify({"error": "金鑰 ID 不能為空"}), 400
    
    result, error = make_litellm_request(f"/key/delete", "POST", {"keys": [key_id]})
    
    if error:
        return jsonify({"error": f"刪除金鑰失敗: {error}"}), 500
    
    return jsonify({"status": "deleted", "key_id": key_id})

@app.route("/api/key_stats/<key_id>", methods=["GET"])
def get_key_stats(key_id):
    """獲取特定金鑰的使用統計"""
    if not key_id:
        return jsonify({"error": "金鑰 ID 不能為空"}), 400
    
    result, error = make_litellm_request(f"/key/list?key={key_id}")
    
    if error:
        return jsonify({"error": f"獲取統計失敗: {error}"}), 500
    
    return jsonify(result)

@app.route("/api/packages", methods=["GET"])
def get_packages():
    """獲取所有可用的權限套餐"""
    return jsonify({"packages": PERMISSION_PACKAGES})

@app.route("/api/update_budget", methods=["POST"])
def update_budget():
    """更新金鑰預算"""
    data = request.json or {}
    key_id = data.get("key_id", "").strip()
    new_budget = data.get("budget", 0)
    
    if not key_id:
        return jsonify({"error": "金鑰 ID 不能為空"}), 400
    
    if new_budget <= 0:
        return jsonify({"error": "預算必須大於 0"}), 400
    
    payload = {
        "key": key_id,
        "budget": new_budget
    }
    
    result, error = make_litellm_request("/key/update", "POST", payload)
    
    if error:
        return jsonify({"error": f"更新預算失敗: {error}"}), 500
    
    return jsonify({"status": "updated", "key_id": key_id, "new_budget": new_budget})

@app.route("/api/system_stats", methods=["GET"])
def get_system_stats():
    """獲取系統整體統計資訊"""
    # 獲取所有金鑰資訊
    result, error = make_litellm_request("/key/list")
    
    if error:
        return jsonify({"error": f"獲取系統統計失敗: {error}"}), 500
    
    keys = result.get("data", [])
    
    # 計算統計資訊
    total_keys = len(keys)
    total_spend = sum(key.get("spend", 0) for key in keys)
    total_budget = sum(key.get("budget", 0) for key in keys)
    active_keys = sum(1 for key in keys if key.get("budget", 0) > key.get("spend", 0))
    
    # 按套餐統計
    package_stats = {}
    for key in keys:
        package = key.get("metadata", {}).get("package", "unknown")
        if package not in package_stats:
            package_stats[package] = {"count": 0, "spend": 0, "budget": 0}
        package_stats[package]["count"] += 1
        package_stats[package]["spend"] += key.get("spend", 0)
        package_stats[package]["budget"] += key.get("budget", 0)
    
    return jsonify({
        "total_keys": total_keys,
        "active_keys": active_keys,
        "total_spend": round(total_spend, 2),
        "total_budget": round(total_budget, 2),
        "budget_utilization": round((total_spend / total_budget * 100) if total_budget > 0 else 0, 1),
        "package_stats": package_stats
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "找不到請求的資源"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "伺服器內部錯誤"}), 500

if __name__ == "__main__":
    print(f"啟動教師管理面板...")
    print(f"LiteLLM URL: {LITELLM_ADMIN_URL}")
    print(f"可用套餐: {list(PERMISSION_PACKAGES.keys())}")
    app.run(host="0.0.0.0", port=5000, debug=True)
