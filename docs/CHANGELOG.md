# Changelog

All notable changes to UtahMosphere OS are documented here.

## [25.1] — Omega-Build Golden Master (2026-06)

### Added
- `utahmosphere_master.py` — Golden Master kernel entry point
- `bootstrap.sh` — bare-metal Auto-Genesis installer (systemd + `utah-kernel`)
- `utahx_proxy.py` — native HTTP proxy (replaces Nginx)
- `utah_container_runtime.py` — UtahContainerEngine per-tenant servers
- `utah_s3_mesh.py` — S3 parity (`GET/PUT/POST /s3/{bucket}/{key}`)
- `utah_lambda_engine.py` — Lambda parity (`POST /lambda/{fn}/invoke`)
- `utah_rds_ledger.py` — RDS parity (`/rds/read`, `/rds/write`)
- `utah_lazarus.py` — AST-validated Lazarus mutation engine
- `examples/omega-build-verify/` — end-to-end parity verification script
- [Omega-Build Golden Master](OMEGA_BUILD.md) architecture document

### Changed
- `utahmosphere_os.py` — full HTTP multiplexer with S3/Lambda/RDS/UtahX proxy
- `genesis_deploy.py` — launches Golden Master + tycoon + swarm + UI
- `setup.sh` — delegates to `bootstrap.sh`
- Container deploy now starts live HTTP listeners on ports 8200+
- `/app/{name}` proxies to container backend after Tycoon settlement
- [Capability Matrix](CAPABILITY_MATRIX.md) and [API Reference](API_REFERENCE.md) updated

## [25.0] — Documentation & API Polish (2026-06)

### Added
- Documentation portal: [docs/README.md](README.md)
- Six role-based tutorials under `docs/tutorials/`
- Per-role recipe docs under `docs/recipes/`
- Reference docs: API Reference, Capability Matrix, Access Control, Local Development, Operations Runbook
- `templates/` — 5 boilerplate packages
- `examples/` — health check, deploy simulator, paid access, hello-world
- `starter-projects/` — minimal-api, voice-controlled-dashboard, monetized-endpoint
- `GET /health` and `GET /status` HTTP endpoints

### Changed
- `flux_gui.py` respects `UTAH_DATA_DIR` for manifest path
- Executive Summary version aligned to v25.0
- Developer Cookbook expanded with links to recipes and templates
- Cloud Parity Migration guide annotated with implementation status
- Root README expanded with full documentation index

### Known Limitations (unchanged)
- S3, Lambda invoke, RDS HTTP routes documented but not implemented
- Lazarus performs file append, not full AST mutation
- Tycoon uses simulated 60s payment settlement

## [25.0] — Omega-Genesis (2024)

- Initial sovereign kernel with voice deploy, Tycoon 402 gate, UtahNetes gossip
- Quantum Ledger biometric claim flow
- Utah-Flux Tkinter UI
- genesis_deploy orchestrator and setup.sh provisioning
