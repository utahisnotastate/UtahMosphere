# 能力矩阵

UtahMosphere OS **v25.0 Golden Master Final** — Omega-Build 实现状态。

---

## HTTP API 端点

| 端点 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/health` | GET | **已实现** | 存活探测 + `build: golden-master-final` |
| `/status` | GET | **已实现** | UI 状态、租户、认领状态、S3 根 |
| `/command` | POST | **已实现** | 语音意图执行 |
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
| **Quantum Ledger** | 已实现 | 生物识别认领 + 验证 |
| **Utah-Tycoon** | **已实现** | 事件驱动结算循环、`POST /app/unlock`、HTTP 402 关卡 |
| **UtahNetes Gossip** | **已实现** | 经 `utah_mesh_engine.py` 5 秒组播同步、`master_registry.json` |
| **Global Swarm** | **已实现** | 确定性 DHT 路由、FIND_NODE、迭代对等查找 |
| **Utah-Flux UI** | 已实现 | Tkinter 状态仪表板 |
| **Auto-Genesis（`genesis_deploy.py`）** | **已实现** | 多进程编排器 |
| **Bootstrap（`bootstrap.sh`）** | **已实现** | 裸机 systemd 安装 |

---

## 语音命令

| 命令模式 | 状态 | 示例 |
|----------|------|------|
| 认领节点 | 已实现 | `"Claim node"` |
| 部署应用 | 已实现 | `"deploy application my-app"` |
| 修补应用 | **已实现** | `"patch app my-app to add logging"` |
| 状态 / 网格 | 已实现 | `"status grid"` |

---

## 部署选项

| 方式 | 状态 | 平台 |
|------|------|------|
| `python3 utahmosphere_master.py` | **推荐** | 全部 |
| `python3 utahmosphere_os.py` | 已实现 | 全部 |
| `python3 genesis_deploy.py` | 已实现 | Linux / 开发 |
| `sudo bash bootstrap.sh` | **推荐生产** | Linux systemd |
| `sudo bash setup.sh` | 已实现 | bootstrap 别名 |
| `docker-compose up` | 可选 | 仅遗留便利方式 |

---

## 路线图（剩余）

- Tycoon 中真实 Bitcoin 内存池集成（结算模拟今日可用）
- `genesis.iso` U 盘安装镜像
- `authorized_nodes[]` 强制执行

详见 [API 参考](API_REFERENCE.md) 与 [开发者手册](DEVELOPER_COOKBOOK.md)。
