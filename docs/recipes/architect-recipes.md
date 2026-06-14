# Architect Recipes

Topology, networking, and deployment patterns for platform engineers.

---

## Recipe: Port & Service Map

```yaml
# utahmosphere-ports.yaml
services:
  http_ingress:
    port: 8999
    protocol: tcp
    process: utahmosphere_os.py
  utahnetes_gossip:
    port: 9001
    protocol: udp
    multicast: 239.255.43.21
  global_swarm:
    port: 9055
    protocol: udp
    process: UtahSwarmNode
tenant_ports:
  range_start: 8200
  assignment: 8200 + len(tenants)
```

---

## Recipe: Single-Node Reference Architecture

```
┌─────────────────────────────────────────┐
│           Sovereign Node                │
│  ┌─────────┐  ┌──────────┐  ┌────────┐ │
│  │ :8999   │  │ Quantum  │  │ Tycoon │ │
│  │ Kernel  │──│ Ledger   │  │ Daemon │ │
│  └────┬────┘  └──────────┘  └────────┘ │
│       │                                 │
│  ┌────▼────┐  ┌──────────┐  ┌────────┐ │
│  │ UtahX   │  │ UtahNetes│  │ Swarm  │ │
│  │ manifests│ │ gossip   │  │ :9055  │ │
│  └─────────┘  └──────────┘  └────────┘ │
│       │                                 │
│  containers/{app}/handler.py            │
└─────────────────────────────────────────┘
```

---

## Recipe: Environment Matrix

| Environment | `UTAH_DATA_DIR` | `UTAH_SECRET_VECTOR` | Claim required |
|-------------|-----------------|----------------------|----------------|
| Local dev | `./.utah-data` | `dev-secret` | No (open mode OK) |
| Staging | `/var/lib/utahmosphere` | Random 32-byte hex | Yes |
| Production | `/var/lib/utahmosphere` | Vault-managed | Yes + backup |

---

## Recipe: Multi-Node LAN Gossip

Requirements:

1. Both nodes on same L2/L3 multicast-capable network
2. UDP 9001 open between nodes
3. Unique hostnames (`node_identity`)

Verification:

```bash
# On node A — deploy app
python examples/voice-deploy-simulator/deploy.py shared-app

# On node B — after ~10s gossip interval
curl http://127.0.0.1:8999/status
# Expect shared-app in tenants if epoch synced
```

---

## Recipe: Ingress with Reverse Proxy (Hybrid)

Until UtahX TCP proxy is live, terminate TLS at Caddy:

```
Caddyfile snippet:
utah.example.com {
    reverse_proxy 127.0.0.1:8999
}
```

---

## Recipe: Observability Stack Hook

```bash
# Prometheus blackbox-style probe
curl -sf http://127.0.0.1:8999/health || alert

# JSON metrics scrape (custom exporter pattern)
curl -s http://127.0.0.1:8999/status | jq '{
  workloads: .ui_state.active_workloads,
  claimed: .claimed,
  mutations: .ui_state.mutation_count
}'
```

Tutorial: [Architect Deployment](../tutorials/03-architect-deployment.md)
