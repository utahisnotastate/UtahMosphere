# Matriz de capacidades

UtahMosphere OS **v29.0 Remote Attestation Infrastructure** — cadena de confianza soberana completa.

---

## Endpoints HTTP de la API

| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Implementado** | `build: omega-build-v29-remote-attested` + instantánea de attestation completa |
| `/attestation/quote` | GET |
| `/registry/quotes` | GET | **Implemented** | Global hardware quote registry |
| `/registry/purge` | POST | **Implemented** | Purge compromised hardware | **Implementado** | Cita TPM RA-TLS para verificación de pares en la malla |
| `/nonce` | GET | **Implementado** | Nonce anti-replay para comando de voz |
| `/status` | GET | **Implementado** | Bloqueo TPM, RA-TLS, regiones mempool Oceanía |
| `/command` | POST | **Implementado** | Voz + nonce + verificación vibe vinculada al TPM |
| `/admin/revoke-node` | POST | **Implementado** | Revocación de nodo (solo raíz) |
| `/app/unlock` | POST | **Implementado** | Liquidación con failover mempool de 4 regiones |
| `/app/{name}` | GET | **Implementado** | Tycoon 402 + proxy UtahX |
| `/s3/*`, `/lambda/*`, `/rds/*` | * | **Implementado** | Paridad cloud completa |

---

## Subsistemas principales

| Componente | Estado | Qué funciona hoy |
|------------|--------|------------------|
| **TPM Locker (`tpm_lock.py`)** | **Implementado** | Vibe-Print sellado al PCR0 vía `tpm2_create` / `tpm2_unseal` |
| **Quote Registry (`quote_registry.py`)** | **Implemented** | Register, purge, merge hardware quotes |
| **RA-TLS Guard (`ra_tls_guard.py`)** | **Implemented** | CA pinning; UtahX ingress |
| **RA-TLS (`ra_tls_attest.py`)** | **Implementado** | Cita TPM en gossip de malla; verificación de pares antes de sync |
| **Failover mempool (`tycoon_failover.py`)** | **Implementado** | Failover US / EU / global / **Oceanía** en 4 regiones |
| **Attestation de hardware (`attestation_guard.py`)** | **Implementado** | Puerta PCR0 en bootstrap |
| **Voice Bridge firmado** | **Implementado** | Nonce automático + HMAC |
| **AuthGuard + Nonce-Guard** | **Implementado** | Seguridad de malla + voz |
| **UtahNetes + Swarm DHT** | **Implementado** | RA-TLS + gossip firmado |
| **Genesis ISO v29** | **Implementado** | `utah_genesis_v29.iso` |
| **Paridad cloud completa** | **Implementado** | S3, Lambda, RDS, UtahX, contenedores |

---

## Despliegue

| Método | Estado |
|--------|--------|
| `python3 utahmosphere_master.py` | **Recomendado** |
| `sudo bash bootstrap.sh` | **Prod** (TPM + tpm2-tools) |
| `python3 genesis_iso_builder.py` | **ISO v29** |

## Variables de entorno

| Variable | Predeterminado | Propósito |
|----------|----------------|-----------|
| `UTAH_TPM_LOCK_ENFORCE` | `1` | Exigir sellado TPM en el claim |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX ingress CA pinning |
| `UTAH_RA_TLS_ENFORCE` | `1` | Exigir citas RA-TLS en la malla |
| `UTAH_MEMPOOL_NODES` | 4 valores predeterminados | Reemplazar lista de failover mempool |

## Hoja de ruta

Todos los elementos de la hoja de ruta v28.0 están **implementados** en v29.0.

Futuro: fijación de CA RA-TLS remota, servicio de registro de citas de hardware.

Consulta la [Referencia de API](API_REFERENCE.md) y el [Recetario del desarrollador](DEVELOPER_COOKBOOK.md).
