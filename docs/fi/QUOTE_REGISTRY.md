# Laitteisto quote -rekisteri (v29.0)

**Laitteisto quote -rekisteri** on hajautettu totuuden lähde kelvollisille TPM-laitteiston sormenjäljille UtahMosphere-parvessa. Solmut eivät luota IP-osoitteisiin — ne luottavat **laitteisto quoteihin**, jotka Utah-Kernel Root CA on allekirjoittanut ja jotka on rekisteröity tähän tilastoon.

## Topologia

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

## Rekisteripalvelu (`quote_registry.py`)

| Metodi | Tarkoitus |
|--------|-----------|
| `register_node(hardware_id, public_quote, ...)` | Lisää solmu biometrisen claimin jälkeen |
| `is_valid_hardware(hardware_id)` | Tarkista aktiivinen rekisterimerkintä |
| `purge_node(hardware_id, reason)` | Karanteeni vaarantunut laitteisto |
| `merge_remote(remote_nodes)` | Replikoi rekisteri mesh-gossipista |
| `export_nodes()` | Täydellinen rekisteritilannekuva synkronointiin |

Pysyvyys: `{UTAH_DATA_DIR}/quote_registry.json`

## RA-TLS Guard (`ra_tls_guard.py`)

Pakottaa **CA-kiinnityksen**. Vain solmut, joiden laitteisto quote on Utah-Kernel Root CA:n allekirjoittama ja rekisterissä, voivat liittyä meshiin tai läpäistä UtahX-sisääntulon.

- X.509-mukautettu OID `1.3.6.1.4.1.99999` kuljettaa TPM quoten (kun `cryptography` on asennettu)
- HTTP-sisääntulo: `X-Utah-Hardware-ID` + `X-Utah-RATLS-Quote` -otsikot validoidaan ennen välitystä

## Biometrinen TPM-sidonta (claim-prosessi)

`"Claim node"` -vaiheessa:

1. Kaappaa akustiset MFCC:t → vibe-print -hash
2. Sinetöi vibe-print TPM PCR0:een (`tpm_lock.py`)
3. Johda `hardware_id` vibesta + PCR0:sta + solmun identiteetistä
4. Allekirjoita laitteisto quote ytimen juuri-CA:lla
5. `register_node()` työntää merkinnän globaaliin rekisteriin
6. Mesh-lähetykset sisältävät `quote_registry` -kentän parin yhdistämiseen

## HTTP API

### GET /registry/quotes

Listaa kaikki rekisteröidyt laitteisto quotet.

```bash
curl http://127.0.0.1:8999/registry/quotes
```

**Vastaus `200`:**

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

Poista vaarantunut laitteisto. Vain juuri-vibe-omistaja.

```bash
curl -X POST http://127.0.0.1:8999/registry/purge \
  -H "Content-Type: application/json" \
  -d '{"hardware_id": "abc...", "acoustic_hash": "root-vibe-64chars", "reason": "firmware tamper"}'
```

## Ympäristö

| Muuttuja | Oletus | Tarkoitus |
|----------|--------|-----------|
| `UTAH_QUOTE_REGISTRY_PATH` | `{UTAH_DATA_DIR}/quote_registry.json` | Rekisterin pysyvyys |
| `UTAH_RA_TLS_GUARD_ENFORCE` | `1` | UtahX-sisääntulo + CA-kiinnitys (`0` = dev) |
| `UTAH_KERNEL_ROOT_CA` | `utahmosphere_omega_build_v29_root_ca` | Quoten allekirjoituksen juuri |
| `UTAH_KERNEL_ROOT_CA_PATH` | `/etc/utahmosphere/security/utah_root_ca.pem` | PEM-julkinen avain CA-vahvistukseen |

Ohita kaikki todentamiskerrokset kehityksessä:

```bash
export UTAH_ATTESTATION_ENFORCE=0
export UTAH_TPM_LOCK_ENFORCE=0
export UTAH_RA_TLS_ENFORCE=0
export UTAH_RA_TLS_GUARD_ENFORCE=0
```

## Liittyvät

- [RA-TLS mesh-todentaminen](RA_TLS.md)
- [Laitteiston todentaminen](ATTESTATION.md)
- [Ominaisuusmatriisi](CAPABILITY_MATRIX.md)
