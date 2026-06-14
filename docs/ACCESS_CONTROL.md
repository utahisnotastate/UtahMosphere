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

```bash
export UTAH_TYCOON_SETTLEMENT_MODE=real
export UTAH_MEMPOOL_API=https://mempool.space/api
export UTAH_ELECTRUM_URL=http://127.0.0.1:50001  # optional
```

---

## Threat Model Summary

| Risk | Mitigation today | Gap |
|------|------------------|-----|
| Unauthorized voice commands | Vibe-print + authorized_nodes | Open mode before claim |
| Unauthorized mesh sync | AuthGuard mesh signatures | Open mode before claim |
| Replay of voice payloads | None | Add nonce/timestamp |
| Default HMAC secret | Env var override | Must change in prod |
| Multi-user admin | authorized_nodes delegation | No UI for revocation |
| Payment bypass | Mempool / electrum verification | Dev addresses simulate |

See [Operations Runbook](OPERATIONS_RUNBOOK.md) for incident response steps.
