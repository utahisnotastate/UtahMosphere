# Omni-Glass UI (v34.0)

**Omni-Glass** 用实时可视化流形替代终端日志和 Datadog——Omni-Mind 思维向量、UtahClaw 研究路径和 Lazarus AST 变异。

## 端点

| 端点 | 端口 | 用途 |
|------|------|------|
| `GET /omni/glass` | 8999 | 事件 + 流形 JSON |
| `GET /manifold` | 9091 | 完整流形 |
| `GET /stream` | 9091 | SSE 流（约 60 FPS） |

```bash
curl http://127.0.0.1:8999/omni/glass
curl -N http://127.0.0.1:9091/stream
```

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_OMNI_GLASS_STREAM` | `1` | 在 9091 启动 SSE 中继 |
| `UTAH_OMNI_GLASS_PORT` | `9091` | FluxRelay 端口 |

## 相关

- [Kinematic Siphon](KINEMATIC_SIPHON.md)
- [UtahClaw](UTAH_CLAW.md)
