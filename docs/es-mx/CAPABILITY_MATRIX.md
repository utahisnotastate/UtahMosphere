# Matriz de capacidades

UtahMosphere OS **v26.0 Omega-Build FINAL** — implementación completa de la hoja de ruta.

---

## Endpoints HTTP de la API

| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Implementado** | Sonda de disponibilidad + `build: omega-build-v26-final` |
| `/nonce` | GET | **Implementado** | Emite nonce nuevo para comando de voz (ventana 30 s) |
| `/status` | GET | **Implementado** | Estado UI, inquilinos, claim, raíz S3 |
| `/command` | POST | **Implementado** | Intención de voz + anti-replay nonce si reclamado |
| `/admin/revoke-node` | POST | **Implementado** | Revocación de nodo autorizado (solo raíz) |
| `/app/unlock` | POST | **Implementado** | Enviar pago; devuelve 202 pendiente de liquidación |
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
| **Proxy UtahX (`utahx_proxy.py`)** | **Implementado** | Proxy HTTP en vivo a puertos de contenedor |
| **UtahContainerEngine (`utah_container_runtime.py`)** | **Implementado** | Servidores HTTP por inquilino en 8200+ |
| **Lazarus AST (`utah_lazarus.py`)** | **Implementado** | Mutación de handler validada AST + canal OTA |
| **S3 Mesh (`utah_s3_mesh.py`)** | **Implementado** | Almacenamiento de objetos local + HMAC |
| **Lambda Engine (`utah_lambda_engine.py`)** | **Implementado** | Invocación de handler sin imágenes |
| **RDS Ledger (`utah_rds_ledger.py`)** | **Implementado** | Registro clave-valor JSON |
| **Quantum Ledger** | **Implementado** | Claim biométrico + verificación |
| **Utah-Tycoon** | **Implementado** | Liquidación mempool/electrum (`tycoon_settlement.py`) |
| **AuthGuard (`ledger_auth.py`)** | **Implementado** | Aplicación de `authorized_nodes[]` para voz + malla |
| **Nonce-Guard (`nonce_guard.py`)** | **Implementado** | Anti-replay 30 s para comandos de voz |
| **Gossip UtahNetes** | **Implementado** | Multidifusión 5 s firmada AuthGuard vía `utah_mesh_engine.py` |
| **Global Swarm** | **Implementado** | DHT determinista + sincronización de registro firmada |
| **Genesis ISO (`genesis_iso_builder.py`)** | **Implementado** | ISO híbrida Alpine vmlinuz/initramfs |
| **UI de revocación Utah-Flux (`ui_revocation.py`)** | **Implementado** | Panel admin en `flux_gui.py` |
| **UI Utah-Flux** | **Implementado** | Tablero Tkinter de estado + revocación |
| **Auto-Genesis (`genesis_deploy.py`)** | **Implementado** | Orquestador multiproceso |
| **Bootstrap (`bootstrap.sh`)** | **Implementado** | Instalación bare-metal systemd |

---

## Comandos de voz

| Patrón de comando | Estado | Ejemplo |
|-------------------|--------|---------|
| Reclamar nodo | Implementado | `"Claim node"` |
| Autorizar nodo | **Implementado** | `"authorize node <64-char-vibe-hash>"` |
| Desplegar aplicación | Implementado | `"deploy application my-app"` |
| Parchear aplicación | **Implementado** | `"patch app my-app to add logging"` |
| Estado / grid | Implementado | `"status grid"` |

**Después del claim:** incluir `nonce` + `command_signature` de `GET /nonce` en cada solicitud `/command`.

---

## Opciones de despliegue

| Método | Estado | Plataforma |
|--------|--------|------------|
| `python3 utahmosphere_master.py` | **Recomendado** | Todas |
| `python3 utahmosphere_os.py` | Implementado | Todas |
| `python3 genesis_deploy.py` | Implementado | Linux / dev |
| `sudo bash bootstrap.sh` | **Recomendado prod** | Linux systemd |
| `sudo bash setup.sh` | Implementado | Alias de bootstrap |
| `python3 genesis_iso_builder.py` | **Implementado** | Linux — genera `utah_genesis_v26.iso` |
| `./mk_iso.sh` | **Implementado** | Wrapper para el generador Genesis ISO |
| `docker-compose up` | Opcional | Solo conveniencia heredada |

---

## Hoja de ruta

Todos los elementos de la hoja de ruta v25.x están **implementados** en v26.0. Trabajo futuro:

- Atestación de hardware para autoinstall Genesis ISO
- Conmutación por error mempool multi-región
- Firma automática de nonce en el puente de voz

Consulta la [Referencia de API](API_REFERENCE.md) y el [Recetario del desarrollador](DEVELOPER_COOKBOOK.md) para detalles de implementación actuales.
