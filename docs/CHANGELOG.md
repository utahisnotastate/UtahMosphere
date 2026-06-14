# Changelog

All notable changes to UtahMosphere OS are documented here.

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
