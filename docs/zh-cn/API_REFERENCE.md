# API 参考

基础 URL（默认）：`http://127.0.0.1:8999`

除非另有说明，所有响应均为 JSON。

---

## GET /health

负载均衡器与监控的存活探测。

**响应 `200`：**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "25.0"
}
```

**示例：**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /status

运行快照：UI 状态、已部署租户及节点是否已被认领。

**响应 `200`：**

```json
{
  "ui_state": {
    "node_status": "Active [Sovereign Core v25.0]",
    "active_workloads": 1,
    "last_voice_command": "deploy application my-app",
    "cluster_health": "Resilient",
    "mutation_count": 0
  },
  "tenants": ["my-app"],
  "claimed": true
}
```

---

## POST /command

以编程方式执行语音意图。与 Voice Bridge 发送的载荷相同。

**请求体：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `transcript` | string | 是 | 语音命令（不区分大小写） |
| `acoustic_hash` | string | 是 | 64 字符 SHA-256 声纹哈希 |

**响应 `200`：**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### 支持的 transcript

| 意图 | transcript 示例 |
|------|-----------------|
| 认领节点 | `"Claim node"` |
| 部署应用 | `"deploy application hello"` 或 `"manifest app hello"` |
| 修补应用 | `"patch app hello to add feature x"` |
| 状态 | `"status grid"` |

**认领节点（首次运行）：**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**部署应用（开放模式 — 认领前，接受任意哈希）：**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**认领后：** `acoustic_hash` 必须与锚定的根声纹哈希匹配，否则内核返回：

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

访问已部署的租户应用。由 Utah-Tycoon 支付授权把关。

**请求头：**

| 请求头 | 说明 |
|--------|------|
| `X-Client-ID` | 可选客户端标识（默认为客户端 IP） |

### 未付款客户端 — 响应 `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

发票在当前模拟中约 60 秒后自动结算。

### 已付款客户端 — 响应 `200`

```json
{
  "status": "Unlocked",
  "message": "Container hello executing."
}
```

**示例：**

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## 错误响应

| 代码 | 场景 |
|------|------|
| `404` | 未知路径 |
| `402` | 应用存在但客户端未支付 Tycoon 发票 |

---

## 端口与组播

| 服务 | 端口 / 地址 |
|------|-------------|
| HTTP 入口 | `8999` |
| UtahNetes gossip | UDP `9001`，组播 `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## 数据文件

| 文件 | 用途 |
|------|------|
| `{UTAH_DATA_DIR}/secure_registry.json` | 租户、UtahX 路由、存储索引 |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Utah-Flux UI 状态 |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | 已部署的 handler 桩 |
| `security/biometric_ledger.json` | 根声纹哈希（`/etc` 不可写时的本地回退） |
| `tycoon/settlement_ledger.json` | 发票与支付状态 |

默认 `UTAH_DATA_DIR`：`/var/lib/utahmosphere`（权限错误时回退到本地目录）。
