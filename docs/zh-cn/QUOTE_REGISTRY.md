# 硬件引用注册表 (v32.0)

**硬件引用注册表**是 UtahMosphere 集群中有效 TPM 硬件指纹的分布式真相源。节点不信任 IP 地址——它们信任由 Utah-Kernel 根 CA 签名并登记在本注册表中的**硬件引用**。

## 拓扑

```
Node A (claim)                    Swarm peers
    |                                  |
    |-- seal vibe to PCR0 ------------>|
    |-- sign hardware quote ---------->|-- merge_remote()
    |-- register_node() -------------->|-- quote_registry in mesh payload
    |                                  |
Peer B connects via RA-TLS ----------> verify against registry
    |                                  |
UtahX ingress ----------------------> ra_tls_guard.verify_http_headers()
```

## 注册服务 (`quote_registry.py`)

| 方法 | 用途 |
|------|------|
| `register_node(hardware_id, public_quote, ...)` | 生物识别 claim 后添加节点 |
| `is_valid_hardware(hardware_id)` | 检查活跃条目 |
| `purge_node(hardware_id, reason)` | 隔离受损硬件 |
| `merge_remote(remote_nodes)` | 从网格 gossip 复制 |
| `export_nodes()` | 完整注册表快照 |

持久化：`{UTAH_DATA_DIR}/quote_registry.json`

## RA-TLS 守卫 (`ra_tls_guard.py`)

**CA 固定**。仅注册表中具有 Utah-Kernel CA 引用的节点可加入网格或通过 UtahX 入口。

- X.509 OID `1.3.6.1.4.1.99999` 承载 TPM 引用
- HTTP：`X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` 在代理前验证

## 生物识别与 TPM 绑定（claim）

`"Claim node"` 时：声纹 → PCR0 → `hardware_id` → 签名引用 → `register_node()` → 网格传播 `quote_registry`。

## HTTP API

见 [API 参考](API_REFERENCE.md)：`GET /registry/quotes`、`POST /registry/purge`。

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | 注册表持久化 |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX 入口 + CA（`0` = 开发） |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v32_root_ca` | 引用签名根 |

开发环境：

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## 相关

- [能力矩阵](CAPABILITY_MATRIX.md)
- [API 参考](API_REFERENCE.md)
