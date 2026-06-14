# UtahMosphere-dokumentaatio

Tervetuloa UtahMosphere OS -dokumentaatioon. **v28.0 TPM-Hardened Attested** — suvereeni luottamusketju: TPM Locker, RA-TLS mesh-todentaminen, Oseanian mempool ja Voice Bridge automaattisella nonce-allekirjoituksella. Sisältö on jaettu **rooleihin**, **oppaisiin**, **resepteihin** ja **aloitusprojekteihin**.

---

## Aloita tästä

| Dokumentti | Parhaiten |
|------------|-----------|
| [Ominaisuusmatriisi](CAPABILITY_MATRIX.md) | Kaikille — mitä toimii nyt vs. tuleva työ |
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

## UtahMosphere OS v28.0

- **Suvereeni reunalaituri** Pythonilla — portti `8999`, `build: omega-build-v28-attested`
- **TPM Locker** — `tpm_lock.py` sinetöi Vibe-Printin PCR0:een claimissä
- **RA-TLS mesh-todentaminen** — `ra_tls_attest.py` + `GET /attestation/quote`
- **Äänikäyttöönotto** — Voice Bridge kutsuu automaattisesti `GET /nonce` ja allekirjoittaa
- **Mempool-varajärjestelmä** — `tycoon_failover.py` neljällä alueella (US, EU, global, Oseania)
- **Biometrinen claim** — komento «Claim node»; TPM-sidottu vibe-vahvistus
- **Solmun peruutus** — `POST /admin/revoke-node` ja Utah-Flux-paneeli
- **Genesis ISO** — `genesis_iso_builder.py` → `utah_genesis_v28.iso`
- **Tycoon HTTP 402** — `GET /app/{name}` 4 alueen mempool-selvityksellä
