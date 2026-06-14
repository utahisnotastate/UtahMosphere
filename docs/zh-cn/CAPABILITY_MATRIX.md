# 能力矩阵

UtahMosphere OS **v29.0 Remote Attestation Infrastructure** — 主权信任链已全部完成。

---

## HTTP API 端点

| 端点 | 方法 | 状态 | 说明 |
|------|------|------|------|
| `/health` | GET | **已实现** | `build: omega-build-v29-remote-attested` + 完整 attestation 快照 |
| `/attestation/quote` | GET |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry |
| `/registry/purge` | POST | **Implemented** | Purge compromised hardware | **已实现** | RA-TLS TPM 引用，用于网格对等节点验证 |
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
| **Genesis ISO v29** | **已实现** | `utah_genesis_v29.iso` |
| **完整云 parity** | **已实现** | S3、Lambda、RDS、UtahX、容器 |

---

## 部署

| 方式 | 状态 |
|------|------|
| `python3 utahmosphere_master.py` | **推荐** |
| `sudo bash bootstrap.sh` | **生产**（TPM + tpm2-tools） |
| `python3 genesis_iso_builder.py` | **v29 ISO** |

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | 认领时要求 TPM 密封 |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | 网格上要求 RA-TLS 引用 |
| `UTAH_MEMPOOL_NODES` | 4 个默认值 | 覆盖内存池故障转移列表 |

## 路线图

v28.0 路线图所有项目已在 v29.0 **实现**。

未来：远程 RA-TLS CA 固定、硬件引用注册服务。

详见 [API 参考](API_REFERENCE.md) 与 [开发者手册](DEVELOPER_COOKBOOK.md)。
