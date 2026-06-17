# UtahMosphere dokumentatsiooni portaal

Tere tulemast UtahMosphere OS dokumentatsiooni keskusesse. **v35.0 Omni-Desk** — suveräänne usaldusahel: TPM Locker, RA-TLS mesh-tõendamine, Okeaania mempool ja automaatne häälsild allkirjastatud nonce-ga. Sisu on jaotatud **sihtgruppide**, **praktiliste õpetuste**, **retseptide** ja **algprojektide** kaupa.

---

## Alusta siit

| Dokument | Sobib kõige paremini |
|----------|----------------------|
| [Omni-Desk](OMNI_DESK.md) | Suveräänne holograafiline töölaud |
| [Cursor epigeneetiline IDE](CURSOR_EPIGENETIC.md) | Level 6 Archivist, Command Decki nupud |
| [Omni-Viewporti laiendus](OMNI_VIEWPORT_EXTENSION.md) | GUI nupud + Inspiration Forge |
| [UtahClaw](UTAH_CLAW.md) | Epistemilise tühimiku lahendaja |
| [Omni-Glass UI](OMNI_GLASS_UI.md) | Reaalajas agentide visualiseerimine |
| [Chrono-State](CHRONO_STATE.md) | Otsemutatsiooni tagasikerimine |
| [Kinematic Siphon](KINEMATIC_SIPHON.md) | Ghost Tune GPU klient |
| [Kvoorumi tunnistajad](QUORUM_WITNESSES.md) | Mitmeregiooni ISP-katkestuse vahekohtunikud |
| [Lazarus automaatne taastamine](LAZARUS_RESTORE.md) | Puhastoa Golden Master taastamine |
| [Oleku-erinevuse mootor](STATE_DIFF_ENGINE.md) | Põimunud <1KB mesh-sünkroniseerimine |
| [Võimekuste maatriks](CAPABILITY_MATRIX.md) | Kõigile — mis töötab täna vs tuleviku töö |
| [API viide](API_REFERENCE.md) | Arendajatele ja operaatoritele |
| [Kohaliku arenduse juhend](LOCAL_DEVELOPMENT.md) | Arendajatele Windowsis, macOS-is või Linuxis |

---

## Rolli juhendid

| Roll | Ülevaade | Õpetus | Retseptid |
|------|----------|--------|-----------|
| **Lapsed ja pered** | [Lihtsas keeles lastele](ELI5_FOR_KIDS.md) | [Esimene robot-kammerjäger](tutorials/01-kids-first-robot-butler.md) | [Retseptide register](recipes/README.md) |
| **Juhtkond (CEO/CTO)** | [Juhtkonna kokkuvõte](EXECUTIVE_SUMMARY.md) | — | [Retseptide register](recipes/README.md) |
| **Arhitektid** | [Tehniline süvauuring](TECHNICAL_DEEP_DIVE.md) | — | [Retseptide register](recipes/README.md) |
| **Arendajad** | [Arendaja retseptiraamat](DEVELOPER_COOKBOOK.md) | [Sinu esimene rakendus](tutorials/05-developer-first-app.md) | [Retseptide register](recipes/README.md) |
| **Mitte-tehnilised kasutajad** | [Mitte-tehniline juhend](NON_TECHNICAL_GUIDE.md) | [Seadistus ilma žargoonita](tutorials/06-non-technical-setup.md) | [Retseptide register](recipes/README.md) |

---

## Õpetused

1. [Sinu esimene robot-kammerjäger](tutorials/01-kids-first-robot-butler.md) — lapsed ja pered
2. [Sinu esimene rakendus](tutorials/05-developer-first-app.md) — arendaja täielik voog
3. [Seadistus ilma žargoonita](tutorials/06-non-technical-setup.md) — mitte-tehniline sisseelamine

---

## Retseptid

- [Retseptide register](recipes/README.md)

---

## Mallid ja algprojektid

| Mall | Eesmärk |
|------|---------|
| [python-http-service](../../templates/python-http-service/) | HTTP mikroteenus |
| [container-handler](../../templates/container-handler/) | `handler.py` |
| [voice-command-client](../../templates/voice-command-client/) | `/command` klient |
| [frontend-upload](../../templates/frontend-upload/) | Brauseri klient |
| [tycoon-payment-client](../../templates/tycoon-payment-client/) | HTTP 402 maksevoog |

| Näide | Kirjeldus |
|-------|-----------|
| [hello-world](../../examples/hello-world/) | Juurutamine `/command` kaudu |
| [check-node-health](../../examples/check-node-health/) | Tervisekontroll |
| [paid-app-access](../../examples/paid-app-access/) | Tycoon maksevärav |
| [omega-build-verify](../../examples/omega-build-verify/) | Täielik S3/Lambda/RDS/konteineri test |

| Algprojekt | Kirjeldus |
|------------|-----------|
| [minimal-api](../../starter-projects/minimal-api/) | Minimaalne API |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Hääl + armatuurlaud |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Tasuline juurdepääs |

---

## UtahMosphere OS v34.0

- **Suveräänne servplatvorm** Pythonis — port `8999`, `build: omega-build-v35-omni-desk`
- **TPM Locker** — `tpm_lock.py` pitstab Vibe-Print PCR0-sse claim-il
- **RA-TLS mesh-tõendamine** — `ra_tls_attest.py` + `GET /attestation/quote`
- **Hääljuurutus** — Voice Bridge kutsub automaatselt `GET /nonce` ja allkirjastab
- **Mempool varuühendus** — `tycoon_failover.py` neljas piirkonnas (USA, EL, globaalne, Okeaania)
- **Biomeetriline claim** — käsk «Claim node»; TPM-iga seotud vibe kontroll
- **Sõlme tühistamine** — `POST /admin/revoke-node` ja Utah-Flux paneel
- **Genesis ISO** — `genesis_iso_builder.py` → `utah_genesis_v35.iso`
- **Tycoon HTTP 402** — `GET /app/{name}` 4-piirkonnilise mempool arveldusega
