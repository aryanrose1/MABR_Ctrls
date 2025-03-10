# =============================================================
# sonde.py - SERIAL SENSOR COMMUNICATION SCRIPT
# -------------------------------------------------------------
# This script communicates with a water quality monitoring sensor (sonde)
# via a serial port connection. It continuously reads and prints sensor data.
#
# Key Functions:
# 1. Connects to the sonde sensor over a specified serial port.
# 2. Reads sensor values and handles disconnection issues.
# 3. Sends commands to request parameter readings from the sensor.
# 4. Prints sensor data in real-time to the terminal.
# =============================================================

from pymodbus.client.sync import ModbusSerialClient  # Used for Modbus communication (not actively used in this script)
from functools import partial  # Helps with function execution (not actively used in this script)
import tkinter as tk  # GUI library (not actively used in this script)
import sys, os  # System and OS-level interactions
import time  # Provides delay functions for sensor communication
import serial  # Handles serial communication with the sonde sensor
import re  # Regular expressions (not actively used in this script)
import datetime  # Used to track when the sensor disconnects
import json  # Handles JSON data (not actively used in this script)
import argparse, sys  # Handles command-line arguments
import traceback  # Used for error handling

# --------------------------
# Parse Command-Line Arguments
# --------------------------
# Allows users to specify the serial port where the sonde is connected.
parser = argparse.ArgumentParser()
parser.add_argument("--sonde_port", help="Specify the serial port for the sonde", default=None)
args = parser.parse_args()

# --------------------------
# Sonde Class - Manages Serial Communication
# --------------------------
class Sonde:
    """
    This class handles communication with the sonde sensor.
    It establishes a serial connection, retrieves sensor values,
    and detects disconnection issues.
    """
    def __init__(self, port):
        self.port = port  # Store the provided serial port
        self.disconnected = True  # Default state: sensor is disconnected
        
        # If a valid port is provided, establish connection
        if port is not None:
            self.disconnected = False  # Mark as connected
            self.serial_port = serial.Serial(port=args.sonde_port, baudrate=9600, timeout=1)  # Open serial port
            self.serial_port.write("0\r\n".encode())  # Send initialization command to sonde
            time.sleep(0.1)  # Short delay to allow sensor to respond

    def is_connected(self):
        """Returns True if the sonde is connected, False otherwise."""
        return not self.disconnected

    def get_value(self):
        """Reads real-time sensor data from the sonde."""
        serial_data = ""
        
        if not self.disconnected:
            try:
                # Check if data is available in the serial buffer
                if self.serial_port.in_waiting > 0:
                    serial_data = self.serial_port.readline().decode("utf-8").strip()  # Read and decode data
                    self.serial_port.flush()  # Clear serial buffer to avoid stale data
            except:
                # If an error occurs, mark the sensor as disconnected
                global disconnected_time
                disconnected_time = datetime.datetime.now()
                self.disconnected = True
                return ""  # Return empty string if sensor is disconnected
        return serial_data

    def get_para(self):
        """
        Sends a command to the sonde sensor to request its parameters.
        Returns the received sensor data.
        """
        serial_data = ""
        
        # Send command to request parameter values
        self.serial_port.write("para \r".encode())
        time.sleep(1)  # Allow time for sensor response
        
        # Read response if data is available
        if self.serial_port.in_waiting > 0:
            serial_data = self.serial_port.readline().decode("utf-8").strip()
            self.serial_port.flush()  # Clear serial buffer to avoid stale data
        
        return serial_data  # Return sensor readings

# --------------------------
# Initialize Sonde Connection
# --------------------------
sonde = Sonde(args.sonde_port)  # Create a Sonde object using the specified serial port
print("Sensor Connected:", sonde.is_connected())  # Print connection status

# --------------------------
# Continuous Data Retrieval
# --------------------------
# This loop runs indefinitely, retrieving sensor data at regular intervals.
while True:
    print("Sonde Data:", sonde.get_para())  # Print retrieved sensor data
    time.sleep(1)  # Pause for a second before requesting the next reading
