#!/bin/bash

LOG_FILE="ui.log"
PID_FILE="ui.pid"

if [ -f "$PID_FILE" ]; then
    if ps -p $(cat "$PID_FILE") > /dev/null; then
       echo "Stopping existing UI application (PID: $(cat "$PID_FILE"))"
       kill $(cat "$PID_FILE")
    fi
fi


nohup streamlit run app.py --server.port 4000 > "$LOG_FILE" 2>&1 & echo $! > "$PID_FILE"

echo "UI application is running. Logs: $LOG_FILE, PID: $PID_FILE"