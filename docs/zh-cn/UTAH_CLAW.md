# UtahClaw 环境运行器 (v34.0)

**UtahClaw** 是 UtahMosphere 的编译潜意识——非阻塞环境守护进程，当 Omni-Compiler 遇到未知能力（如 Stripe GraphQL、Twilio）时填补**认识论空白**。

## 拓扑

```
未解析意图 → EpistemicVoid
        |
        v
[UtahClaw 环境运行器]
   /        |        \
Web/DHT   全息记忆     沙箱
抓取器                 编译器
        |
[MCP 工具锻造 → Lazarus 热注入]
```

## 模块 (`utahclaw/`)

| 模块 | 用途 |
|------|------|
| `ambient_runner.py` | 异步空白研究 + MCP 工具锻造 |
| `holographic_memory.py` | 叠加概念干涉模式 |
| `epistemic_void.py` | `EpistemicVoid` 异常 + 空白检测 |
| `kinematic_siphon.py` | Ghost Tune B-Web 二进制编码 |
| `service.py` | 端口 **9090** 上的快速套接字 HTTP |

## HTTP API

### POST /claw/void（内核端口 8999）

```bash
curl -X POST http://127.0.0.1:8999/claw/void \
  -H "Content-Type: application/json" \
  -d '{"concept": "Integrate with Stripe GraphQL API"}'
```

### GET /claw/status

待处理研究、已锻造工具、全息记忆统计。

## Omni-Compiler 集成

当意图匹配空白关键词（`stripe`、`graphql`、`twilio`）时，`omni_compiler.py` 委派给 UtahClaw。

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_CLAW_ENFORCE` | `1` | 启用运行器（`0` = 开发） |
| `UTAH_CLAW_PORT` | `9090` | UtahClaw 快速套接字 |
| `UTAH_CLAW_TOOLS_DIR` | `{UTAH_DATA_DIR}/mcp_tools` | 锻造的 MCP 工具 |

## 相关

- [Omni-Glass UI](OMNI_GLASS_UI.md)
- [Chrono-State](CHRONO_STATE.md)
- [Omni-Compiler](../OMNI_COMPILER.md)
