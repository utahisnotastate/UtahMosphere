# Access Control Model

UtahMosphere OS does **not** implement traditional multi-user RBAC (no admin/user/guest roles in code). Instead, it uses a **sovereign node ownership** model with tenant isolation, delegated node authority, and optional payment gates.

---

## Identity Concepts

### 1. Node Owner (Root Vibe Holder)

- The **first person** to say `"Claim node"` anchors their acoustic vibe-print hash to the hardware.
- Stored in `biometric_ledger.json` as `root_vibe_hash`.
- All subsequent `/command` requests must present a matching `acoustic_hash` **or** a hash listed in `authorized_nodes[]`.
- Before claim, the node runs in **open mode** — any acoustic hash is accepted.

### 2. Authorized Entity

Any voice/command payload where `acoustic_hash` matches `root_vibe_hash` or an entry in `authorized_nodes[]` (constant-time compare via `ledger_auth.AuthGuard`).

Delegate a node:

```
"authorize node <64-char-vibe-hash>"
```

### 3. Mesh Gossip Signatures (v25.1)

UtahNetes multicast and Swarm DHT payloads include `mesh_signature` and `signer_hash` fields. Unsigned or unauthorized sync messages are rejected when the node is claimed.

### 4. Tenant

A deployed application registered in `cluster_registry["tenants"]`. Each tenant gets:

- A workspace port (starting at `8200 + tenant count`)
- A UtahX route manifest in `utahx_mesh/{app}.utahx.json`
- A `handler.py` in `containers/{app}/`

### 5. Client (HTTP)

Identified by `X-Client-ID` header or source IP when accessing `/app/{name}`.

### 6. Paid Client

A client with a **settled** Tycoon invoice for the target app. Settlement uses real mempool monitoring when `UTAH_TYCOON_SETTLEMENT_MODE=real`.

---

## Security Flow

```
Voice Bridge / API Client
        │
        ▼
  POST /command
        │
        ├─ "claim node" → anchor root_vibe_hash + authorized_nodes[]
        │
        ├─ "authorize node <hash>" → append to authorized_nodes[]
        │
        ├─ optional request_signature → AuthGuard HMAC verify
        │
        ├─ verify acoustic_hash in whitelist
        │     └─ mismatch → "SECURITY LOCKDOWN"
        │
        └─ authorized → deploy / patch / status

UtahNetes Mesh / Swarm DHT
        │
        ├─ verify mesh_signature against authorized_nodes[]
        │     └─ reject → log and drop sync
        │
        └─ authorized → merge tenant registry

HTTP Client
        │
        ▼
  GET /app/{name}
        │
        ├─ tycoon check_access_authorization (mempool or simulate)
        │     └─ unpaid → 402 + invoice
        │
        └─ paid → 200 unlocked
```

---

## HMAC Tenant Isolation

For S3 APIs, tenant requests may use:

```
signature = HMAC-SHA256(UTAH_SECRET_VECTOR, f"{tenant_id}:{path}")
```

**Production checklist:**

1. Set `UTAH_SECRET_VECTOR` to a strong random value (32+ bytes).
2. Never commit secrets to source control.
3. Claim the node immediately after provisioning.
4. Back up `biometric_ledger.json` — losing it requires re-claiming.

```bash
export UTAH_SECRET_VECTOR="$(openssl rand -hex 32)"
```

---

## `authorized_nodes[]` (v25.1 — Enforced)

The ledger stores `authorized_nodes` in `biometric_ledger.json` and mirrors them to `secure_registry.json`. `ledger_auth.AuthGuard` enforces:

- Voice command delegation (non-root vibe hashes)
- UtahNetes mesh gossip participation
- Swarm DHT ledger sync (when `mesh_signature` present)

---

## Tycoon Settlement Modes

| Mode | Behavior |
|------|----------|
| `auto` (default) | Mempool API for real addresses; timed fallback for `bc1q_utah_*` dev addresses |
| `real` | Always query mempool.space / electrum |
| `simulate` | Timed settlement only (local dev) |

## Voice Nonce Anti-Replay (v26.0)

After node claim, every `/command` request requires:

1. `GET /nonce` — receive fresh timestamp nonce
2. Compute `command_signature = HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")`
3. Include `nonce` and `command_signature` in the POST body

Replayed commands fail after 30 seconds or if nonce is reused.

Disable enforcement for testing: `export UTAH_NONCE_ENFORCE=0`

## Utah-Flux Revocation (v26.0)

Run `python flux_gui.py` to open the revocation panel. Set `UTAH_FLUX_ACOUSTIC_HASH` to your root vibe hash, or enter it when prompted. Revoking a node removes it from `authorized_nodes[]` and prunes mesh gossip instantly.

---

## Threat Model Summary

| Risk | Mitigation today | Gap |
|------|------------------|-----|
| Unauthorized voice commands | Vibe-print + authorized_nodes | Open mode before claim |
| Unauthorized mesh sync | AuthGuard mesh signatures | Open mode before claim |
| Replay of voice payloads | Nonce-Guard 30s window | Disable with `UTAH_NONCE_ENFORCE=0` |
| Default HMAC secret | Env var override | Must change in prod |
| Multi-user admin | authorized_nodes + revocation UI | No automated revocation audit log |
| Payment bypass | Mempool / electrum verification | Dev addresses simulate |

See [Operations Runbook](OPERATIONS_RUNBOOK.md) for incident response steps.
