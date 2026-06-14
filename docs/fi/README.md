# UtahMosphere-dokumentaatio

Tervetuloa UtahMosphere OS -dokumentaatioon. Sisältö on jaettu **rooleihin**, **oppaisiin**, **resepteihin** ja **aloitusprojekteihin**.

**Muut kielet:** jokainen locale on täysin erillinen sivusto (yksi kieli per sivu). Katso [Dokumentaation kielet](../LANGUAGES.md).

---

## Aloita tästä

| Dokumentti | Parhaiten |
|------------|-----------|
| [Laitteisto quote -rekisteri](QUOTE_REGISTRY.md) | Globaali TPM-laitteiston sormenjälkitilasto |
| [RA-TLS mesh-todentaminen](RA_TLS.md) | TPM quote -vahvistus + CA-kiinnitys mesh-solmuille |
| [Laitteiston todentaminen](ATTESTATION.md) | TPM PCR0 + Vibe-Print-sinetti |
| [Genesis ISO -asentaja](GENESIS_ISO.md) | USB-UEFI-käynnistyskuva |
| [Ominaisuusmatriisi](CAPABILITY_MATRIX.md) | Kaikille — v30.0 etätodentamisinfra |
| [API-viite](API_REFERENCE.md) | Kehittäjille ja operaattoreille |
| [Paikallisen kehityksen opas](LOCAL_DEVELOPMENT.md) | Kehittäjille Windowsissa, macOS:ssä tai Linuxissa |

---

## Roolioppaat

| Rooli | Yleiskatsaus | Opas | Reseptit |
|-------|--------------|------|----------|
| **Lapset ja perheet** | [Selitettynä lapsille](ELI5_FOR_KIDS.md) | [Ensimmäinen robottihovimestari](tutorials/01-kids-first-robot-butler.md) | [Reseptihakemisto](recipes/README.md) |
| **Johtajat (CEO/CTO)** | [Johdon yhteenveto](EXECUTIVE_SUMMARY.md) | — | [Reseptihakemisto](recipes/README.md) |
| **Arkkitehdit** | [Tekninen syväluotaus](TECHNICAL_DEEP_DIVE.md) | — | [Reseptihakemisto](recipes/README.md) |
| **Kehittäjät** | [Kehittäjän keittokirja](DEVELOPER_COOKBOOK.md) | [Ensimmäinen sovellus](tutorials/05-developer-first-app.md) | [Reseptihakemisto](recipes/README.md) |
| **Ei-tekniset käyttäjät** | [Ei-tekninen opas](NON_TECHNICAL_GUIDE.md) | [Käyttöönotto ilman jargon](tutorials/06-non-technical-setup.md) | [Reseptihakemisto](recipes/README.md) |

---

## Oppaat

1. [Ensimmäinen robottihovimestari](tutorials/01-kids-first-robot-butler.md) — lapset ja perheet
2. [Ensimmäinen sovellus](tutorials/05-developer-first-app.md) — kehittäjän kokonaisprosessi
3. [Käyttöönotto ilman jargon](tutorials/06-non-technical-setup.md) — ei-tekninen käyttöönotto

---

## Reseptit

- [Reseptihakemisto](recipes/README.md)

---

## Mallit ja aloitusprojektit

| Malli | Tarkoitus |
|-------|-----------|
| [python-http-service](../../templates/python-http-service/) | HTTP-mikropalvelu |
| [container-handler](../../templates/container-handler/) | `handler.py` |
| [voice-command-client](../../templates/voice-command-client/) | `/command`-asiakas |
| [frontend-upload](../../templates/frontend-upload/) | Selainasiakas |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | HTTP 402 -maksu |

| Esimerkki | Kuvaus |
|-----------|--------|
| [hello-world](../../examples/hello-world/) | Käyttöönotto `/command`-kautta |
| [check-node-health](../../examples/check-node-health/) | Terveystarkistus |
| [paid-app-access](../../examples/paid-app-access/) | Tycoon-maksuportti |
| [omega-build-verify](../../examples/omega-build-verify/) | Täysi S3/Lambda/RDS/kontti-testi |

| Aloitusprojekti | Kuvaus |
|-----------------|--------|
| [minimal-api](../../starter-projects/minimal-api/) | Minimaalinen API |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Ääni + kojelauta |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Maksullinen pääsy |

---

## UtahMosphere OS v30.0 etätodentamisinfra

- **Quote-rekisteri (`quote_registry.py`):** globaali TPM-laitteiston sormenjälkitilasto; rekisteröinti, poisto ja yhdistäminen meshissä
- **RA-TLS Guard (`ra_tls_guard.py`):** CA-kiinnitys; UtahX-sisääntulo; X.509 OID -vahvistus
- **RA-TLS mesh-todentaminen** — `ra_tls_attest.py` + `GET /attestation/quote`; rekisterin replikointi
- **TPM Locker** — `tpm_lock.py` sinetöi Vibe-Printin PCR0:een claimissä
- **Äänikäyttöönotto** — Voice Bridge kutsuu automaattisesti `GET /nonce` ja allekirjoittaa
- **Mempool-varajärjestelmä** — `tycoon_failover.py` neljällä alueella (US, EU, global, Oseania)
- **Biometrinen claim** — komento «Claim node»; TPM-sidottu vibe-vahvistus
- **Solmun peruutus** — `POST /admin/revoke-node` ja Utah-Flux-paneeli
- **Genesis ISO v30** — `genesis_iso_builder.py` → `utah_genesis_v30.iso`
- **Tycoon HTTP 402** — `GET /app/{name}` 4 alueen mempool-selvityksellä

Build `omega-build-v30-federated-attested`. Suositeltu käynnistys: `python3 utahmosphere_master.py`.
