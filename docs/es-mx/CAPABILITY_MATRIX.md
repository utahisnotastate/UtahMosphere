# Matriz de capacidades

UtahMosphere OS **v25.1 Migration Ready** — estado de implementación según Omega-Build.

---

## Endpoints HTTP de la API

| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Implementado** | Sonda de disponibilidad + `build: golden-master-v25.1` |
| `/status` | GET | **Implementado** | Estado UI, inquilinos, claim, raíz S3 |
| `/command` | POST | **Implementado** | Ejecución de intención de voz |
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
| **Quantum Ledger** | Implementado | Claim biométrico + verificación |
| **Utah-Tycoon** | **Implementado** | Liquidación mempool/electrum (`tycoon_settlement.py`), `POST /app/unlock`, puerta HTTP 402 |
| **Gossip UtahNetes** | **Implementado** | Multidifusión 5 s firmada AuthGuard vía `utah_mesh_engine.py` |
| **Global Swarm** | **Implementado** | DHT determinista + sincronización de registro firmada |
| **AuthGuard (`ledger_auth.py`)** | **Implementado** | Aplicación de `authorized_nodes[]` para voz + malla |
| **Genesis ISO (`mk_iso.sh`)** | **Implementado** | Generador de instalador flash UEFI/híbrido |
| **UI Utah-Flux** | Implementado | Tablero Tkinter de estado |
| **Auto-Genesis (`genesis_deploy.py`)** | **Implementado** | Orquestador multiproceso |
| **Bootstrap (`bootstrap.sh`)** | **Implementado** | Instalación bare-metal systemd |

---

## Comandos de voz

| Patrón de comando | Estado | Ejemplo |
|-------------------|--------|---------|
| Reclamar nodo | Implementado | `"Claim node"` |
| Desplegar aplicación | Implementado | `"deploy application my-app"` |
| Parchear aplicación | **Implementado** | `"patch app my-app to add logging"` |
| Autorizar nodo | **Implementado** | `"authorize node <64-char-vibe-hash>"` |
| Estado / grid | Implementado | `"status grid"` |

---

## Opciones de despliegue

| Método | Estado | Plataforma |
|--------|--------|------------|
| `python3 utahmosphere_master.py` | **Recomendado** | Todas |
| `python3 utahmosphere_os.py` | Implementado | Todas |
| `python3 genesis_deploy.py` | Implementado | Linux / dev |
| `sudo bash bootstrap.sh` | **Recomendado prod** | Linux systemd |
| `sudo bash setup.sh` | Implementado | Alias de bootstrap |
| `./mk_iso.sh` | **Implementado** | Linux — genera `utah_genesis_v25.iso` |
| `docker-compose up` | Opcional | Solo conveniencia heredada |

---

## Hoja de ruta (pendiente)

- Empaquetado Alpine/vmlinuz dentro de Genesis ISO (el menú de arranque documenta hoy la ruta de instalación manual)
- Anti-replay nonce/marca de tiempo para comandos de voz
- Interfaz de revocación de `authorized_nodes`

Consulta la [Referencia de API](API_REFERENCE.md) y el [Recetario del desarrollador](DEVELOPER_COOKBOOK.md) para detalles de implementación actuales.
