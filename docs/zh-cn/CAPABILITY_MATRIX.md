# 能力矩阵

UtahMosphere OS **v27.0 Production Immutable** — 主权信任锚点已全部完成。

---

## HTTP API 端点

| 端点 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/health` | GET | **已实现** | 存活探测 + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **已实现** | 签发新的语音命令 nonce（30 秒窗口） |
| `/status` | GET | **已实现** | UI 状态、租户、attestation、内存池故障转移统计 |
| `/command` | POST | **已实现** | 语音意图 + 自动 nonce 签名（`voice_bridge_signed.py`） |
| `/admin/revoke-node` | POST | **已实现** | 根节点专用授权节点撤销 |
| `/app/unlock` | POST | **已实现** | 提交支付；内存池故障转移结算 |
| `/app/{name}` | GET | **已实现** | Tycoon 402 关卡 + UtahX 代理至容器 |
| `/app/{name}/{path}` | GET | **已实现** | 子路径代理至容器后端 |
| `/s3/{bucket}/{key}` | GET | **已实现** | 对象读取（本地 NVMe） |
| `/s3/{bucket}/{key}` | PUT/POST | **已实现** | 对象写入；可选 HMAC 头 |
| `/s3/{bucket}/{prefix}*` | GET | **已实现** | 列出对象 |
| `/lambda/{fn}/invoke` | POST | **已实现** | Serverless handler 调用 |
| `/lambda/{fn}` | GET | **已实现** | 空事件 GET 调用 |
| `/rds/write` | POST | **已实现** | 键值写入 |
| `/rds/read/{key}` | GET | **已实现** | 键值读取 |

---

## 核心子系统

| 组件 | 状态 | 当前可用功能 |
|------|------|--------------|
| **Golden Master（`utahmosphere_master.py`）** | **已实现** | 统一入口 |
| **内核（`utahmosphere_os.py`）** | **已实现** | 完整 HTTP 多路复用、注册表、网格 |
| **硬件 attestation（`attestation_guard.py`）** | **已实现** | bootstrap 与 health 中的 TPM 2.0 PCR0 关卡 |
| **内存池故障转移（`tycoon_failover.py`）** | **已实现** | 美/欧/亚内存池静默故障转移 |
| **签名语音桥（`voice_bridge_signed.py`）** | **已实现** | 自动 `GET /nonce` + HMAC 签名 |
| **UtahX 代理（`utahx_proxy.py`）** | **已实现** | 实时 HTTP 代理至容器端口 |
| **UtahContainerEngine（`utah_container_runtime.py`）** | **已实现** | 8200+ 租户 HTTP 服务 |
| **Lazarus AST（`utah_lazarus.py`）** | **已实现** | AST 验证 handler 变更 + OTA |
| **S3 / Lambda / RDS** | **已实现** | 完整云 parity |
| **Quantum Ledger** | **已实现** | 生物识别认领 + 验证 |
| **Utah-Tycoon** | **已实现** | 故障转移内存池 + electrum（`tycoon_settlement.py`） |
| **AuthGuard（`ledger_auth.py`）** | **已实现** | `authorized_nodes[]` 强制执行 |
| **Nonce-Guard（`nonce_guard.py`）** | **已实现** | 语音命令 30 秒防重放 |
| **UtahNetes + Swarm DHT** | **已实现** | 签名 gossip + 确定性路由 |
| **Genesis ISO（`genesis_iso_builder.py`）** | **已实现** | Alpine vmlinuz + 支持 attestation 的 bootstrap |
| **Utah-Flux 撤销 UI** | **已实现** | `flux_gui.py` 中的管理面板 |
| **Auto-Genesis / Bootstrap** | **已实现** | systemd + attestation 关卡 |

---

## 语音命令

| 命令模式 | 状态 | 示例 |
|----------|------|------|
| 认领节点 | 已实现 | `"Claim node"` |
| 授权节点 | 已实现 | `"authorize node <64-char-vibe-hash>"` |
| 部署应用 | 已实现 | `"deploy application my-app"` |
| 修补应用 | 已实现 | `"patch app my-app to add logging"` |
| 状态 / 网格 | 已实现 | `"status grid"` |

**Voice Bridge v27.0** 自动获取 `GET /nonce` 并为每条命令签名。手动客户端使用 `voice_bridge_signed.get_signed_payload()`。

---

## 部署选项

| 方式 | 状态 | 平台 |
|------|------|------|
| `python3 utahmosphere_master.py` | **推荐** | 全部 |
| `sudo bash bootstrap.sh` | **推荐生产** | Linux + TPM（可选跳过） |
| `python3 genesis_iso_builder.py` | **已实现** | 生成 `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **已实现** | Genesis ISO 包装脚本 |
| `python3 voice_bridge.py` | **已实现** | 自动 nonce 签名语音客户端 |

---

## 路线图

v26.0 及更早路线图所有项目已在 v27.0 **实现**。

未来增强：

- TPM 引用 attestation 远程验证（RA-TLS）
- 第四内存池区域（大洋洲）
- 声纹与 TPM PCR 硬件绑定

详见 [API 参考](API_REFERENCE.md) 与 [开发者手册](DEVELOPER_COOKBOOK.md)。
