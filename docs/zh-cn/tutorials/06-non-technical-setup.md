# 教程：无术语配置

**受众：** 非技术用户、小企业主  
**时间：** 20 分钟（需懂技术的朋友协助）  
**目标：** 运行 UtahMosphere 并部署你的第一个应用

---

## 什么是 UtahMosphere？

把它想象成一台**小型电脑大脑**，在**办公室或家里**运行你的网站或应用 — 不用每月向 Amazon 或 Google 付云账单。

你甚至可以**跟它说话**：「Deploy application my-store」，它就会完成配置。

完整通俗指南：[非技术指南](../NON_TECHNICAL_GUIDE.md)

---

## 你需要什么

| 物品 | 原因 |
|------|------|
| 迷你电脑或树莓派 | 「大脑」硬件 |
| 互联网（用于安装） | 一次性下载软件 |
| 懂技术的朋友（可选） | 运行安装命令 |
| USB 麦克风（可选） | 语音控制 |

---

## 步骤 1：安装大脑

你的朋友在迷你电脑（Linux）上运行**一条命令**：

```bash
sudo bash setup.sh
```

这会自动安装一切。大约需要 10–15 分钟。

**没有 Linux？** 朋友可以用 Docker：

```bash
docker-compose up -d
```

---

## 步骤 2：检查是否正常运行

朋友打开浏览器或终端检查：

```bash
curl http://127.0.0.1:8999/health
```

若看到 `"healthy"` — 大脑已唤醒。

---

## 步骤 3：教会它你的声音（可选）

朋友运行：

```bash
python voice_bridge.py
```

你清晰地说：**"Claim node"**

现在只有你的声音（或授权的朋友）能控制系统。

---

## 步骤 4：上线你的应用

**用语音：** 说 **"Deploy application my-store"**

**不用语音：** 朋友运行：

```bash
python examples/voice-deploy-simulator/deploy.py my-store
```

就这样。没有复杂的服务器设置。

---

## 步骤 5：查看运行中的内容

朋友可以打开绿色仪表板：

```bash
python flux_gui.py
```

或从同一网络的任意电脑检查：

```bash
curl http://YOUR-MINI-PC-IP:8999/status
```

---

## 日常任务（请朋友帮忙）

| 你想… | 说或请朋友… |
|-------|-------------|
| 添加新应用 | "Deploy application [name]" |
| 查看运行内容 | "Status grid" |
| 看仪表板 | 打开 Utah-Flux GUI |
| 修复问题 | 重启：`sudo systemctl restart utahmosphere` |

---

## 「免维护」承诺

UtahMosphere 在后台清理旧资源并自我修复。你配置一次，它会持续运行。

备份与恢复请朋友参考运维最佳实践，并定期备份 `.utah-data/` 目录。

---

## 术语表

| 词 | 简单含义 |
|----|----------|
| **Deploy** | 把应用放到大脑上 |
| **Claim node** | 教会大脑你的声音 |
| **Tenant** | 系统上运行的一个应用 |
| **Healthy** | 大脑工作正常 |

更多帮助：[配方索引](../recipes/README.md)
