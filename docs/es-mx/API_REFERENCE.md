# Referencia de API

URL base (predeterminada): `http://127.0.0.1:8999`

Todas las respuestas son JSON salvo que se indique lo contrario.

---

## GET /health

Sonda de disponibilidad para balanceadores de carga y monitoreo.

**Respuesta `200`:**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "25.1",
  "build": "golden-master-v25.1"
}
```

**Ejemplo:**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /status

Instantánea operativa: estado de la UI, inquilinos desplegados y si el nodo ha sido reclamado.

**Respuesta `200`:**

```json
{
  "ui_state": {
    "node_status": "Active [Sovereign Core v25.0]",
    "active_workloads": 1,
    "last_voice_command": "deploy application my-app",
    "cluster_health": "Resilient",
    "mutation_count": 0
  },
  "tenants": ["my-app"],
  "claimed": true,
  "authorized_nodes": ["abc123..."],
  "swarm_peers": 2,
  "tycoon": {
    "pending": 0,
    "settled_invoices": 1,
    "swept_funds": 5000,
    "settlement_mode": "auto",
    "mempool_api": "https://mempool.space/api"
  }
}
```

---

## POST /command

Ejecuta una intención de voz de forma programática. Mismo payload que envía Voice Bridge.

**Cuerpo de la solicitud:**

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `transcript` | string | Sí | Comando hablado (sin distinción de mayúsculas) |
| `acoustic_hash` | string | Sí | Hash vibe-print SHA-256 de 64 caracteres |
| `request_signature` | string | No | HMAC AuthGuard opcional para nodos delegados |

**Respuesta `200`:**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Transcripciones soportadas

| Intención | Ejemplo de transcripción |
|-----------|--------------------------|
| Reclamar nodo | `"Claim node"` |
| Autorizar nodo | `"authorize node <64-char-vibe-hash>"` |
| Desplegar app | `"deploy application hello"` o `"manifest app hello"` |
| Parchear app | `"patch app hello to add feature x"` |
| Estado | `"status grid"` |

**Reclamar nodo (primera ejecución):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Desplegar app (modo abierto — antes del claim, cualquier hash aceptado):**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**Después del claim:** `acoustic_hash` debe coincidir con el hash vibe raíz anclado **o** con una entrada en `authorized_nodes[]`, o el kernel devuelve:

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Accede a una aplicación de inquilino desplegada. Protegida por autorización de pago Utah-Tycoon.

**Encabezados:**

| Encabezado | Descripción |
|------------|-------------|
| `X-Client-ID` | Identificador de cliente opcional (predeterminado: IP del cliente) |

### Cliente sin pago — Respuesta `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Las facturas se liquidan automáticamente después de ~60 segundos en la simulación actual.

### Cliente con pago — Respuesta `200`

UtahX reenvía la solicitud al backend UtahContainerEngine en el puerto del inquilino. El cuerpo de la respuesta es la salida JSON del handler.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## POST /app/unlock

Enviar una solicitud de desbloqueo por pago. Tycoon consulta mempool.space (o electrum-server) para la finalidad del pago. Las direcciones de desarrollo (`bc1q_utah_*`) usan liquidación temporizada en modo `auto`.

**Cuerpo de la solicitud:**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**Respuesta `202`:**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

Tras la liquidación, `GET /app/{app_name}` con el mismo `X-Client-ID` reenvía al contenedor.

---

## Respuestas de error

| Código | Cuándo |
|--------|--------|
| `404` | Ruta desconocida |
| `402` | La app existe pero el cliente no ha pagado la factura Tycoon |

---

## Puertos y multidifusión

| Servicio | Puerto / Dirección |
|----------|-------------------|
| Ingreso HTTP | `8999` |
| Gossip UtahNetes | UDP `9001`, multidifusión `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Archivos de datos

| Archivo | Propósito |
|---------|-----------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Inquilinos, rutas UtahX, índice de almacenamiento |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | Estado de la UI Utah-Flux |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Stub de handler desplegado |
| `security/biometric_ledger.json` | Hash vibe raíz (respaldo local si `/etc` no es escribible) |
| `tycoon/settlement_ledger.json` | Estado de facturas y pagos |

`UTAH_DATA_DIR` predeterminado: `/var/lib/utahmosphere` (recurre a directorios locales en errores de permisos).
