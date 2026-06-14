# Matriz de capacidades

UtahMosphere OS **v27.0 Production Immutable** — anclas de confianza soberanas completas.

---

## Endpoints HTTP de la API

| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Implementado** | Sonda de disponibilidad + `build: omega-build-v27-production` + `attestation` |
| `/nonce` | GET | **Implementado** | Emite nonce nuevo para comando de voz (ventana 30 s) |
| `/status` | GET | **Implementado** | Estado UI, inquilinos, attestation, estadísticas de failover mempool |
| `/command` | POST | **Implementado** | Intención de voz + firma nonce automática (`voice_bridge_signed.py`) |
| `/admin/revoke-node` | POST | **Implementado** | Revocación de nodo autorizado (solo raíz) |
| `/app/unlock` | POST | **Implementado** | Enviar pago; liquidación con failover mempool |
| `/app/{name}` | GET | **Implementado** | Puerta Tycoon 402 + proxy UtahX al contenedor |
| `/app/{name}/{path}` | GET | **Implementado** | Proxy de subruta al backend del contenedor |
| `/s3/{bucket}/{key}` | GET | **Implementado** | Lectura de objeto (NVMe local) |
| `/s3/{bucket}/{key}` | PUT/POST | **Implementado** | Escritura de objeto; encabezados HMAC opcionales |
| `/s3/{bucket}/{prefix}*` | GET | **Implementado** | Listar objetos |
| `/lambda/{fn}/invoke` | POST | **Implementado** | Invocación de handler serverless |
| `/lambda/{fn}` | GET | **Implementado** | Invocación GET con evento vacío |
| `/rds/write` | POST | **Implementado** | Escritura clave-valor |
| `/rds/read/{key}` | GET | **Implementado** | Lectura clave-valor |

---

## Subsistemas principales

| Componente | Estado | Qué funciona hoy |
|------------|--------|------------------|
| **Golden Master (`utahmosphere_master.py`)** | **Implementado** | Punto de entrada unificado |
| **Kernel (`utahmosphere_os.py`)** | **Implementado** | Multiplexor HTTP completo, registro, malla |
| **Attestation de hardware (`attestation_guard.py`)** | **Implementado** | Puerta PCR0 TPM 2.0 en bootstrap + health |
| **Failover mempool (`tycoon_failover.py`)** | **Implementado** | Failover silencioso mempool US/EU/ASIA |
| **Voice Bridge firmado (`voice_bridge_signed.py`)** | **Implementado** | `GET /nonce` automático + firma HMAC |
| **Proxy UtahX (`utahx_proxy.py`)** | **Implementado** | Proxy HTTP en vivo a puertos de contenedor |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implementado** | Servidores HTTP por inquilino en 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implementado** | Mutación de handler validada AST + OTA |
| **S3 / Lambda / RDS** | **Implementado** | Paridad cloud completa |
| **Quantum Ledger** | **Implementado** | Claim biométrico + verificación |
| **Utah-Tycoon** | **Implementado** | Failover mempool + electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Implementado** | Aplicación de `authorized_nodes[]` |
| **Nonce-Guard (`nonce_guard.py`)** | **Implementado** | Anti-replay 30 s para comandos de voz |
| **UtahNetes + Swarm DHT** | **Implementado** | Gossip firmado + enrutamiento determinista |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Implementado** | Alpine vmlinuz + bootstrap con attestation |
| **UI de revocación Utah-Flux** | **Implementado** | Panel admin en `flux_gui.py` |
| **Auto-Genesis / Bootstrap** | **Implementado** | systemd + puerta de attestation |

---

## Comandos de voz

| Patrón de comando | Estado | Ejemplo |
|-------------------|--------|---------|
| Reclamar nodo | Implementado | `"Claim node"` |
| Autorizar nodo | Implementado | `"authorize node <64-char-vibe-hash>"` |
| Desplegar aplicación | Implementado | `"deploy application my-app"` |
| Parchear aplicación | Implementado | `"patch app my-app to add logging"` |
| Estado / grid | Implementado | `"status grid"` |

**Voice Bridge v27.0** obtiene automáticamente `GET /nonce` y firma cada comando. Los clientes manuales usan `voice_bridge_signed.get_signed_payload()`.

---

## Opciones de despliegue

| Método | Estado | Plataforma |
|--------|--------|------------|
| `python3 utahmosphere_master.py` | **Recomendado** | Todas |
| `sudo bash bootstrap.sh` | **Recomendado prod** | Linux + TPM (omisión opcional) |
| `python3 genesis_iso_builder.py` | **Implementado** | Genera `utah_genesis_v27.iso` |
| `./mk_iso.sh` | **Implementado** | Wrapper Genesis ISO |
| `python3 voice_bridge.py` | **Implementado** | Cliente de voz con nonce automático |

---

## Hoja de ruta

Todos los elementos de la hoja de ruta v26.0 y anteriores están **implementados** en v27.0.

Mejoras futuras:

- Verificación remota de cita de attestation TPM (RA-TLS)
- Cuarta región mempool (Oceanía)
- Vinculación vibe-print al PCR TPM

Consulta la [Referencia de API](API_REFERENCE.md) y el [Recetario del desarrollador](DEVELOPER_COOKBOOK.md) para detalles de implementación actuales.
