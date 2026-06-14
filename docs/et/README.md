# UtahMosphere dokumentatsiooni portaal

Tere tulemast UtahMosphere OS dokumentatsiooni keskusesse. **Golden Master Final v25.0** — ühtne bare-metal tuum, kus Utah-Tycoon, UtahNetes ja Global Swarm on täielikult integreeritud. Sisu on jaotatud **sihtgruppide**, **praktiliste õpetuste**, **retseptide** ja **algprojektide** kaupa.

---

## Alusta siit

| Dokument | Sobib kõige paremini |
|----------|----------------------|
| [Võimekuste maatriks](CAPABILITY_MATRIX.md) | Kõigile — mis töötab täna vs teekaart |
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
| [voice-deploy-simulator](../../examples/voice-deploy-simulator/) | Ilma mikrofonita |

| Algprojekt | Kirjeldus |
|------------|-----------|
| [minimal-api](../../starter-projects/minimal-api/) | Minimaalne API |
| [voice-controlled-dashboard](../../starter-projects/voice-controlled-dashboard/) | Hääl + armatuurlaud |
| [monetized-endpoint](../../starter-projects/monetized-endpoint/) | Tasuline juurdepääs |

---

## UtahMosphere OS v25.0

- **Suveräänne servplatvorm** Pythonis — port `8999`
- **Hääljuurutus** — Voice Bridge või `POST /command`
- **Biomeetriline claim** — käsk «Claim node»
- **Tycoon HTTP 402** — `GET /app/{name}`
