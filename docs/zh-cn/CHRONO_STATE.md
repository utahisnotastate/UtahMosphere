# Chrono-State 执行 (v34.0)

**Chrono-State** 使 CI/CD 预发布环境过时。在 Lazarus 注入 AI 代码前，引擎对模块内存做快照。若变异失败，时间回滚——通常在 HTTP 超时之前。

## 模块 (`chrono_state.py`)

| 方法 | 用途 |
|------|------|
| `execute_with_rewind()` | 推测执行 + 失败回滚 |
| `snapshot_namespace()` | 深拷贝模块 dict |
| `rewind_namespace()` | 恢复变异前状态 |

## HTTP API

### GET /chrono/status

```bash
curl http://127.0.0.1:8999/chrono/status
```

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_CHRONO_ENFORCE` | `1` | 启用 chrono 回滚（`0` = 直接执行） |

## 相关

- [UtahClaw](UTAH_CLAW.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
