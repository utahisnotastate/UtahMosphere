# 教程：你的第一个应用

**受众：** 前端与后端开发者  
**时间：** 30 分钟  
**目标：** 在 UtahMosphere 上端到端部署、访问并扩展应用

---

## 前置条件

- Python 3.11+
- `pip install -r requirements.txt`
- 已完成[本地开发指南](../LOCAL_DEVELOPMENT.md)（可选）

---

## 步骤 1：启动内核

```bash
export UTAH_DATA_DIR="$(pwd)/.utah-data"
python utahmosphere_os.py
```

确认：

```bash
curl http://127.0.0.1:8999/health
```

---

## 步骤 2：部署 `hello-world`

```bash
python examples/voice-deploy-simulator/deploy.py hello-world
```

预期响应包含端口 `8200`（首个租户）。

检查状态：

```bash
curl http://127.0.0.1:8999/status
```

---

## 步骤 3：访问你的应用（支付关卡）

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

首次响应：**402 Payment Required**，附带 Bitcoin 地址。

等待约 60 秒（模拟结算），重试：

```bash
curl -H "X-Client-ID: dev-user" http://127.0.0.1:8999/app/hello-world
```

响应：**200 Unlocked**。

或使用辅助脚本：

```bash
python examples/paid-app-access/access_app.py hello-world
```

---

## 步骤 4：自定义 Handler

编辑：

```
.utah-data/containers/hello-world/handler.py
```

```python
def handler(event, context):
    return {
        "status": "active",
        "message": "Hello from my first UtahMosphere app!",
        "event": event,
    }
```

通过语音/API 修补：

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"patch app hello-world to add greeting","acoustic_hash":"0"}'
```

---

## 步骤 5：构建真实服务（模板）

复制入门项目：

```bash
cp -r starter-projects/minimal-api my-api
cd my-api
python handler_service.py
```

部署到 UtahMosphere：

```bash
python ../examples/voice-deploy-simulator/deploy.py my-api
```

---

## 步骤 6：前端集成

使用 [frontend-upload 模板](../../templates/frontend-upload/) 或从你的应用获取状态：

```javascript
const res = await fetch("http://127.0.0.1:8999/status");
const data = await res.json();
console.log("Active tenants:", data.tenants);
```

---

## 步骤 7：生成 HMAC 签名（未来存储 API）

```python
import hmac
import hashlib

SECRET = b"utah_akashic_sovereign_perimeter_authorization_vector"
tenant_id = "hello-world"
path = "/s3/assets/photo.jpg"
sig = hmac.new(SECRET, f"{tenant_id}:{path}".encode(), hashlib.sha256).hexdigest()
```

---

## 你构建了什么

- 通过 `/command` API 部署应用
- 完成 Tycoon HTTP 402 支付流程
- 自定义 `handler.py`
- 将前端连接到 `/status`

---

## 下一步

- [开发者手册](../DEVELOPER_COOKBOOK.md)
- [API 参考](../API_REFERENCE.md)
- [模板](../../templates/) 与 [入门项目](../../starter-projects/)
