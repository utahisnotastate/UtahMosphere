### 🍳 开发者手册：UtahMosphere 配方

本手册是开发者的入口。完整配方库见 **[配方索引](recipes/README.md)**。

---

#### **快速链接**

| 任务 | 说明 |
|------|------|
| 通过 API 部署 | 见下方「通过 /command 部署」配方 |
| 健康监控 | 见 [示例 check-node-health](../../examples/check-node-health/) |
| 支付流程（402） | 见 [模板 tycoon-payment-client](../../templates/tycoon-payment-client/) |
| HMAC 签名 | 见下方「生成签名」配方 |
| 语音意图 | 见下方「自定义语音意图」配方 |

**教程：** [你的第一个应用](tutorials/05-developer-first-app.md)  
**模板：** [templates/](../../templates/) · **入门项目：** [starter-projects/](../../starter-projects/)

---

#### **前端配方：直连边缘图片上传**

> **状态：** 路线图（S3 Mesh API 尚未路由）。模式已为迁移做好准备。

```javascript
async function uploadToUtah(file, tenantId, signature) {
  const response = await fetch(`http://utahmosphere.local:8999/s3/assets/${file.name}`, {
    method: 'POST',
    headers: {
      'X-Utah-Tenant-ID': tenantId,
      'X-Utah-Signature': signature,
      'Content-Type': file.type
    },
    body: file
  });
  return await response.json();
}
```

**当前已实现：** 使用 `fetch('http://127.0.0.1:8999/status')` — 见 [frontend-upload 模板](../../templates/frontend-upload/)。

---

#### **后端配方：通过 /command 部署**

> **状态：** 已实现

```python
import json, urllib.request

def deploy(app_name):
    payload = json.dumps({
        "transcript": f"deploy application {app_name}",
        "acoustic_hash": "0" * 64,
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8999/command",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

或运行：`python examples/voice-deploy-simulator/deploy.py my-app`

---

#### **后端配方：同步会话存储**

> **状态：** 路线图（RDS 账本 HTTP 路由）

```python
import requests

def save_session(session_id, user_data):
    url = "http://localhost:8999/rds/write"
    payload = {"key": f"session:{session_id}", "value": user_data}
    requests.post(url, json=payload)

def get_session(session_id):
    url = f"http://localhost:8999/rds/read/session:{session_id}"
    return requests.get(url).json()['value']
```

---

#### **语音桥接配方：自定义意图**

```python
CUSTOM_INTENTS = {
    "go dark mode": lambda: print("[Vibe] Initiating aesthetic shift..."),
}

def handle_custom(transcript):
    for phrase, action in CUSTOM_INTENTS.items():
        if phrase in transcript.lower():
            action()
            return True
    return False
```

完整模式见 [voice-command-client 模板](../../templates/voice-command-client/)。

---

#### **样板：UtahMosphere Python 服务**

模板：[templates/python-http-service/](../../templates/python-http-service/)

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "running", "environment": "UtahMosphere"}).encode())

if __name__ == "__main__":
    HTTPServer(('', 8080), SimpleHandler).serve_forever()
```

---

#### **安全说明：生成签名**

```python
import hmac, hashlib, os

SECRET = os.environ.get("UTAH_SECRET_VECTOR", "utah_akashic_sovereign_perimeter_authorization_vector").encode()
tenant_id = "my-tenant"
path = "/s3/bucket/key"
signature = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

生产环境请更改 `UTAH_SECRET_VECTOR` 环境变量。详见 [能力矩阵](CAPABILITY_MATRIX.md) 安全模型部分。
