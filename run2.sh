#!/bin/bash
# =============================================================
# Bash Script to Start Sensor Logger
# -------------------------------------------------------------
# This script:
# 1. Identifies and assigns the correct serial ports for various devices.
# 2. Prints the detected port assignments for debugging.
# 3. Passes the correct ports as arguments to the logger script.
# 4. Starts the logger script (`logger.py`) with the detected sensor ports.
# =============================================================

# Navigate to the working directory where the logger script is stored
cd ~/Desktop/ubuntu_logger

# -------------------------------------------------------------
# Detect Serial Ports for Connected Devices
# -------------------------------------------------------------
# The `get_port.sh` script lists available serial ports. 
# We filter the output using `grep` to find specific device names
# and extract their port names using `awk`.

OXY_PORT=$(./get_port.sh | grep FT232 | head -n1 | awk '{print $1;}')  # Detect Oxygen Sensor
ARD_PORT=$(./get_port.sh | grep Arduino | head -n1 | awk '{print $1;}')  # Detect Arduino Board
SONDE_PORT=$(./get_port.sh | grep DSCJx11A920 | head -n1 | awk '{print $1;}')  # Detect Sonde Sensor

# Print a timestamp when the script starts
echo $(date): System started

# Print detected ports for debugging
if [[ -n "$OXY_PORT" ]]; then
    echo "Oxygen Sensor Port: $OXY_PORT"
fi

if [[ -n "$ARD_PORT" ]]; then
    echo "Arduino Port: $ARD_PORT"
fi

if [[ -n "$SONDE_PORT" ]]; then
    echo "Sonde Port: $SONDE_PORT"
fi

# -------------------------------------------------------------
# Prepare Command-Line Arguments for Logger Script
# -------------------------------------------------------------
# These arguments will be passed to `logger.py` to specify which
# serial ports to use for each sensor.
controller_arg=""
o2_arg=""
sonde_arg=""

if [[ -n "$ARD_PORT" ]]; then
    controller_arg="--controller_port $ARD_PORT"
fi

if [[ -n "$OXY_PORT" ]]; then
    o2_arg="--O2_port $OXY_PORT"
fi

if [[ -n "$SONDE_PORT" ]]; then
    sonde_arg="--sonde_port $SONDE_PORT"
fi

# -------------------------------------------------------------
# Start the Logger Script
# -------------------------------------------------------------
# The script runs `logger.py` with detected ports as arguments.
# `sudo` is used to ensure it has the necessary permissions to access serial devices.

sudo python3 ./logger.py $controller_arg $o2_arg $sonde_arg

# If running in a loop, the script would wait 5 seconds before restarting
# Uncomment the lines below if you want the script to restart automatically.

# Wait for 5 seconds before the next iteration
# sleep 5
# done
