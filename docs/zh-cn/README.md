# UtahMosphere 文档门户

欢迎来到 UtahMosphere OS 文档中心。**v35.0 Omni-Desk** — 统一裸机主权边缘平台，默认端口 **8999**。v34.0 完成主权信任链：**TPM 声纹锁定**、**网格 RA-TLS attestation**、**四区域内存池故障转移**和**自动语音 nonce 签名** — 从芯片到全球网格。内容按**受众角色**、**实操教程**、**可复制配方**和**入门项目**组织。

---

## 从这里开始

| 文档 | 最适合 |
|------|--------|
| [Omni-Desk](OMNI_DESK.md) | 主权全息桌面 |
| [UtahClaw](UTAH_CLAW.md) | 认识论空白解析器 |
| [Omni-Glass UI](OMNI_GLASS_UI.md) | 实时智能体可视化遥测 |
| [Chrono-State](CHRONO_STATE.md) | 实时变异回滚 |
| [Kinematic Siphon](KINEMATIC_SIPHON.md) | Ghost Tune GPU 客户端 |
| [仲裁见证节点](QUORUM_WITNESSES.md) | 多区域 ISP 中断决胜仲裁 |
| [Lazarus 自动恢复](LAZARUS_RESTORE.md) | 洁净室 Golden Master 恢复 |
| [状态差分引擎](STATE_DIFF_ENGINE.md) | 纠缠态 <1KB mesh 同步 |
| [能力矩阵](CAPABILITY_MATRIX.md) | 所有人 — v35.0 Omni-Desk 与未来工作 |
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

## v35.0 Omni-Desk 功能

- **TPM Locker：** 通过 `tpm2_create` / `tpm2_unseal` 将声纹密封至 PCR0（`tpm_lock.py`）
- **RA-TLS：** 网格 gossip 上的 TPM 引用；同步前验证对等节点（`ra_tls_attest.py`）
- **内存池故障转移：** 美 / 欧 / 全球 / 大洋洲四区域故障转移（`tycoon_failover.py`）
- **硬件 attestation：** bootstrap 中的 TPM 2.0 PCR0 关卡（`attestation_guard.py`）
- **签名语音桥：** 自动 `GET /nonce` + HMAC（`voice_bridge_signed.py`）
- **UtahX / ContainerEngine / S3 / Lambda / RDS：** 完整云 parity
- **AuthGuard + Nonce-Guard + Utah-Flux 撤销：** 网格治理
- **Genesis ISO v35：** `utah_genesis_v35.iso`

构建标识 `omega-build-v35-omni-desk`。推荐入口：`python3 utahmosphere_master.py`。
