# nanobot Reboot Sequence

**DANGER ZONE:** This requires stopping nanobot

## BEFORE Reboot

1. ✅ Backup verified: ~/Documents/Nanodata/BACKUP_RELAY.sh
2. ✅ Check current state: ps aux | grep nanobot
3. ✅ Check dashboard: curl -s http://localhost:18790/dashboard/api/health

## REBOOT Commands

### Option 1: Quick Reboot (with backup)
```bash
# Backup (already done above)

# Stop
echo "Stopping nanobot..."
kill $(cat ~/.nanobot/run/gateway.pid 2>/dev/null || lsof -ti :18790)
sleep 3

# Verify stopped
if ! lsof -i :18790 >/dev/null 2>&1; then
    echo "✅ Nanobot stopped"
else
    echo "⚠️ Process still running, force killing..."
    kill -9 $(lsof -ti :18790)
fi

# Start
echo "Starting nanobot..."
cd /Users/adam/Documents/Nanobot
nohup /Users/adam/Documents/Nanobot/.venv/bin/nanobot gateway > ~/.nanobot/logs/gateway.log 2>&1 &
PID=$!
echo $PID > ~/.nanobot/run/gateway.pid

sleep 5

# Verify started
if curl -s http://localhost:18790/dashboard/api/health | grep -q "OK"; then
    echo "✅ Nanobot restarted successfully"
else
    echo "❌ Failed to restart, check logs: tail -f ~/.nanobot/logs/gateway.log"
    exit 1
fi
```

### Option 2: Use Scripts
```bash
# Use SETUP_RECOVER.sh helper
./SETUP_RECOVER.sh stop
sleep 3
./SETUP_RECOVER.sh start

# Or manual
~/Documents/Nanodata/BACKUP_RELAY.sh
cd /Users/adam/Documents/Nanobot
./SETUP_RECOVER.sh stop
./SETUP_RECOVER.sh start
```

## AFTER Reboot

1. ✅ Process running: ps aux | grep nanobot
2. ✅ Port listening: lsof -i :18790
3. ✅ API health: curl -s http://localhost:18790/dashboard/api/health
4. ✅ Dashboard: Open http://localhost:18790/dashboard
5. ✅ Skills loaded: Check logs for "Loaded skill" messages
6. ✅ Test skills: Try Apple Notes, PDF Manager, OpenCode IDE

## VERIFY New Skills

```bash
# Apple Notes
cd /Users/adam/Documents/Nanobot
nanobot agent -m "List all my Apple Notes"

# PDF Manager
nanobot agent -m "List all PDFs"

# OpenCode IDE
nanobot agent -m "Show project structure"
```

## 📊 Expected Results

### Apple Notes
- ✅ Should return list of notes from Notes.app
- ✅ If no notes: "No notes found."

### PDF Manager
- ✅ Should return PDFs in workspace
- ✅ If no PDFs: "No PDFs found."

### OpenCode IDE
- ✅ Should return project directory tree
- ✅ Should include skills/, nanobot/, workspace/

## 🔄 Current State

**Before reboot:**
- Gateway running
- Dashboard accessible
- Old skills loaded (dashboard, telegram, etc.)

**After reboot:**
- Gateway running
- Dashboard accessible
- All skills loaded (includes new Apple Notes, PDF, IDE)

## ⚠️ WARNING

- This will disconnect current session
- Telegram bot will restart
- Any in-flight commands will be lost
- Make sure to save any important conversations

## ✅ VERIFICATION DONE

When you see:
1. ✅ Backup verified
2. ✅ Process stopped
3. ✅ New process started
4. ✅ Skills loaded in logs
5. ✅ Test commands work

Then nanobot is successfully rebooted with new skills!
