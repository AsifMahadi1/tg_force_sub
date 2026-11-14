#!/usr/bin/env bash
# start.sh — start the force-subscribe bot in the background.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LOG="$HERE/bot.log"
PIDFILE="$HERE/bot.pid"

[ -f "$HERE/.env" ] || { echo "!! .env missing"; exit 1; }

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "Already running (pid $(cat "$PIDFILE"))."; exit 1
fi

cd "$HERE"
nohup bash run.sh > "$LOG" 2>&1 &
echo $! > "$PIDFILE"
echo "Started force-subscribe bot (pid $(cat "$PIDFILE"))"
echo "Log: $LOG"
sleep 3; tail -6 "$LOG"
