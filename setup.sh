#!/usr/bin/env bash
# UtahMosphere v25.0 Genesis Install — delegates to bootstrap.sh
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "${DIR}/bootstrap.sh" "$@"
