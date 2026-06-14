# UtahMosphere 文档门户

欢迎来到 UtahMosphere OS 文档中心。**Migration Ready v25.1**：统一裸机内核，内存池 Tycoon 结算、AuthGuard `authorized_nodes[]` 强制执行、Genesis ISO 安装器（`mk_iso.sh`），UtahNetes 与 Global Swarm 已全面就绪。内容按**受众角色**、**实操教程**、**可复制配方**和**入门项目**组织。

---

## 从这里开始

| 文档 | 最适合 |
|------|--------|
| [能力矩阵](CAPABILITY_MATRIX.md) | 所有人 — 当前可用功能与路线图 |
| [API 参考](API_REFERENCE.md) | 开发者与运维人员 |
| [本地开发指南](LOCAL_DEVELOPMENT.md) | 在 Windows、macOS 或 Linux 上开发的开发者 |

---

## 角色指南（概览）

| 角色 | 概览文档 | 教程 | 配方 |
|------|----------|------|------|
| **儿童与家庭** | [儿童通俗讲解](ELI5_FOR_KIDS.md) | [教程：你的第一个机器人管家](tutorials/01-kids-first-robot-butler.md) | [配方索引](recipes/README.md) |
| **高管（CEO/CTO）** | [高管摘要](EXECUTIVE_SUMMARY.md) | — | [配方索引](recipes/README.md) |
| **架构师** | [技术深度解析](TECHNICAL_DEEP_DIVE.md) | — | [配方索引](recipes/README.md) |
| **开发者** | [开发者手册](DEVELOPER_COOKBOOK.md) | [教程：你的第一个应用](tutorials/05-developer-first-app.md) | [配方索引](recipes/README.md) |
| **非技术用户** | [非技术指南](NON_TECHNICAL_GUIDE.md) | [教程：无术语配置](tutorials/06-non-technical-setup.md) | [配方索引](recipes/README.md) |

---

## 教程（分步操作）

1. [你的第一个机器人管家](tutorials/01-kids-first-robot-butler.md) — 儿童与家庭
2. [你的第一个应用](tutorials/05-developer-first-app.md) — 开发者端到端流程
3. [无术语配置](tutorials/06-non-technical-setup.md) — 非技术用户入门

---

## 配方（可复制代码）

- [配方索引](recipes/README.md) — 所有配方的总目录

---

## 模板与入门项目

### 模板（`templates/`）

可复用的样板代码，可复制到你自己的项目中：

| 模板 | 用途 |
|------|------|
| [python-http-service](../../templates/python-http-service/) | 独立 HTTP 微服务 |
| [container-handler](../../templates/container-handler/) | UtahContainerEngine `handler.py` |
| [voice-command-client](../../templates/voice-command-client/) | 程序化 `/command` 客户端 |
| [frontend-upload](../../templates/frontend-upload/) | 浏览器上传客户端 |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | HTTP 402 支付流程 |

### 示例（`examples/`）

可运行的小脚本，用于调用实时 API：

| 示例 | 演示内容 |
|------|----------|
| [hello-world](../../examples/hello-world/) | 通过 `/command` 部署应用 |
| [check-node-health](../../examples/check-node-health/) | 健康与状态探测 |
| [paid-app-access](../../examples/paid-app-access/) | Tycoon 内存池/electrum 结算 |
| [omega-build-verify](../../examples/omega-build-verify/) | 完整 S3/Lambda/RDS/容器 parity 测试 |
| [voice-deploy-simulator](../../examples/voice-deploy-simulator/) | 无需麦克风即可部署 |

### 入门项目（`starter-projects/`）

可 fork 并扩展的完整迷你项目：

| 项目 | 说明 |
|------|------|
| [minimal-api](../../starter-projects/minimal-api/) | 最小可部署 API 工作负载 |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | 语音 + 状态仪表板 |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | 付费访问应用模式 |

---

## 关于 UtahMosphere OS

UtahMosphere OS v25.1 Migration Ready 是主权边缘 Python 平台，构建标识 `golden-master-v25.1`，默认 HTTP 入口端口为 **8999**。核心功能：内存池 Tycoon 结算、AuthGuard `authorized_nodes[]` 强制执行、Genesis ISO 安装器（`./mk_iso.sh`）、`authorize node` 语音命令。推荐入口：`utahmosphere_master.py`。
