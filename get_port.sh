#!/bin/bash
# =============================================================
# USB DEVICE FINDER & IDENTIFIER
# -------------------------------------------------------------
# This script scans all connected USB devices and prints their
# associated device paths along with their unique serial identifiers.
#
# Key Functions:
# 1. Finds all USB devices connected to the system.
# 2. Extracts device names and their corresponding serial identifiers.
# 3. Outputs the detected USB devices in the format: /dev/device_name - ID_SERIAL.
# =============================================================

# Loop through all USB system paths containing device information
for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
    (
        # Extract the base system path for the USB device
        syspath="${sysdevpath%/dev}"
        
        # Retrieve the device name assigned by the system
        devname="$(udevadm info -q name -p $syspath)"
        
        # Skip bus-related entries (we only need actual device paths)
        [[ "$devname" == "bus/"* ]] && exit
        
        # Extract all available properties of the device
        eval "$(udevadm info -q property --export -p $syspath)"
        
        # Skip devices without a serial identifier
        [[ -z "$ID_SERIAL" ]] && exit
        
        # Print the device path and its serial identifier
        echo "/dev/$devname - $ID_SERIAL"
    )
done
