# Access Control Model

UtahMosphere OS does **not** implement traditional multi-user RBAC (no admin/user/guest roles in code). Instead, it uses a **sovereign node ownership** model with tenant isolation and optional payment gates.

---

## Identity Concepts

### 1. Node Owner (Root Vibe Holder)

- The **first person** to say `"Claim node"` anchors their acoustic vibe-print hash to the hardware.
- Stored in `biometric_ledger.json` as `root_vibe_hash`.
- All subsequent `/command` requests must present a matching `acoustic_hash`.
- Before claim, the node runs in **open mode** — any acoustic hash is accepted.

### 2. Authorized Entity

Any voice/command payload where `acoustic_hash` matches `root_vibe_hash` (constant-time HMAC compare).

### 3. Tenant

A deployed application registered in `cluster_registry["tenants"]`. Each tenant gets:

- A workspace port (starting at `8200 + tenant count`)
- A UtahX route manifest in `utahx_mesh/{app}.utahx.json`
- A `handler.py` in `containers/{app}/`

### 4. Client (HTTP)

Identified by `X-Client-ID` header or source IP when accessing `/app/{name}`.

### 5. Paid Client

A client with a **settled** Tycoon invoice for the target app. Until paid, requests receive HTTP `402`.

---

## Security Flow

```
Voice Bridge / API Client
        │
        ▼
  POST /command
        │
        ├─ "claim node" → anchor root_vibe_hash
        │
        ├─ verify acoustic_hash == root_vibe_hash
        │     └─ mismatch → "SECURITY LOCKDOWN"
        │
        └─ authorized → deploy / patch / status

HTTP Client
        │
        ▼
  GET /app/{name}
        │
        ├─ tycoon check_access_authorization
        │     └─ unpaid → 402 + invoice
        │
        └─ paid → 200 unlocked
```

---

## HMAC Tenant Isolation

For future S3/RDS APIs, tenant requests will use:

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

## `authorized_nodes[]` (Future)

The ledger stores `authorized_nodes` as an array but it is **not read or enforced** in v25.0. Planned use: delegate voice authority to additional vibe-print hashes without transferring root ownership.

---

## Threat Model Summary

| Risk | Mitigation today | Gap |
|------|------------------|-----|
| Unauthorized voice commands | Vibe-print after claim | Open mode before claim |
| Replay of voice payloads | None | Add nonce/timestamp |
| Default HMAC secret | Env var override | Must change in prod |
| Multi-user admin | Single owner only | `authorized_nodes` not wired |
| Payment bypass | Simulated settlement | Not real Bitcoin verification |

See [Operations Runbook](OPERATIONS_RUNBOOK.md) for incident response steps.
