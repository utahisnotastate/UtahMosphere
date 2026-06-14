# Changelog

All notable changes to UtahMosphere OS are documented here.

## [27.0] — Production Immutable (2026-06)

### Added
- `attestation_guard.py` — TPM 2.0 PCR0 hardware root-of-trust in `bootstrap.sh`
- `tycoon_failover.py` — multi-region mempool failover (mempool.space, signet, blockstream)
- `voice_bridge_signed.py` — automatic `GET /nonce` + HMAC signing for voice commands
- [Hardware Attestation](ATTESTATION.md) documentation
- `/health` and `/status` `attestation` field

### Changed
- `voice_bridge.py` — uses `voice_bridge_signed` for all transmissions
- `tycoon_settlement.py` — routes through `MempoolFailover` before electrum fallback
- Genesis ISO output: `utah_genesis_v27.iso`
- Build identifier: `omega-build-v27-production`
- v26.0 roadmap items complete; all locale docs updated

## [26.0] — Omega-Build FINAL (2026-06)

### Added
- `genesis_iso_builder.py` — Alpine vmlinuz/initramfs bundling, syslinux auto-install menu
- `nonce_guard.py` — 30-second voice command anti-replay (`GET /nonce`, `command_signature`)
- `ui_revocation.py` — Utah-Flux authorized node revocation panel
- `POST /admin/revoke-node` — root-only mesh node revocation API
- `GET /nonce` — server-issued command nonce endpoint

### Changed
- `mk_iso.sh` delegates to `genesis_iso_builder.py`; output `utah_genesis_v26.iso`
- `flux_gui.py` — revocation admin panel wired to kernel API
- `quantum_ledger.py` — `revoke_node()` with AuthGuard refresh
- Build identifier: `omega-build-v26-final`
- Roadmap items (Alpine ISO, nonce anti-replay, revocation UI): **complete**
- All locale documentation updated for v26.0

## [25.3] — Migration Ready (2026-06)

### Added
- `tycoon_settlement.py` — real-time mempool.space / electrum-server Bitcoin settlement
- `ledger_auth.py` — AuthGuard HMAC enforcement for `authorized_nodes[]`
- `mk_iso.sh` — Genesis ISO builder (`utah_genesis_v25.iso`)
- [Genesis ISO Installer](GENESIS_ISO.md) documentation
- Voice command: `"authorize node <hash>"` for delegated mesh authority

### Changed
- Utah-Tycoon: simulated 60s wait → mempool polling with `auto`/`real`/`simulate` modes
- UtahNetes mesh: signed gossip payloads (`mesh_signature`, `signer_hash`)
- `authorized_nodes[]`: stub → **enforced** via AuthGuard
- `/status` includes `authorized_nodes` and expanded `tycoon` stats
- Build identifier: `golden-master-v25.1`

## [25.2] — Golden Master Final (2026-06)

### Added
- `utah_mesh_engine.py` — UtahNetes 5s multicast + `master_registry.json`
- `utah_ota_lazarus.py` — OTA Lazarus channel for swarm kernel push
- `POST /app/unlock` — Tycoon payment unlock with HTTP 202
- Deterministic DHT routing: FIND_NODE, iterative peer lookup in Swarm
- Tycoon `threading.Event` settlement loop with tenant activation callbacks

### Changed
- Utah-Tycoon, UtahNetes, Global Swarm: **Partial → Implemented**
- `utahmosphere_master.py` — Golden Master Final entry point
- `genesis_deploy.py` — module pre-warm + `threading.Event().wait()`
- All locale CAPABILITY_MATRIX and API_REFERENCE docs updated

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
