# Changelog

All notable changes to UtahMosphere OS are documented here.

## [35.1] — Omni-Viewport Extension & Cursor Level 6 (2026-06)

### Added
- `extensions/utah-omni-viewport/` — Command Deck + Inspiration Forge GUI (no slash commands)
- `scripts/inspiration_scanner.py` — cross-codebase pattern mining for feature planning
- MCP bridges: `utahclaw_mcp_bridge.py`, `mcp_godeye.py`, `mcp_deployer.py`, `mcp_zeo_entropy.py`, `mcp_akashic_adr.py`
- `.cursorrules`, `.cursor/memory.md`, `.cursor/mcp.json`, ADR store, Level-6 skills
- [Cursor Epigenetic IDE](CURSOR_EPIGENETIC.md), [Omni-Viewport Extension](OMNI_VIEWPORT_EXTENSION.md) + 8 locale translations

### Changed
- Protocol triggers moved from slash commands to Omni-Viewport buttons
- `.gitignore` — allow project JSON; exclude personal `.cursor/user.json` and workspace editor settings

## [35.0] — Omni-Desk Genesis Suite (2026-06)

### Added
- `omni_desk.py` — Material-UI inspired holographic desktop on port **9092**
- Five Genesis apps: WebForge, ZEO-Canvas, AppSmith, Holo-Notebook, Claw-Harvester
- `GET /desk/apps`, `GET /desk/status`, `GET /desk/ui`, `POST /desk/intent`
- `ambient_runner.harvest_codebase()` + `POST /harvest` on UtahClaw port 9090
- [Omni-Desk](OMNI_DESK.md) guide + 8 locale translations

### Changed
- Build: `omega-build-v35-omni-desk`
- Genesis ISO: `utah_genesis_v35.iso`
- RA-TLS root CA: `utahmosphere_omega_build_v35_root_ca`
- `examples/omega-build-verify/verify.py` — desk probes

## [34.0] — UtahClaw & Omni-Glass Chrono-State (2026-06)

### Added
- `utahclaw/` — ambient runner, holographic memory, epistemic void, kinematic siphon
- `chrono_state.py` — speculative AI mutation with memory rewind
- `omni_glass_stream.py` — FluxRelay SSE on port 9091
- `POST /claw/void`, `GET /claw/status`, `GET /chrono/status`, `GET /siphon/ghost-tune`
- UtahClaw fast-socket on port 9090
- [UtahClaw](UTAH_CLAW.md), [Chrono-State](CHRONO_STATE.md), [Omni-Glass UI](OMNI_GLASS_UI.md), [Kinematic Siphon](KINEMATIC_SIPHON.md)

### Changed
- `omni_glass.py` — state manifold, thought vectors, claw research telemetry
- `omni_compiler.py` — epistemic void → UtahClaw dispatch; chrono post-deploy
- Genesis ISO: `utah_genesis_v34.iso`
- Build: `omega-build-v34-utah-claw`
- Documentation: v34 guides translated (8 locales); API health JSON + quote registry CA sync

## [33.0] — Omni-Compiler & Utah-Omni-Mind (2026-06)

### Added
- `omni_compiler.py` — agentic intent → blueprint → live deployment
- `mcp_omni_bridge.py` — MCP context-aware compile loop
- `utah_omni_mind.py` + `utahvidia/` — sovereign local inference (ZEO-Shield, Osmotic Router)
- `omni_primitives.py` — kernel tool-calling primitives
- `omni_glass.py` — Omni-Glass real-time agentic event log
- `POST /omni/compile`, `GET /omni/status`, `GET /omni/glass`
- [Omni-Compiler](OMNI_COMPILER.md), [MCP Bridge](MCP_OMNI_BRIDGE.md), [Utah-Omni-Mind](UTAH_OMNI_MIND.md)

### Changed
- Voice `/command` — `compile` / `omni` intents route to Omni-Compiler
- `bootstrap.sh` — optional Akashic model download (`UTAH_OMNI_DOWNLOAD_MODEL=1`)
- Genesis ISO: `utah_genesis_v33.iso`
- Build: `omega-build-v33-omni-mind`
- v32.0 roadmap complete; all locale docs updated

## [32.0] — Multi-Region Witnesses & Lazarus Auto-Restore (2026-06)

### Added
- `quorum_witness.py` — multi-region witness quorum (US/EU/Oceania/Asia tie-breakers)
- `lazarus_restore.py` — Golden Master auto-restore with kexec atomic boot
- `state_diff_engine.py` — entangled state-diff sync (<1KB mesh deltas)
- `GET /witness/status`, `GET /lazarus/status`, `POST /lazarus/restore`
- [Quorum Witnesses](QUORUM_WITNESSES.md), [Lazarus Restore](LAZARUS_RESTORE.md), [State-Diff Engine](STATE_DIFF_ENGINE.md)

### Changed
- `utah_mesh_engine.py` — registry_delta broadcast when bandwidth-efficient
- `drift_detector.py` — triggers Lazarus auto-restore after kexec attempt
- `emergency_quarantine()` — schedules Lazarus clean-room restoration
- Genesis ISO: `utah_genesis_v32.iso`
- Build: `omega-build-v32-lazarus-self-healing`
- v31.0 roadmap complete; all locale docs updated

## [31.0] — Federated Quorum & PCR-Drift-Healing (2026-06)

### Added
- `dht_consensus_engine.py` — `GlobalQuoteQuorum` with 51%+ majority consensus
- `GET /quorum/consensus` — export quorum vote ledger
- `drift_detector.perform_rollback()` — kexec to last verified kernel image
- Quorum vote replication on mesh gossip (`quorum_consensus` payload)
- [Federated Quorum Consensus](QUORUM_CONSENSUS.md) documentation

### Changed
- `drift_detector.py` — automated kexec rollback after quarantine
- `utahmosphere_os.py` — quorum verify on attestation response; combined quarantine status
- `ra_tls_attest.py` — quorum verification on mesh quotes
- Genesis ISO: `utah_genesis_v31.iso`
- Build: `omega-build-v31-federated-quorum`
- v30.0 roadmap complete; all locale docs updated

## [30.0] — DHT-Federated Attestation & Drift Healing (2026-06)

### Added
- `dht_quote_registry.py` — DHT golden measurement consensus ledger
- `drift_detector.py` — continuous PCR0 monitoring + emergency quarantine
- `GET /dht/consensus` — export DHT golden registry
- `POST /dht/challenge` — swarm attestation challenge
- Swarm packets: `ATTESTATION_CHALLENGE`, `ATTESTATION_RESPONSE`, `DHT_GOLDEN_SYNC`, `QUARANTINE_NOTICE`
- `emergency_quarantine()` — cryo-stasis all containers on drift
- `stop_all_containers()` in `utah_container_runtime.py`
- [DHT-Federated Attestation](DHT_FEDERATION.md), [PCR Drift Detection](PCR_DRIFT.md)

### Changed
- `utah_swarm_protocol.py` — attestation challenge routing
- `ra_tls_attest.py` — DHT federation verify on mesh quotes
- Genesis ISO: `utah_genesis_v30.iso`
- Build: `omega-build-v30-federated-attested`
- v29.0 roadmap complete (DHT federation + PCR drift); locale docs updated

## [29.0] — Remote Attestation Infrastructure (2026-06)

### Added
- `ra_tls_guard.py` — CA pinning, X.509 TPM quote OID `1.3.6.1.4.1.99999`, UtahX ingress guard
- `quote_registry.py` — distributed hardware quote registry with purge and mesh merge
- `GET /registry/quotes` — export registered hardware fingerprints
- `POST /registry/purge` — quarantine compromised hardware (root vibe only)
- Biometric-to-TPM binding: claim registers hardware quote globally
- [Hardware Quote Registry](QUOTE_REGISTRY.md) documentation

### Changed
- `ra_tls_attest.py` — v29 build, `hardware_id`, registry replication on mesh gossip
- `utahx_proxy.py` — RA-TLS header verification before proxy
- `utah_mesh_engine.py` — vibe-bound quotes on mesh sync
- Genesis ISO: `utah_genesis_v29.iso`
- Build: `omega-build-v29-remote-attested`
- v28.0 roadmap complete (remote CA pinning + quote registry); all locale docs updated

## [28.0] — TPM-Hardened Attested (2026-06)

### Added
- `tpm_lock.py` — Vibe-Print sealed to TPM PCR0 via `tpm2_create` / `tpm2_unseal`
- `ra_tls_attest.py` — RA-TLS TPM quotes on UtahNetes mesh gossip
- `GET /attestation/quote` — peer quote endpoint
- Oceania/APAC mempool node in `tycoon_failover.py` (4-region failover)
- [RA-TLS Mesh Attestation](RA_TLS.md) documentation

### Changed
- `quantum_ledger.py` — claim seals vibe to TPM; verify checks binding
- `utah_mesh_engine.py` — RA-TLS attach + verify on mesh sync
- Genesis ISO: `utah_genesis_v28.iso`
- Build: `omega-build-v28-attested`
- v27.0 roadmap complete; all locale docs updated

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
