# Ops Recipes

System administration, monitoring, backup, and troubleshooting.

---

## Health Monitoring

**Status:** Implemented

```bash
#!/bin/bash
# health-probe.sh
curl -sf http://127.0.0.1:8999/health | jq .
curl -sf http://127.0.0.1:8999/status | jq '{tenants, claimed, workloads: .ui_state.active_workloads}'
```

Example: [examples/check-node-health](../../examples/check-node-health/)

---

## Recipe: systemd Service Check

```bash
sudo systemctl is-active utahmosphere
sudo journalctl -u utahmosphere --since "1 hour ago" | tail -50
```

---

## Recipe: Backup Script

```bash
#!/bin/bash
BACKUP_DIR="/backup/utahmosphere"
DATE=$(date +%Y%m%d)
mkdir -p "$BACKUP_DIR"

tar czf "$BACKUP_DIR/utah-$DATE.tar.gz" \
  /var/lib/utahmosphere/secure_registry.json \
  /var/lib/utahmosphere/containers \
  /etc/utahmosphere/security/biometric_ledger.json \
  /var/lib/utahmosphere/tycoon/settlement_ledger.json 2>/dev/null

echo "Backup: $BACKUP_DIR/utah-$DATE.tar.gz"
```

---

## Recipe: Reset to Open Mode (Emergency)

```bash
sudo systemctl stop utahmosphere
sudo mv /etc/utahmosphere/security/biometric_ledger.json \
        /etc/utahmosphere/security/biometric_ledger.json.bak
sudo systemctl start utahmosphere
curl http://127.0.0.1:8999/status | jq .claimed  # false
```

---

## Recipe: Port Conflict Diagnosis

```bash
# Linux
ss -tlnp | grep 8999
ss -ulnp | grep -E '9001|9055'

# Windows PowerShell
netstat -ano | findstr 8999
```

---

## Recipe: Headless Server (No GUI)

Skip `flux_gui.py`. Monitor via:

```bash
watch -n 5 'curl -s http://127.0.0.1:8999/status | jq .ui_state'
```

Or read manifest file:

```bash
cat /var/lib/utahmosphere/flux_ui_manifest.json
```

---

## Recipe: Docker Compose Ops

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## Recipe: Tycoon Invoice Debug

```bash
cat tycoon/settlement_ledger.json | jq '.invoices'
# or production path:
cat /var/lib/utahmosphere/tycoon/settlement_ledger.json | jq '.invoices'
```

Look for `"status": "settled"` for your `client_id`.

---

## Recipe: Local Dev on Windows

```powershell
$env:UTAH_DATA_DIR = "$PWD\.utah-data"
python utahmosphere_os.py
```

Full guide: [Local Development](../LOCAL_DEVELOPMENT.md)  
Runbook: [Operations Runbook](../OPERATIONS_RUNBOOK.md)
