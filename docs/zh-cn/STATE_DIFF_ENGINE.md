# 纠缠态差分引擎 (v32.0)

**纠缠态同步** 仅传输注册表状态的*数学差分*——使全球节点以 **<1KB 开销** 达到一致状态，而非传输完整注册表载荷。

## 模块 (`state_diff_engine.py`)

```python
delta = get_state_delta(local_state, remote_state)
merged = apply_state_delta(remote_state, delta)
```

| 函数 | 用途 |
|------|------|
| `get_state_delta(local, remote)` | 最小键级差分 |
| `apply_state_delta(base, delta)` | 重建同步状态 |
| `encode_delta(local, remote)` | 打包差分与哈希供 mesh 使用 |
| `state_hash(state)` | SHA-256 规范状态指纹 |
| `should_use_delta(local, remote)` | 差分小于完整 JSON 时使用差分 |

## Mesh 集成

UtahNetes gossip 在带宽更高效时发送 `registry_delta` 而非完整 `registry`。见证节点在合并前验证 `state_hash`。

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_STATE_DIFF_ENFORCE` | `1` | 更小时优先差分同步 |
| `UTAH_STATE_DIFF_MAX_BYTES` | `1024` | 差分载荷最大字节数 |

## 相关文档

- [仲裁见证节点](QUORUM_WITNESSES.md)
- [Lazarus 自动恢复](LAZARUS_RESTORE.md)
