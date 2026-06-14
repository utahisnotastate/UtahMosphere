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
  "version": "27.0",
  "build": "omega-build-v27-production",
  "attestation": {
    "tpm_present": true,
    "provisioned": true,
    "sealed": false,
    "enforce": true
  }
}
```

**示例：**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /nonce

签发新的语音命令 nonce。节点认领后且 `UTAH_NONCE_ENFORCE=1`（默认）时必需。

**响应 `200`：**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**示例：**

```bash
curl http://127.0.0.1:8999/nonce
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
  "claimed": true,
  "authorized_nodes": ["abc123..."],
  "swarm_peers": 2,
  "tycoon": {
    "pending": 0,
    "settled_invoices": 1,
    "swept_funds": 5000,
    "settlement_mode": "auto",
    "mempool_failover_nodes": [
      "https://mempool.space/api",
      "https://mempool.space/signet/api",
      "https://blockstream.info/api"
    ]
  },
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true
  }
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
| `nonce` | integer | 认领后 | 来自 `GET /nonce` 的服务器签发时间戳 |
| `command_signature` | string | 认领后 | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — 别名：`signature` |
| `request_signature` | string | 否 | 委派节点的可选 AuthGuard HMAC |

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
| 授权节点 | `"authorize node <64-char-vibe-hash>"` |
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

**Voice Bridge v27.0** 自动调用 `GET /nonce` 并完成签名。手动签名：

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
```

**认领后：** `acoustic_hash` 必须与根节点或 `authorized_nodes[]` 匹配，且 `nonce` + `command_signature` 必须有效，否则内核返回：

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

UtahX 将请求代理至租户端口的 UtahContainerEngine 后端。响应体为 handler 的 JSON 输出。

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

写入对象至 Utah S3 Mesh（本地 NVMe 存储）。

**请求头（可选）：**

| 请求头 | 说明 |
|--------|------|
| `X-Utah-Tenant-ID` | 租户标识 |
| `X-Utah-Signature` | `{tenant_id}:{path}` 的 HMAC-SHA256 |

**示例：**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

读取对象。返回原始字节。使用 `GET /s3/{bucket}/prefix*` 列出。

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

写入键值记录至 Utah RDS Ledger。

**请求体：**

```json
{"key": "user:123", "value": {"name": "Alice", "score": 9000}}
```

**响应 `200`：**

```json
{"key": "user:123", "status": "written", "epoch": 1718280000.0}
```

---

## GET /rds/read/{key}

按键读取记录。

```bash
curl http://127.0.0.1:8999/rds/read/user:123
```

---

## POST /lambda/{function_name}/invoke

调用 Utah Lambda handler（无需拉取容器镜像）。

**请求体：** 传递给 `handler(event, context)` 的 JSON 事件

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

**响应 `200`：**

```json
{"result": {"message": "Hello General 23 from Utah Lambda!"}}
```

---

## POST /app/unlock

提交支付解锁请求。Tycoon 轮询 mempool.space（或 electrum-server）以确认支付最终性。开发地址（`bc1q_utah_*`）在 `auto` 模式下使用定时结算。

**请求体：**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**响应 `202`：**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

结算完成后，使用相同 `X-Client-ID` 调用 `GET /app/{app_name}` 将代理至容器。

---

## POST /admin/revoke-node

从 `authorized_nodes[]` 撤销委派节点。仅限根声纹持有者。Utah-Flux 撤销面板调用此端点。

**请求体：**

```json
{
  "node_hash": "abc123...64chars",
  "acoustic_hash": "root-vibe-hash-64chars"
}
```

**响应 `200`：**

```json
{"status": "revoked", "node_hash": "abc123..."}
```

---

## 错误响应

| 代码 | 场景 |
|------|------|
| `404` | 未知路径或节点不可撤销 |
| `402` | 应用存在但客户端未支付 Tycoon 发票 |
| `403` | 撤销凭证或 HMAC 无效 |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | 容器 handler |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Lambda handler |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | S3 Mesh 对象 |
| `{UTAH_DATA_DIR}/rds/ledger.json` | RDS 键值存储 |
| `security/biometric_ledger.json` | 根声纹哈希（`/etc` 不可写时的本地回退） |
| `tycoon/settlement_ledger.json` | 发票与支付状态 |

默认 `UTAH_DATA_DIR`：`/var/lib/utahmosphere`（权限错误时回退到本地目录）。
