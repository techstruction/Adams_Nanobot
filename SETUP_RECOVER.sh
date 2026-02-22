#!/bin/bash
# nanobot Dashboard Setup & Recovery Script
# Version: 2.0
# Date: 2026-02-21

set -e

echo "🚀 nanobot Dashboard Setup & Recovery Script"
echo "=============================================="
echo ""

# Configuration
NANOBOT_DIR="/Users/adam/Documents/Nanobot"
WORKSPACE_DIR="$HOME/.nanobot/workspace"
DASHBOARD_PORT="18790"
VENV_PYTHON="$NANOBOT_DIR/.venv/bin/python"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[✓]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

error() {
    echo -e "${RED}[✗]${NC} $1"
}

info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Check if we're in the right directory
check_directory() {
    if [[ ! -f "$NANOBOT_DIR/pyproject.toml" ]]; then
        error "nanobot directory not found at $NANOBOT_DIR"
        error "Please run this script from the nanobot project root or update NANOBOT_DIR"
        exit 1
    fi
    log "Found nanobot directory: $NANOBOT_DIR"
}

# Check if virtual environment exists
check_venv() {
    if [[ ! -f "$VENV_PYTHON" ]]; then
        warn "Virtual environment not found at $VENV_PYTHON"
        info "Creating virtual environment..."
        cd "$NANOBOT_DIR"
        python3 -m venv .venv
        log "Virtual environment created"
    else
        log "Virtual environment found"
    fi
}

# Install/verify dependencies
install_dependencies() {
    info "Installing/verifying dependencies..."
    cd "$NANOBOT_DIR"
    
    if command -v uv &> /dev/null; then
        uv pip install fastapi uvicorn pydantic
        log "Dependencies installed via uv"
    else
        "$VENV_PYTHON" -m pip install fastapi uvicorn pydantic
        log "Dependencies installed via pip"
    fi
}

# Stop any existing dashboard on the port
stop_existing_dashboard() {
    local pid=$(lsof -ti :$DASHBOARD_PORT 2>/dev/null || echo "")
    if [[ -n "$pid" ]]; then
        warn "Found existing dashboard on port $DASHBOARD_PORT (PID: $pid)"
        kill $pid
        sleep 2
        log "Stopped existing dashboard"
    else
        log "No existing dashboard found on port $DASHBOARD_PORT"
    fi
}

# Initialize dashboard data directory
init_dashboard_data() {
    local data_dir="$WORKSPACE_DIR/dashboard/data"
    
    if [[ ! -d "$data_dir" ]]; then
        info "Creating dashboard data directory..."
        mkdir -p "$data_dir"
    fi
    
    # Create empty data files if they don't exist
    for file in bookmarks.json chat.json tasks.json schedule.json; do
        if [[ ! -f "$data_dir/$file" ]]; then
            echo "[]" > "$data_dir/$file"
            log "Created $file"
        fi
    done
    
    log "Dashboard data ready at $data_dir"
}

# Verify dashboard files
verify_dashboard_files() {
    local template_dir="$NANOBOT_DIR/nanobot/skills/dashboard/templates"
    
    local required_files=("index.html" "script.js" "style.css")
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$template_dir/$file" ]]; then
            error "Missing dashboard file: $template_dir/$file"
            exit 1
        fi
    done
    
    log "All dashboard files verified"
}

# Start dashboard
start_dashboard() {
    log "Starting dashboard server..."
    cd "$NANOBOT_DIR"
    
    # Run in background
    nohup "$VENV_PYTHON" -m uvicorn nanobot.skills.dashboard.server:app \
        --host 0.0.0.0 \
        --port $DASHBOARD_PORT \
        --reload \
        > "$WORKSPACE_DIR/logs/dashboard.log" 2>&1 &
    
    local dashboard_pid=$!
    
    # Wait for server to start
    sleep 3
    
    # Check if it's running
    if ps -p $dashboard_pid > /dev/null; then
        log "Dashboard started successfully (PID: $dashboard_pid)"
        info "Access at: http://localhost:18790/dashboard"
        info "API health: http://localhost:18790/dashboard/api/health"
        info "Logs: $WORKSPACE_DIR/logs/dashboard.log"
        
        # Save PID
        echo $dashboard_pid > "$WORKSPACE_DIR/run/dashboard.pid"
    else
        error "Failed to start dashboard"
        error "Check logs: $WORKSPACE_DIR/logs/dashboard.log"
        exit 1
    fi
}

# Show status
show_status() {
    echo ""
    log "Dashboard Status:"
    echo "==================="
    
    local pid=$(lsof -ti :$DASHBOARD_PORT 2>/dev/null || echo "")
    if [[ -n "$pid" ]]; then
        info "Status: RUNNING (PID: $pid)"
        info "URL: http://localhost:$DASHBOARD_PORT/dashboard"
        info "API: http://localhost:$DASHBOARD_PORT/dashboard/api/health"
    else
        warn "Status: NOT RUNNING"
        info "To start: $0 start"
    fi
    
    echo ""
    info "Data location: $WORKSPACE_DIR/dashboard/data"
    info "Config: $HOME/.nanobot/config.json"
}

# Main menu
show_menu() {
    echo ""
    echo "Dashboard Setup Menu:"
    echo "======================"
    echo "1. Full setup (recommended for first run)"
    echo "2. Start dashboard only"
    echo "3. Stop dashboard"
    echo "4. Show status"
    echo "5. View logs"
    echo "6. Exit"
    echo ""
    read -p "Select option [1-6]: " choice
    
    case $choice in
        1)
            check_directory
            check_venv
            install_dependencies
            stop_existing_dashboard
            init_dashboard_data
            verify_dashboard_files
            start_dashboard
            ;;
        2)
            stop_existing_dashboard
            start_dashboard
            ;;
        3)
            stop_existing_dashboard
            ;;
        4)
            show_status
            ;;
        5)
            tail -f "$WORKSPACE_DIR/logs/dashboard.log" 2>/dev/null || error "No logs found"
            ;;
        6)
            exit 0
            ;;
        *)
            error "Invalid option"
            exit 1
            ;;
    esac
}

# Handle command line arguments
case "${1:-menu}" in
    setup)
        check_directory
        check_venv
        install_dependencies
        stop_existing_dashboard
        init_dashboard_data
        verify_dashboard_files
        start_dashboard
        ;;
    start)
        stop_existing_dashboard
        start_dashboard
        ;;
    stop)
        stop_existing_dashboard
        ;;
    status)
        show_status
        ;;
    logs)
        tail -f "$WORKSPACE_DIR/logs/dashboard.log" 2>/dev/null || error "No logs found"
        ;;
    menu)
        show_menu
        ;;
    *)
        echo "Usage: $0 [setup|start|stop|status|logs|menu]"
        exit 1
        ;;
esac

exit 0
