START:

NB="$HOME/src/Adams_Nanobot/.venv/bin/nanobot"
LOG="$HOME/.nanobot/logs/gateway.log"
PIDFILE="$HOME/.nanobot/run/gateway.pid"
mkdir -p "$HOME/.nanobot/logs" "$HOME/.nanobot/run"
: > "$LOG"
nohup "$NB" gateway >>"$LOG" 2>&1 </dev/null & echo $! > "$PIDFILE"



STOP:

PIDFILE="$HOME/.nanobot/run/gateway.pid"
[ -f "$PIDFILE" ] && kill "$(cat "$PIDFILE" 2>/dev/null || true)" 2>/dev/null || true
pkill -f "nanobot gateway" 2>/dev/null || true
sleep 2
pkill -9 -f "nanobot gateway" 2>/dev/null || true




