# Lazarus 内核自动恢复 (v32.0)

当 **PCR 漂移检测** 触发隔离（v31.0）时，**Lazarus 守护进程** 自动执行 **洁净室恢复**：从 DHT 共识获取已验证的 Golden Master，重新注入内核状态并恢复计算。

## 流程

```
PCR drift detected
  --> emergency_quarantine() (stop containers)
  --> perform_rollback() (kexec attempt)
  --> LazarusRestore.auto_restore()
        1. Fetch golden_master from checkpoint / DHT
        2. kexec -l /boot/vmlinuz-verified
        3. apply_state() — re-inject registry + quorum
        3. Resume compute
```

## 模块 (`lazarus_restore.py`)

| 方法 | 用途 |
|------|------|
| `auto_restore(kernel_ref)` | 完整洁净室恢复 |
| `get_golden_master(kernel_ref)` | 从检查点或 DHT 加载 |
| `apply_state(kernel_ref, golden)` | 原子化状态重实例化 |
| `save_checkpoint(kernel_ref)` | 将黄金状态持久化到磁盘 |
| `schedule_auto_restore(kernel_ref)` | 隔离后异步恢复 |

检查点：`{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json`

## HTTP API

### GET /lazarus/status

### POST /lazarus/restore

```bash
curl -X POST http://127.0.0.1:8999/lazarus/restore
```

## 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `UTAH_LAZARUS_AUTO_RESTORE` | `1` | Golden Master + kexec 原子恢复（`0` = 开发） |
| `UTAH_LAZARUS_KEXEC_ENFORCE` | `1` | 恢复时 kexec（`0` = 开发） |
| `UTAH_LAZARUS_KEXEC_KERNEL` | `/boot/vmlinuz-verified` | 已验证恢复内核 |
| `UTAH_LAZARUS_KEXEC_INITRD` | `/boot/initramfs-verified` | 已验证 initramfs |
| `UTAH_LAZARUS_CHECKPOINT_PATH` | `{UTAH_DATA_DIR}/lazarus_golden_checkpoint.json` | Golden Master 检查点 |

## 相关文档

- [PCR 漂移检测](PCR_DRIFT.md)
- [DHT 联邦](DHT_FEDERATION.md)
