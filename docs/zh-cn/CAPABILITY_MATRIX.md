# 能力矩阵

UtahMosphere OS **v26.0 Omega-Build FINAL** — 路线图完整实现。

---

## HTTP API 端点

| 端点 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/health` | GET | **已实现** | 存活探测 + `build: omega-build-v26-final` |
| `/nonce` | GET | **已实现** | 签发新的语音命令 nonce（30 秒窗口） |
| `/status` | GET | **已实现** | UI 状态、租户、认领状态、S3 根 |
| `/command` | POST | **已实现** | 语音意图 + 认领后 nonce 防重放 |
| `/admin/revoke-node` | POST | **已实现** | 根节点专用授权节点撤销 |
| `/app/unlock` | POST | **已实现** | 提交支付；返回 202 待结算 |
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
| **UtahX 代理（`utahx_proxy.py`）** | **已实现** | 实时 HTTP 代理至容器端口 |
| **UtahContainerEngine（`utah_container_runtime.py`）** | **已实现** | 8200+ 租户 HTTP 服务 |
| **Lazarus AST（`utah_lazarus.py`）** | **已实现** | AST 验证 handler 变更 + OTA 通道 |
| **S3 Mesh（`utah_s3_mesh.py`）** | **已实现** | 本地对象存储 + HMAC |
| **Lambda Engine（`utah_lambda_engine.py`）** | **已实现** | 无镜像 handler 调用 |
| **RDS Ledger（`utah_rds_ledger.py`）** | **已实现** | JSON 键值账本 |
| **Quantum Ledger** | **已实现** | 生物识别认领 + 验证 |
| **Utah-Tycoon** | **已实现** | 内存池/electrum 结算（`tycoon_settlement.py`） |
| **AuthGuard（`ledger_auth.py`）** | **已实现** | 语音与网格的 `authorized_nodes[]` 强制执行 |
| **Nonce-Guard（`nonce_guard.py`）** | **已实现** | 语音命令 30 秒防重放 |
| **UtahNetes Gossip** | **已实现** | 经 `utah_mesh_engine.py` AuthGuard 签名 5 秒组播 |
| **Global Swarm** | **已实现** | 确定性 DHT + 签名账本同步 |
| **Genesis ISO（`genesis_iso_builder.py`）** | **已实现** | Alpine vmlinuz/initramfs 混合 ISO |
| **Utah-Flux 撤销 UI（`ui_revocation.py`）** | **已实现** | `flux_gui.py` 中的管理面板 |
| **Utah-Flux UI** | **已实现** | Tkinter 状态 + 撤销仪表板 |
| **Auto-Genesis（`genesis_deploy.py`）** | **已实现** | 多进程编排器 |
| **Bootstrap（`bootstrap.sh`）** | **已实现** | 裸机 systemd 安装 |

---

## 语音命令

| 命令模式 | 状态 | 示例 |
|----------|------|------|
| 认领节点 | 已实现 | `"Claim node"` |
| 授权节点 | **已实现** | `"authorize node <64-char-vibe-hash>"` |
| 部署应用 | 已实现 | `"deploy application my-app"` |
| 修补应用 | **已实现** | `"patch app my-app to add logging"` |
| 状态 / 网格 | 已实现 | `"status grid"` |

**认领后：** 每次 `/command` 请求须包含来自 `GET /nonce` 的 `nonce` + `command_signature`。

---

## 部署选项

| 方式 | 状态 | 平台 |
|------|------|------|
| `python3 utahmosphere_master.py` | **推荐** | 全部 |
| `python3 utahmosphere_os.py` | 已实现 | 全部 |
| `python3 genesis_deploy.py` | 已实现 | Linux / 开发 |
| `sudo bash bootstrap.sh` | **推荐生产** | Linux systemd |
| `sudo bash setup.sh` | 已实现 | bootstrap 别名 |
| `python3 genesis_iso_builder.py` | **已实现** | Linux — 生成 `utah_genesis_v26.iso` |
| `./mk_iso.sh` | **已实现** | Genesis ISO 构建器包装脚本 |
| `docker-compose up` | 可选 | 仅遗留便利方式 |

---

## 路线图

v25.x 路线图所有项目已在 v26.0 **实现**。未来工作：

- Genesis ISO 自动安装硬件 attestation
- 多区域内存池故障转移
- 语音桥接自动 nonce 签名

详见 [API 参考](API_REFERENCE.md) 与 [开发者手册](DEVELOPER_COOKBOOK.md)。
