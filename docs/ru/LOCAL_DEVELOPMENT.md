# Руководство по локальной разработке

Запуск UtahMosphere на Windows, macOS или Linux без привилегий root и без путей `/var/lib`.

---

## Предварительные требования

- Python 3.11+
- `pip install -r requirements.txt`

**Только Voice Bridge (опционально):**

- Микрофон + `pyaudio` (на Windows может быть сложно — используйте готовые wheels)
- Доступ в интернет для Google Speech Recognition

---

## Быстрый локальный старт

### 1. Укажите локальный каталог данных

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

### 2. Запустите ядро

```bash
python utahmosphere_os.py
```

Проверка:

```bash
curl http://127.0.0.1:8999/health
```

### 3. Развёртывание без микрофона

```bash
python examples/voice-deploy-simulator/deploy.py hello
```

Или напрямую через curl (открытый режим до claim):

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript":"deploy application hello","acoustic_hash":"0"}'
```

### 4. Опционально: Voice Bridge

Во втором терминале (ядро должно быть запущено):

```bash
python voice_bridge.py
```

Скажите: **"Claim node"**, затем **"deploy application my-app"**.

### 5. Опционально: интерфейс Utah-Flux

```bash
python flux_gui.py
```

Требуется дисплей (Tkinter). В headless-средах пропускается корректно.

---

## Структура каталогов (локально)

Когда `UTAH_DATA_DIR` установлен в `./.utah-data`:

```
.utah-data/
├── secure_registry.json
├── flux_ui_manifest.json
├── containers/
│   └── hello/
│       └── handler.py
└── utahx_mesh/
    └── hello.utahx.json

security/biometric_ledger.json   # локальный fallback
tycoon/settlement_ledger.json    # локальный fallback
```

Добавьте `.utah-data/`, `security/`, `tycoon/` и `swarm/` в `.gitignore` (уже учтено).

---

## Заметки для Windows

- Запускайте PowerShell от администратора только при привязке привилегированных портов (для 8999 не нужно).
- `genesis_deploy.py` работает без root на Windows (`os.name == 'nt'`).
- `setup.sh` только для Linux; на Windows используйте шаги локальной разработки выше.
- При проблемах с `pyaudio`: `pip install pipwin && pipwin install pyaudio` или используйте WSL.

---

## Заметки для macOS

```bash
brew install portaudio
pip install pyaudio
```

---

## Docker (все платформы)

```bash
docker-compose up
```

Используется host networking — в Docker Desktop для Windows/Mac порт 8999 маппится на localhost.

---

## Запуск примеров

```bash
python examples/check-node-health/health_check.py
python examples/paid-app-access/access_app.py hello
```

---

## Настройка IDE

Рекомендуемые переменные окружения в конфигурации запуска IDE:

| Переменная | Значение |
|----------|-------|
| `UTAH_DATA_DIR` | `${workspaceFolder}/.utah-data` |
| `UTAH_SECRET_VECTOR` | `local-dev-secret` |

Точка входа для отладки: `utahmosphere_os.py`

---

## Следующие шаги

- [Учебник: Ваше первое приложение](tutorials/05-developer-first-app.md)
- [Справочник API](API_REFERENCE.md)
- [Шаблоны](../../templates/) и [Стартовые проекты](../../starter-projects/)
