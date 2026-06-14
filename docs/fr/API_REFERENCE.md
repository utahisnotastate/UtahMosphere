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
  "version": "25.0"
}
```

**Exemple :**

```bash
curl http://127.0.0.1:8999/health
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
  "claimed": true
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

**Après revendication :** `acoustic_hash` doit correspondre au hash vibe racine ancré, sinon le noyau renvoie :

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

```json
{
  "status": "Unlocked",
  "message": "Container hello executing."
}
```

**Exemple :**

```bash
curl -H "X-Client-ID: demo-client" http://127.0.0.1:8999/app/hello
```

---

## Réponses d'erreur

| Code | Quand |
|------|-------|
| `404` | Chemin inconnu |
| `402` | L'application existe mais le client n'a pas payé la facture Tycoon |

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
| `{UTAH_DATA_DIR}/containers/{app}/handler.py` | Stub de handler déployé |
| `security/biometric_ledger.json` | Hash vibe racine (repli local si `/etc` non inscriptible) |
| `tycoon/settlement_ledger.json` | État des factures et paiements |

`UTAH_DATA_DIR` par défaut : `/var/lib/utahmosphere` (repli vers des répertoires locaux en cas d'erreur de permission).
