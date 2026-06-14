# 教程：你的第一个机器人管家

**受众：** 儿童与家庭  
**时间：** 15 分钟  
**需要：** 已安装 UtahMosphere 的电脑，可选麦克风

---

## 你将构建什么

电脑上一个小小的「机器人管家」，听你说话并在你要求时部署应用。

---

## 步骤 1：认识管家

UtahMosphere 就像在小盒子（迷你电脑或树莓派）里有一个机器人管家。不用付钱给大公司托管你的东西，管家就住在**你的**房间里。

启动管家的大脑：

```bash
python utahmosphere_os.py
```

如果你不在 Linux 上，请大人帮忙把 `UTAH_DATA_DIR` 设为你电脑上的一个文件夹。

---

## 步骤 2：跟管家打招呼

打开第二个窗口并运行：

```bash
python voice_bridge.py
```

当它显示 **"Listening..."** 时，试着说：

> **"Claim node"**

这教会管家识别你的声音。就像给管家一把只有你的声音能用的钥匙。

---

## 步骤 3：建一个柠檬水摊

说：

> **"Deploy application lemonade"**

管家在电脑上创建一个小小的「柠檬水摊」应用。检查是否成功：

```bash
curl http://127.0.0.1:8999/status
```

在 tenants 列表中查找 `"lemonade"`。

---

## 步骤 4：没有麦克风？没问题！

请大人运行这个：

```bash
python examples/voice-deploy-simulator/deploy.py lemonade
```

结果一样 — 管家仍会建好你的摊位。

---

## 步骤 5：看控制屏幕

如果你有屏幕，运行：

```bash
python flux_gui.py
```

你会看到绿色文字显示管家在做什么 — 就像宇宙飞船仪表板！

---

## 你学到了什么

- **Claim node** = 教会管家你的声音
- **Deploy application** = 建造新东西
- 管家会列出它建造的一切

---

## 趣味挑战

1. 部署三个应用：`toys`、`games` 和 `art`
2. 说 **"status grid"** 并阅读管家的报告
3. 画一张机器人管家的图，标注：语音、大脑、应用

更多活动：[配方索引](../recipes/README.md)

家长指南：[儿童通俗讲解](../ELI5_FOR_KIDS.md)
