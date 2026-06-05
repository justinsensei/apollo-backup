#!/bin/bash
export PATH="$HOME/.bun/bin:$PATH"
set -a
if [ -f "$HOME/.hermes/.env" ]; then
    source "$HOME/.hermes/.env"
fi
set +a

echo "Starting automated gbrain dream cycle..."
gbrain dream --stale
echo "Dream cycle complete."
