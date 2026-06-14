# 本地开发指南

在 Windows、macOS 或 Linux 上运行 UtahMosphere，无需 root 权限或 `/var/lib` 路径。

---

## 前置条件

- Python 3.11+
- `pip install -r requirements.txt`

**仅 Voice Bridge（可选）：**

- 麦克风 + `pyaudio`（Windows 上可能较棘手 — 使用预编译 wheel）
- 互联网访问（用于 Google Speech Recognition）

---

## 快速本地启动

### 1. 设置本地数据目录

```powershell
# Windows PowerShell
$env:UTAH_DATA_DIR = "$PWD\.utah-data"
$env:UTAH_SECRET_VECTOR = "dev-only-change-me"
```

```bash
# macOS / Linux
export UTAH_DATA_DIR="$(pwd)/.utah-data"
export UTAH_SECRET_VECTOR="dev-only-change-me"
```

### 2. 启动内核

```bash
python utahmosphere_os.py
```

验证：

```bash
curl http://127.0.0.1:8999/health
```

### 3. 无需麦克风即可部署

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

或直接使用 curl（认领前为开放模式）：

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. 可选：Voice Bridge

在第二个终端中（内核必须正在运行）：

```bash
python voice_bridge.py
```

说：**"Claim node"**，然后说 **"deploy application my-app"**。

### 5. 可选：Utah-Flux 界面

```bash
python flux_gui.py
```

需要显示器（Tkinter）。在无头环境中会优雅跳过。

---

## 目录结构（本地）

当 `UTAH_DATA_DIR` 设置为 `./.utah-data` 时：

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # 本地回退
tycoon/settlement_ledger.json    # 本地回退
```

将 `.utah-data/`、`security/`、`tycoon/` 和 `swarm/` 加入 `.gitignore`（已涵盖）。

---

## Windows 说明

- 仅在绑定特权端口时需要以管理员身份运行 PowerShell（8999 不需要）。
- `genesis_deploy.py` 在 Windows 上无需 root（`os.name == 'nt'`）。
- `setup.sh` 仅适用于 Linux；在 Windows 上使用上述本地开发步骤。
- 若 `pyaudio` 有问题：`pip install pipwin && pipwin install pyaudio`，或使用 WSL。

---

## macOS 说明

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker（全平台）

```bash
docker-compose up
```

使用主机网络 — 在 Windows/Mac 的 Docker Desktop 上，端口 8999 映射到 localhost。

---

## 运行示例

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## IDE 配置

建议在 IDE 运行配置中设置以下环境变量：

| 变量 | 值 |
|------|-----|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

调试入口点：`utahmosphere_os.py`

---

## 下一步

- [教程：你的第一个应用](tutorials/05-developer-first-app.md)
- [API 参考](API_REFERENCE.md)
- [模板](../../templates/) 与 [入门项目](../../starter-projects/)
