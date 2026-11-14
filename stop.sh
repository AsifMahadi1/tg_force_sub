#!/usr/bin/env bash
# stop.sh — stop the force-subscribe bot.
HERE="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$HERE/bot.pid"
if [ -f "$PIDFILE" ]; then
  PID="$(cat "$PIDFILE")"
  if kill -0 "$PID" 2>/dev/null; then
    # kill the whole process group (run.sh + python child)
    kill -- -"$PID" 2>/dev/null || kill "$PID" 2>/dev/null
    echo "stopped pid $PID"
  else
    echo "not running"
  fi
  rm -f "$PIDFILE"
else
  echo "no pid file"
fi
