# Kinematic Siphon (v34.0)

**Kinematic Siphon** 使 UtahMosphere 客户端无需 Chrome/Electron。内核流式传输 **Ghost Tune**——紧凑的 B-Web 二进制协议，将 Omni-Glass 场景图编码为 GPU 纹理直传。

## HTTP API

### GET /siphon/ghost-tune

```bash
curl http://127.0.0.1:8999/siphon/ghost-tune --output ghost.tune
```

返回 `application/octet-stream`，魔数头为 `UTAH\x01`。

## 相关

- [Omni-Glass UI](OMNI_GLASS_UI.md)
