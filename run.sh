#!/usr/bin/env bash
# run.sh — run the force-subscribe bot in a crash-loop (auto-restart).
# Pure stdlib: no venv, no pip install needed.
set -e
cd "$(dirname "$0")"
set -a
source .env
set +a
while true; do
  python3 bot.py
  echo "[runner] exited, restarting in 3s..."
  sleep 3
done
