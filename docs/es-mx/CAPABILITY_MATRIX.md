# Matriz de capacidades

UtahMosphere OS **v25.0 Golden Master Final** — estado de implementación según Omega-Build.

---

## Endpoints HTTP de la API

| Endpoint | Método | Estado | Notas |
|----------|--------|--------|-------|
| `/health` | GET | **Implementado** | Sonda de disponibilidad + `build: golden-master-final` |
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
| **Utah-Tycoon** | **Implementado** | Bucle de liquidación orientado a eventos, `POST /app/unlock`, puerta HTTP 402 |
| **Gossip UtahNetes** | **Implementado** | Sincronización multidifusión 5 s vía `utah_mesh_engine.py`, `master_registry.json` |
| **Global Swarm** | **Implementado** | Enrutamiento DHT determinista, FIND_NODE, búsqueda iterativa de pares |
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
| `docker-compose up` | Opcional | Solo conveniencia heredada |

---

## Hoja de ruta (pendiente)

- Integración real del mempool Bitcoin en Tycoon (la simulación de liquidación funciona hoy)
- Imagen de instalación `genesis.iso` en memoria USB
- Aplicación del campo `authorized_nodes[]`

Consulta la [Referencia de API](API_REFERENCE.md) y el [Recetario del desarrollador](DEVELOPER_COOKBOOK.md) para detalles de implementación actuales.
