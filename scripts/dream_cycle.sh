#!/bin/bash
export PATH="$HOME/.bun/bin:$PATH"
set -a
if [ -f "$HOME/.hermes/.env" ]; then
    source "$HOME/.hermes/.env"
fi
set +a

log_dir="$HOME/.gbrain/logs"
mkdir -p "$log_dir"
log_file="$log_dir/dream-cron.log"

# Run the dream cycle silently, logging all output
if ! gbrain dream --stale > "$log_file" 2>&1; then
    echo "❌ Automated dream cycle failed:"
    cat "$log_file"
    exit 1
fi
