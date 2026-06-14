# Operations Runbook

Procedures for deploying, monitoring, backing up, and recovering UtahMosphere OS nodes.

---

## Production Deployment (Linux)

```bash
sudo bash setup.sh
```

This:

1. Installs Python dependencies
2. Creates `/var/lib/utahmosphere` data paths
3. Installs scripts to `/usr/local/bin/`
4. Enables `utahmosphere.service` (systemd)

**Manual start (without systemd):**

```bash
sudo UTAH_SECRET_VECTOR="$(openssl rand -hex 32)" python3 genesis_deploy.py
```

---

## Service Management

```bash
sudo systemctl status utahmosphere
sudo systemctl restart utahmosphere
sudo journalctl -u utahmosphere -f
```

---

## Health Monitoring

| Check | Command | Expected |
|-------|---------|----------|
| Liveness | `curl -sf http://127.0.0.1:8999/health` | `"status":"healthy"` |
| Workloads | `curl -s http://127.0.0.1:8999/status \| jq .tenants` | Array of app names |
| Claim status | `curl -s http://127.0.0.1:8999/status \| jq .claimed` | `true` after voice claim |

---

## Backup

Critical files to back up daily:

| Path | Contents |
|------|----------|
| `/var/lib/utahmosphere/secure_registry.json` | Tenants, routes |
| `/etc/utahmosphere/security/biometric_ledger.json` | Root vibe hash |
| `/var/lib/utahmosphere/tycoon/settlement_ledger.json` | Payment state |
| `/var/lib/utahmosphere/containers/` | App handler code |

```bash
tar czf utah-backup-$(date +%Y%m%d).tar.gz \
  /var/lib/utahmosphere/secure_registry.json \
  /var/lib/utahmosphere/containers \
  /etc/utahmosphere/security/biometric_ledger.json \
  /var/lib/utahmosphere/tycoon/settlement_ledger.json
```

---

## Recovery

### Registry corruption

1. Stop the service: `sudo systemctl stop utahmosphere`
2. Restore `secure_registry.json` from backup
3. Restart: `sudo systemctl start utahmosphere`

### Lost biometric ledger

1. Delete or rename `biometric_ledger.json`
2. Restart kernel — node enters **open mode**
3. Re-run Voice Bridge and say **"Claim node"**
4. Re-deploy applications

### Port conflicts

| Port | Service | Fix |
|------|---------|-----|
| 8999 | HTTP kernel | `ss -tlnp \| grep 8999` — stop conflicting process |
| 9001 | UtahNetes gossip | Ensure single kernel instance |
| 9055 | Swarm UDP | Firewall: allow UDP 9055 for mesh peers |

---

## Security Hardening

```bash
# Strong HMAC secret
export UTAH_SECRET_VECTOR="$(openssl rand -hex 32)"

# Restrict ingress (example: UFW)
sudo ufw allow 8999/tcp
sudo ufw allow 9001/udp
sudo ufw allow 9055/udp
```

Claim the node immediately after provisioning. See [Access Control](ACCESS_CONTROL.md).

---

## Troubleshooting

### Voice Bridge: microphone not found

- Install `portaudio` / `pyaudio`
- Check `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`

### SECURITY LOCKDOWN after claim

- `acoustic_hash` must match anchored root vibe
- Re-claim only by resetting `biometric_ledger.json` (see Recovery)

### HTTP 402 on `/app/{name}`

- Expected until Tycoon invoice settles (~60s simulation)
- Use `X-Client-ID` consistently across requests
- Check `tycoon/settlement_ledger.json` for invoice status

### Utah-Flux GUI not showing

- Headless server: expected — use `curl /status` instead
- Check `flux_ui_manifest.json` exists in `UTAH_DATA_DIR`

### Docker janitor errors

The kernel's predictive janitor calls `docker system prune` if Docker is installed. Harmless if Docker is absent.

---

## Logs

| Source | Location |
|--------|----------|
| systemd | `journalctl -u utahmosphere` |
| Kernel stdout | Terminal if run manually |
| Tycoon | Console: `[Tycoon]` prefixed lines |
| Swarm | Console: `[Swarm Engine]` prefixed lines |

---

## Related Docs

- [Ops Recipes](recipes/ops-recipes.md)
- [Local Development](LOCAL_DEVELOPMENT.md)
- [API Reference](API_REFERENCE.md)
