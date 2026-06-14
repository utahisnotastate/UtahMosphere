# 多区域仲裁见证节点 (v32.0)

**见证节点** 是轻量级区域观察者，仅保存蜂群共识的密码学哈希。当某区域（如 US-East）与骨干网失联时，**大洋洲** 与 **欧洲** 的见证节点充当决胜仲裁者——在无中心化控制的情况下维持蜂群完整性。

## 架构

```
US-East Node (partitioned)     Witness Layer
        |                           |
        |-- state_hash ------------>|-- us-east witness
        |                           |-- eu-west witness
        |                           |-- oceania-apac witness
        |<-- quorum confirmed ------|   (>51% must agree)
```

## 模块 (`quorum_witness.py`)

| 方法 | 用途 |
|------|------|
| `get_consensus(proposed_state_hash)` | 需 >50% 见证节点确认哈希 |
| `ping_and_verify(hash)` | 按区域 HTTP 探测见证节点 |
| `record_local_witness(hash)` | 远端不可达时的本地决胜 |
| `export_witnesses()` | 区域见证状态导出 |

默认区域：`us-east`、`eu-west`、`oceania-apac`

## HTTP API

### GET /witness/status

```bash
curl http://127.0.0.1:8999/witness/status
```

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_WITNESS_ENFORCE` | `1` | 强制见证仲裁（`0` = 开发） |
| `UTAH_WITNESS_THRESHOLD` | `0.51` | 最低投票比例 |
| `UTAH_WITNESS_NODES` | 3 个默认 | 逗号分隔的见证端点 |

## 相关文档

- [联邦仲裁共识](QUORUM_CONSENSUS.md)
- [状态差分引擎](STATE_DIFF_ENGINE.md)
