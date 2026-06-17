# 能力矩阵

UtahMosphere OS **v35.0 Omni-Desk** — 主权信任链已全部完成。

---

## HTTP API 端点

| 端点 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/desk/apps` | GET | **已实现** | Genesis Suite 注册表 |
| `/desk/status` | GET | **已实现** | Omni-Desk 状态 |
| `/desk/ui` | GET | **已实现** | 全息桌面 HTML |
| `/desk/intent` | POST | **已实现** | Genesis 应用意图 |
| `/health` | GET | **已实现** | `build: omega-build-v35-omni-desk` + 完整 attestation 快照 |
| `/attestation/quote` | GET | **已实现** | RA-TLS TPM 引用，用于网格对等节点验证 |
| `/registry/quotes` | GET | **已实现** | 全局硬件引用注册表 |
| `/registry/purge` | POST | **已实现** | 清除受损硬件 |
| `/claw/void` | POST | **已实现** | 认识论空白调度 |
| `/claw/status` | GET | **已实现** | UtahClaw 运行器统计 |
| `/chrono/status` | GET | **已实现** | Chrono-State 状态 |
| `/siphon/ghost-tune` | GET | **已实现** | Ghost Tune 二进制 |
| `/omni/compile` | POST | **已实现** | 智能体意图编译 |
| `/omni/status` | GET | **已实现** | Omni-Mind 统计 |
| `/omni/glass` | GET | **已实现** | 智能体事件日志 |
| `/witness/status` | GET | **已实现** | 多区域见证节点 |
| `/lazarus/status` | GET | **已实现** | Lazarus 检查点 |
| `/lazarus/restore` | POST | **已实现** | Golden Master 恢复 |
| `/quorum/consensus` | GET | **已实现** | 多数仲裁投票账本 |
| `/dht/consensus` | GET | **已实现** | DHT 黄金账本 |
| `/dht/challenge` | POST | **已实现** | 蜂群认证挑战 |
| `/nonce` | GET | **已实现** | 语音命令防重放 nonce |
| `/status` | GET | **已实现** | TPM 锁定、RA-TLS、大洋洲内存池区域 |
| `/command` | POST | **已实现** | 语音 + nonce + TPM 绑定声纹验证 |
| `/admin/revoke-node` | POST | **已实现** | 根节点专用节点撤销 |
| `/app/unlock` | POST | **已实现** | 4 区域内存池故障转移结算 |
| `/app/{name}` | GET | **已实现** | Tycoon 402 + UtahX 代理 |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **已实现** | 完整云 parity |

---

## 核心子系统

| 组件 | 状态 | 当前可用功能 |
|------|------|--------------|
| **TPM Locker（`tpm_lock.py`）** | **已实现** | 通过 `tpm2_create` / `tpm2_unseal` 将声纹密封至 PCR0 |
| **RA-TLS（`ra_tls_attest.py`）** | **已实现** | 网格 gossip 上的 TPM 引用；同步前验证对等节点 |
| **内存池故障转移（`tycoon_failover.py`）** | **已实现** | 美 / 欧 / 全球 / **大洋洲** 四区域故障转移 |
| **硬件 attestation（`attestation_guard.py`）** | **已实现** | bootstrap PCR0 关卡 |
| **签名语音桥** | **已实现** | 自动 nonce + HMAC |
| **AuthGuard + Nonce-Guard** | **已实现** | 网格 + 语音安全 |
| **UtahNetes + Swarm DHT** | **已实现** | RA-TLS + 签名 gossip |
| **Genesis ISO v35** | **已实现** | `utah_genesis_v35.iso` |
| **完整云 parity** | **已实现** | S3、Lambda、RDS、UtahX、容器 |

---

## 部署

| 方式 | 状态 |
|------|------|
| `python3 utahmosphere_master.py` | **推荐** |
| `sudo bash bootstrap.sh` | **生产**（TPM + tpm2-tools） |
| `python3 genesis_iso_builder.py` | **v35 ISO** |

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | 认领时要求 TPM 密封 |
| `UTAH_QUORUM_ENFORCE` | `1` | 多数仲裁 |
| `UTAH_WITNESS_ENFORCE` | `1` | 多区域见证节点 |
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | 自动恢复 |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | Lazarus kexec |
| `UTAH_STATE_DIFF_ENFORCE` | `1` | 纠缠态差分同步 |
| `UTAH_PCR_ROLLBACK_ENFORCE` | `1` | kexec rollback |
| `UTAH_DHT_FEDERATION_ENFORCE` | `1` | DHT golden consensus |
| `UTAH_PCR_DRIFT_ENFORCE` | `1` | PCR drift monitor |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | 网格上要求 RA-TLS 引用 |
| `UTAH_MEMPOOL_NODES` | 4 个默认值 | 覆盖内存池故障转移列表 |

| `UTAH_OMNI_DESK_ENFORCE` | `1` | Omni-Desk |
| `UTAH_CLAW_ENFORCE` | `1` | UtahClaw 环境运行器 |
| `UTAH_CHRONO_ENFORCE` | `1` | Chrono-State 回滚 |
| `UTAH_OMNI_GLASS_STREAM` | `1` | Omni-Glass SSE 流 |
| `UTAH_OMNI_ENFORCE` | `1` | Omni-Compiler |

## 路线图

v28.0 路线图所有项目已在 v34.0 **实现**。

未来：远程 RA-TLS CA 固定、硬件引用注册服务。

详见 [API 参考](API_REFERENCE.md) 与 [开发者手册](DEVELOPER_COOKBOOK.md)。
