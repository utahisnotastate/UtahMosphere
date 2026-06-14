# Contributing to UtahMosphere

Thank you for contributing to UtahMosphere OS. This guide covers local setup, code conventions, and how to extend the platform.

---

## Getting Started

1. Fork and clone the repository
2. Follow [Local Development Guide](docs/LOCAL_DEVELOPMENT.md)
3. Run health check: `python examples/check-node-health/health_check.py`

---

## Project Layout

| Path | Purpose |
|------|---------|
| `utahmosphere_os.py` | Kernel, HTTP gateway, mesh gossip |
| `quantum_ledger.py` | Biometric access control |
| `voice_bridge.py` | Voice → `/command` bridge |
| `utah_tycoon.py` | Payment gate daemon |
| `utah_swarm_protocol.py` | P2P swarm node |
| `flux_gui.py` | Tkinter status UI |
| `genesis_deploy.py` | Multi-process launcher |
| `docs/` | Documentation portal |
| `examples/` | Runnable API examples |
| `templates/` | Copy-paste boilerplate |
| `starter-projects/` | Forkable mini-apps |

---

## Adding a Voice Intent

1. Edit `execute_voice_intent()` in `utahmosphere_os.py`
2. Add transcript parsing branch
3. Update [API Reference](docs/API_REFERENCE.md)
4. Add recipe in [docs/recipes/voice-recipes.md](docs/recipes/voice-recipes.md)

---

## Adding an HTTP Endpoint

1. Extend `SovereignIngressMultiplexer` in `utahmosphere_os.py`
2. Document in [API Reference](docs/API_REFERENCE.md) and [Capability Matrix](docs/CAPABILITY_MATRIX.md)
3. Add example under `examples/`

---

## Code Style

- Python 3.11+ with type hints where practical
- Match existing module docstring headers and log prefix style (`[Component]`)
- Prefer stdlib; avoid heavy dependencies for core kernel
- Minimal diffs — do not refactor unrelated code in the same PR

---

## Documentation

When changing behavior:

- Update [Capability Matrix](docs/CAPABILITY_MATRIX.md) if implementation status changes
- Add or update recipes in `docs/recipes/`
- Note breaking changes in [CHANGELOG](docs/CHANGELOG.md)

---

## Pull Request Checklist

- [ ] Tested locally with `UTAH_DATA_DIR=./.utah-data`
- [ ] API/docs updated if endpoints or intents changed
- [ ] No secrets committed
- [ ] Examples run without modification

---

## License

Contributions are licensed under the MIT License (see [LICENSE](LICENSE)).
