# 能力矩阵

本矩阵记录 UtahMosphere OS **v25.0** 当前实现的功能，与营销文档描述或未来版本计划中的功能对比。迁移与开发时请据此设定准确预期。

---

## HTTP API 端点

| 端点 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/health` | GET | **已实现** | 节点存活探测 |
| `/status` | GET | **已实现** | UI 状态、租户列表、认领状态 |
| `/command` | POST | **已实现** | 语音意图执行（JSON 请求体） |
| `/app/{name}` | GET | **已实现** | Tycoon 把关的应用访问（付款前返回 402） |
| `/s3/*` | * | 计划中 | 迁移指南中有文档；尚未路由 |
| `/lambda/*/invoke` | POST | 计划中 | 部署时仅创建 handler 桩 |
| `/rds/read/*`、`/rds/write` | * | 计划中 | 注册表存在；HTTP 路由未接通 |

---

## 核心子系统

| 组件 | 状态 | 当前可用功能 |
|------|------|--------------|
| **内核（`utahmosphere_os.py`）** | 已实现 | 注册表、语音意图、UtahX 路由清单、网格 gossip |
| **Quantum Ledger** | 已实现 | 根声纹认领、生物识别哈希验证、认领前开放模式 |
| **Voice Bridge** | 已实现 | Google STT + MFCC 声纹提取 → `/command` |
| **Utah-Tycoon** | 部分 | 发票生成、模拟 60 秒结算、HTTP 402 关卡 |
| **UtahNetes Gossip** | 部分 | 局域网 UDP 组播租户同步 |
| **Global Swarm** | 部分 | UDP 对等表、ping 保活；完整 Kademlia 查找为桩 |
| **Lazarus 守护进程** | 部分 | 向 `handler.py` 追加补丁注释（非完整 AST 重写） |
| **Utah-Flux UI** | 已实现 | 读取 `flux_ui_manifest.json` 的 Tkinter 仪表板 |
| **UtahX 代理** | 部分 | 写入 JSON 路由清单；无实时 TCP 代理进程 |

---

## 语音命令（已授权）

| 命令模式 | 状态 | 示例 |
|----------|------|------|
| 认领节点 | 已实现 | `"Claim node"` |
| 部署应用 | 已实现 | `"deploy application my-app"` |
| 修补应用 | 部分 | `"patch app my-app to add logging"` |
| 状态 / 网格 | 已实现 | `"status grid"` |

---

## 部署选项

| 方式 | 状态 | 平台 |
|------|------|------|
| `python3 utahmosphere_os.py` | 已实现 | 全部（本地设置 `UTAH_DATA_DIR`） |
| `python3 genesis_deploy.py` | 已实现 | Linux 优先；Windows 开发可用 |
| `sudo bash setup.sh` | 已实现 | Linux（systemd 服务） |
| `docker-compose up` | 已实现 | 可选；使用主机网络 |

---

## 安全模型

| 功能 | 状态 | 说明 |
|------|------|------|
| 单一根声纹持有者 | 已实现 | 首位认领的说话者拥有节点 |
| `authorized_nodes[]` 字段 | 桩 | 存储在账本 JSON 中；代码中未强制执行 |
| HMAC 租户签名 | 已文档化 | 提供配方；内核强制执行部分实现 |
| Ed25519 签名 | 计划中 | 文档有引用；未实现 |
| 默认 `UTAH_SECRET_VECTOR` | 已实现 | 生产环境请更改 |

---

## Docker / Nginx 关系

UtahMosphere 的**主要运行时**是裸机 Python。Docker 和 Nginx 是**可选的传统路径**：

- `docker-compose.yaml` — 本地试用的便捷封装
- `nginx.conf` — 参考配置；UtahX JSON 清单是主权路径
- `setup.sh` — 在干净 Linux 安装中清除 Docker/Nginx（生产主权节点）

混合环境中，迁移期间可与 UtahMosphere 并存 Docker/Nginx。

---

## 路线图（尚未实现）

- S3 兼容对象存储 HTTP API
- Lambda 风格 invoke HTTP API
- RDS 账本读/写 HTTP API
- 基于 Git 的部署语音命令
- 通过 Lazarus 完整 AST 变更
- Tycoon 中真实的 Bitcoin 内存池集成

版本历史见项目根目录变更记录。
