#!/bin/bash
# Define the output file path
OUTPUT_FILE="/home/$(whoami)/log_project/system_health.csv"
# --- 1. CAPTURE CPU USAGE ---
# We use 'top' to get the idle percentage and subtract it from 100.
# 'awk' is used to extract the specific number from the text output.
CPU_IDLE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print $1}')
CPU_USAGE=$(echo "100 - $CPU_IDLE" | bc)
# --- 2. CAPTURE MEMORY USAGE ---
# We use 'free -m' to get memory in MB.
MEM_TOTAL=$(free -m | awk '/Mem:/ { print $2 }')
MEM_USED=$(free -m | awk '/Mem:/ { print $3 }')
# Calculate percentage
MEM_PERCENT=$(( 100 * MEM_USED / MEM_TOTAL ))
# --- 3. CAPTURE DISK USAGE ---
# We check the root directory '/'
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
# --- 4. TIMESTAMP ---
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
# --- 5. SAVE TO CSV ---
# If the file doesn't exist, write the header row first
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Timestamp,CPU_Percent,Mem_Percent,Disk_Percent" > "$OUTPUT_FILE"
fi
# Append the data
echo "$TIMESTAMP,$CPU_USAGE,$MEM_PERCENT,$DISK_USAGE" >> "$OUTPUT_FILE"
