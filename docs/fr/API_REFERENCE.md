# Référence API

URL de base (par défaut) : `http://127.0.0.1:8999`

Toutes les réponses sont au format JSON sauf indication contraire.

---

## GET /health

Sonde de disponibilité pour les équilibreurs de charge et la surveillance.

**Réponse `200` :**

```json
{
  "status": "healthy",
  "node": "my-hostname",
  "version": "27.0",
  "build": "omega-build-v27-production",
  "attestation": {
    "tpm_present": true,
    "provisioned": true,
    "sealed": false,
    "enforce": true
  }
}
```

**Exemple :**

```bash
curl http://127.0.0.1:8999/health
```

---

## GET /nonce

Émet un nonce frais pour commande vocale. Requis après revendication du nœud lorsque `UTAH_NONCE_ENFORCE=1` (par défaut).

**Réponse `200` :**

```json
{
  "nonce": 1718323200,
  "window_sec": 30,
  "signature_hint": "HMAC-SHA256(acoustic_hash, f'{nonce}:{transcript}')"
}
```

**Exemple :**

```bash
curl http://127.0.0.1:8999/nonce
```

---

## GET /status

Instantané opérationnel : état de l'interface, locataires déployés et statut de revendication du nœud.

**Réponse `200` :**

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
    "mempool_failover_nodes": [
      "https://mempool.space/api",
      "https://mempool.space/signet/api",
      "https://blockstream.info/api"
    ]
  },
  "attestation": {
    "tpm_present": false,
    "provisioned": false,
    "sealed": false,
    "enforce": true
  }
}
```

---

## POST /command

Exécuter une intention vocale par programmation. Même charge utile que celle envoyée par Voice Bridge.

**Corps de la requête :**

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `transcript` | string | Oui | Commande parlée (insensible à la casse) |
| `acoustic_hash` | string | Oui | Hash vibe-print SHA-256 sur 64 caractères |
| `nonce` | integer | Après revendication | Horodatage émis par le serveur depuis `GET /nonce` |
| `command_signature` | string | Après revendication | `HMAC-SHA256(acoustic_hash, f"{nonce}:{transcript}")` — alias : `signature` |
| `request_signature` | string | Non | HMAC AuthGuard optionnel pour nœuds délégués |

**Réponse `200` :**

```json
{
  "status": "manifested",
  "response": "Application successfully anchored into UtahContainerEngine loop on workspace port 8200."
}
```

### Transcriptions prises en charge

| Intention | Exemple de transcription |
|-----------|--------------------------|
| Revendiquer le nœud | `"Claim node"` |
| Autoriser un nœud | `"authorize node <64-char-vibe-hash>"` |
| Déployer une application | `"deploy application hello"` ou `"manifest app hello"` |
| Corriger une application | `"patch app hello to add feature x"` |
| Statut | `"status grid"` |

**Revendiquer le nœud (première exécution) :**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "Claim node", "acoustic_hash": "abc123..."}'
```

**Déployer une application (mode ouvert — avant revendication, tout hash accepté) :**

```bash
curl -X POST http://127.0.0.1:8999/command \
  -H "Content-Type: application/json" \
  -d '{"transcript": "deploy application hello", "acoustic_hash": "0000000000000000000000000000000000000000000000000000000000000000"}'
```

**Voice Bridge v27.0** appelle `GET /nonce` et signe automatiquement. Signature manuelle :

```python
from voice_bridge_signed import get_signed_payload
payload = get_signed_payload("deploy application hello", acoustic_hash)
```

**Après revendication :** `acoustic_hash` doit correspondre à la racine ou à `authorized_nodes[]`, et `nonce` + `command_signature` doivent être valides, sinon le noyau renvoie :

```json
{
  "status": "manifested",
  "response": "Access Denied. Biological signature does not match the Akashic Record."
}
```

---

## GET /app/{app_name}

Accéder à une application locataire déployée. Protégé par l'autorisation de paiement Utah-Tycoon.

**En-têtes :**

| En-tête | Description |
|---------|-------------|
| `X-Client-ID` | Identifiant client optionnel (par défaut : IP du client) |

### Client non payé — Réponse `402 Payment Required`

```json
{
  "error": "Payment Required for UtahContainer Execution",
  "payment_address": "bc1q_utah_ephemeral_a1b2c3d4e5f6",
  "amount_sats": 5000,
  "message": "Transmit value to unlock silicon processing path."
}
```

Les factures se règlent automatiquement après ~60 secondes dans la simulation actuelle.

### Client payé — Réponse `200`

UtahX transmet la requête au backend UtahContainerEngine sur le port du locataire. Le corps de la réponse est la sortie JSON du handler.

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## PUT/POST /s3/{bucket}/{key}

Écrire un objet dans Utah S3 Mesh (stockage NVMe local).

**En-têtes (optionnels) :**

| En-tête | Description |
|---------|-------------|
| `X-Utah-Tenant-ID` | Identifiant locataire |
| `X-Utah-Signature` | HMAC-SHA256 de `{tenant_id}:{path}` |

**Exemple :**

```bash
curl -X PUT http://127.0.0.1:8999/s3/my-data/file.txt \
  -H "Content-Type: text/plain" \
  --data-binary "Hello Utah"
```

---

## GET /s3/{bucket}/{key}

Lire un objet. Renvoie des octets bruts. Utiliser `GET /s3/{bucket}/prefix*` pour lister.

```bash
curl http://127.0.0.1:8999/s3/my-data/file.txt
```

---

## POST /rds/write

Écrire un enregistrement clé-valeur dans Utah RDS Ledger.

**Corps de la requête :**

```json
{"key": "user:123", "value": {"name": "Alice", "score": 9000}}
```

**Réponse `200` :**

```json
{"key": "user:123", "status": "written", "epoch": 1718280000.0}
```

---

## GET /rds/read/{key}

Lire un enregistrement par clé.

```bash
curl http://127.0.0.1:8999/rds/read/user:123
```

---

## POST /lambda/{function_name}/invoke

Invoquer un handler Utah Lambda (sans tirage d'image conteneur).

**Corps de la requête :** événement JSON passé à `handler(event, context)`

```bash
curl -X POST http://127.0.0.1:8999/lambda/my-function/invoke \
  -H "Content-Type: application/json" \
  -d '{"name": "General 23"}'
```

**Réponse `200` :**

```json
{"result": {"message": "Hello General 23 from Utah Lambda!"}}
```

---

## POST /app/unlock

Soumettre une demande de déverrouillage par paiement. Tycoon interroge mempool.space (ou electrum-server) pour la finalité du paiement. Les adresses de développement (`bc1q_utah_*`) utilisent un règlement temporisé en mode `auto`.

**Corps de la requête :**

```json
{
  "app_name": "hello",
  "client_id": "demo-client",
  "payment_tx": "optional-tx-hint",
  "amount_sats": 5000
}
```

**Réponse `202` :**

```json
{
  "status": "pending",
  "message": "Payment required. Awaiting ledger consensus.",
  "tx_id": "tx_abc123",
  "payment_address": "bc1q_utah_ephemeral_...",
  "amount_sats": 5000
}
```

Après règlement, `GET /app/{app_name}` avec le même `X-Client-ID` transmet la requête au conteneur.

---

## POST /admin/revoke-node

Révoquer un nœud délégué de `authorized_nodes[]`. Titulaire vibe racine uniquement. Le panneau de révocation Utah-Flux appelle ce point de terminaison.

**Corps de la requête :**

```json
{
  "node_hash": "abc123...64chars",
  "acoustic_hash": "root-vibe-hash-64chars"
}
```

**Réponse `200` :**

```json
{"status": "revoked", "node_hash": "abc123..."}
```

---

## Réponses d'erreur

| Code | Quand |
|------|-------|
| `404` | Chemin inconnu ou nœud non révocable |
| `402` | L'application existe mais le client n'a pas payé la facture Tycoon |
| `403` | Identifiants de révocation ou HMAC invalides |

---

## Ports et multidiffusion

| Service | Port / Adresse |
|---------|----------------|
| Ingress HTTP | `8999` |
| Gossip UtahNetes | UDP `9001`, multidiffusion `239.255.43.21` |
| Global Swarm | UDP `9055` |

---

## Fichiers de données

| Fichier | Objectif |
|---------|----------|
| `{UTAH_DATA_DIR}/secure_registry.json` | Locataires, routes UtahX, index de stockage |
| `{UTAH_DATA_DIR}/flux_ui_manifest.json` | État de l'interface Utah-Flux |
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Handler conteneur |
| `{UTAH_DATA_DIR}/lambda/{fn}/handler.py` | Handler Lambda |
| `{UTAH_DATA_DIR}/s3/{bucket}/{key}` | Objets S3 Mesh |
| `{UTAH_DATA_DIR}/rds/ledger.json` | Magasin clé-valeur RDS |
| `security/biometric_ledger.json` | Hash vibe racine (repli local si `/etc` non inscriptible) |
| `tycoon/settlement_ledger.json` | État des factures et paiements |

`UTAH_DATA_DIR` par défaut : `/var/lib/utahmosphere` (repli vers des répertoires locaux en cas d'erreur de permission).
