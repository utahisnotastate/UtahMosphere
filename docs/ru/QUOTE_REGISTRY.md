# Реестр аппаратных цитат (v30.0)

**Реестр аппаратных цитат** — распределённый источник истины для действительных отпечатков TPM в рое UtahMosphere. Узлы не доверяют IP-адресам — они доверяют **аппаратным цитатам**, подписанным корневым CA Utah-Kernel и зарегистрированным в этом реестре.

## Топология

```
Node A (claim)                    Swarm peers
    |                                  |
    |-- seal vibe to PCR0 ------------>|
    |-- sign hardware quote ---------->|-- merge_remote()
    |-- register_node() -------------->|-- quote_registry in mesh payload
    |                                  |
Peer B connects via RA-TLS ----------> verify against registry
    |                                  |
UtahX ingress ----------------------> ra_tls_guard.verify_http_headers()
```

## Сервис реестра (`quote_registry.py`)

| Метод | Назначение |
|--------|------------|
| `register_node(hardware_id, public_quote, ...)` | Добавить узел после биометрического claim |
| `is_valid_hardware(hardware_id)` | Проверить активную запись |
| `purge_node(hardware_id, reason)` | Карантин скомпрометированного оборудования |
| `merge_remote(remote_nodes)` | Репликация из mesh gossip |
| `export_nodes()` | Полный снимок реестра |

Хранение: `{UTAH_DATA_DIR}/quote_registry.json`

## RA-TLS Guard (`ra_tls_guard.py`)

**Закрепление CA.** Только узлы с цитатой Utah-Kernel CA из реестра могут войти в mesh или пройти UtahX ingress.

- X.509 OID `1.3.6.1.4.1.99999` — TPM цитата
- HTTP: заголовки `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote`

## Связка биометрии с TPM (claim)

При `"Claim node"`: vibe-print → PCR0 → `hardware_id` → подписанная цитата → `register_node()` → mesh распространяет `quote_registry`.

## HTTP API

См. [Справочник API](API_REFERENCE.md): `GET /registry/quotes`, `POST /registry/purge`.

## Переменные окружения

| Переменная | По умолчанию | Назначение |
|------------|--------------|------------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Персистентность |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress + CA (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v30_root_ca` | Корень подписи |

Dev:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## См. также

- [Матрица возможностей](CAPABILITY_MATRIX.md)
- [Справочник API](API_REFERENCE.md)
