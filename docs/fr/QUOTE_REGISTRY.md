# Registre des citations matérielles (v32.0)

Le **registre des citations matérielles** est la source de vérité distribuée des empreintes matérielles TPM valides dans l'essaim UtahMosphere. Les nœuds ne font pas confiance aux adresses IP — ils font confiance aux **citations matérielles** signées par la CA racine Utah-Kernel et enregistrées dans ce registre.

## Topologie

```
Node A (claim)                    Swarm peers
    |                                  |
    |-- seal vibe to PCR0 ------------>|
    |-- sign hardware quote ---------->|-- merge_remote()
    |-- register_node() -------------->|-- quote_registry in mesh payload
    |                                  |
Peer B connects via RA-TLS ----------> verify against registry
    |                                  |
UtahX ingress ----------------------> ra_tls_guard.verify_http_headers()
```

## Service de registre (`quote_registry.py`)

| Méthode | Objectif |
|--------|---------|
| `register_node(hardware_id, public_quote, ...)` | Ajouter un nœud après revendication biométrique |
| `is_valid_hardware(hardware_id)` | Vérifier une entrée active du registre |
| `purge_node(hardware_id, reason)` | Mettre en quarantaine le matériel compromis |
| `merge_remote(remote_nodes)` | Répliquer le registre depuis le gossip du maillage |
| `export_nodes()` | Instantané complet du registre pour synchronisation |

Persistance : `{UTAH_DATA_DIR}/quote_registry.json`

## Garde RA-TLS (`ra_tls_guard.py`)

Applique l'**épinglage CA**. Seuls les nœuds dont la citation matérielle est signée par la CA racine Utah-Kernel et présente dans le registre peuvent rejoindre le maillage ou passer l'ingress UtahX.

- L'OID personnalisé X.509 `1.3.6.1.4.1.99999` transporte la citation TPM (lorsque `cryptography` est installé)
- Ingress HTTP : en-têtes `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` validés avant le proxy

## Liaison biométrique au TPM (flux de revendication)

Lors de `"Claim node"` :

1. Capturer les MFCC acoustiques → hash vibe-print
2. Sceller le vibe-print au PCR0 TPM (`tpm_lock.py`)
3. Dériver `hardware_id` à partir du vibe + PCR0 + identité du nœud
4. Signer la citation matérielle avec la CA racine du noyau
5. `register_node()` pousse l'entrée vers le registre global
6. Les diffusions du maillage incluent `quote_registry` pour la fusion entre pairs

## API HTTP

### GET /registry/quotes

Lister toutes les citations matérielles enregistrées.

```bash
curl http://127.0.0.1:8999/registry/quotes
```

**Réponse `200` :**

```json
{
  "nodes": {
    "abc123...": {
      "public_quote": "{\"body\":\"...\",\"signature\":\"...\"}",
      "vibe_hash": "64-char-sha256",
      "status": "active"
    }
  },
  "stats": {"active": 1, "purged": 0, "total": 1}
}
```

### POST /registry/purge

Purger le matériel compromis. Titulaire vibe racine uniquement.

```bash
curl -X POST http://127.0.0.1:8999/registry/purge \
  -H "Content-Type: application/json" \
  -d '{"hardware_id": "abc...", "acoustic_hash": "root-vibe-64chars", "reason": "firmware tamper"}'
```

## Variables d'environnement

| Variable | Défaut | Objectif |
|----------|--------|----------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Persistance du registre |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | Ingress UtahX + épinglage CA (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v32_root_ca` | Racine de signature des citations |
| `UTAH_KERNEL_ROOT_CA_PATH` | `/etc/utahmosphere/security/utah_root_ca.pem` | Clé publique PEM pour vérification CA |

Ignorer toutes les couches d'attestation en développement :

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## Voir aussi

- [Attestation RA-TLS du maillage](RA_TLS.md)
- [Attestation matérielle](ATTESTATION.md)
- [Matrice des capacités](CAPABILITY_MATRIX.md)
