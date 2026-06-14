#!/usr/bin/env bash
# ==============================================================================
# UtahMosphere Golden Master Genesis ISO Builder (v26.0)
# Delegates to genesis_iso_builder.py for Alpine vmlinuz bundling.
# ==============================================================================

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${REPO_DIR}"

python3 genesis_iso_builder.py "$@"
