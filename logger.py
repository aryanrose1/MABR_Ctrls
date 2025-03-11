# =============================================================
# SENSOR MONITORING & CONTROL SYSTEM WITH GUI
# -------------------------------------------------------------
# This script handles:
# 1. **Communication with multiple sensors** using Modbus RTU and Serial protocols.
# 2. **Graphical User Interface (GUI)** to display real-time sensor data.
# 3. **Background threads** for continuous sensor monitoring and data acquisition.
# 4. **Writes real-time sensor data to JSON for external use.**
#
# This system is designed for **real-time monitoring of water quality** in a
# wastewater treatment plant or similar industrial setup.
# =============================================================

from pymodbus.client.sync import ModbusSerialClient  # Modbus communication
from functools import partial  # Allows function pre-configuration
import tkinter as tk  # GUI framework
import sys, os  # System-level operations
import time  # Timing and delays
import serial  # Serial communication for sensors
import re  # Regular expressions
import datetime  # Timestamp management
import json  # Configuration file handling
import argparse  # Command-line argument parsing
import traceback  # Error handling and debugging
import threading  # Background threads for continuous sensor data updates

# --------------------------
# Sensor Data File
# --------------------------
SENSOR_DATA_FILE = "sensor_data.json"

def write_sensor_data(data):
    """Writes sensor data to a JSON file for external use."""
    with open(SENSOR_DATA_FILE, "w") as file:
        json.dump(data, file)

# --------------------------
# Sensor Data Buffer
# --------------------------
# Stores real-time readings from different sensors
log_buffer = ["-", "-", "-", "-", "-", "-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-","-"]

# Index positions for specific parameters in the log buffer
pH_idx = 1
orp_idx = 2
NH4_idx = 3
NO3_idx = 4
ODO_idx = 5
temp_idx = 6
cond_idx = 7

# Global variables for tracking system state
sonde_log_entry = ""
o2_mA = ""
disconnected_time = datetime.datetime.now()
startup = True  # Tracks first-time startup state
boot_log = True  # Determines if initial logs need to be stored
button_start = 2  # GUI layout configuration
scale_size = 18  # Font scaling for GUI

# --------------------------
# Command-line Arguments
# --------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--controller_port", help="Controller port", default=None)
parser.add_argument("--O2_port", help="Oxygen sensor port", default=None)
parser.add_argument("--sonde_port", help="Sonde sensor port", default=None)
args = parser.parse_args()

# --------------------------
# Configuration File Handling
# --------------------------
def read_config_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_config_file(file_path, config):
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=2)

config_file_path = 'config.json'
config = read_config_file(config_file_path)

# --------------------------
# Function for Mapping Sensor Values
# --------------------------
def map_value(value, input_min, input_max, output_min, output_max):
    return output_min + (value - input_min) * (output_max - input_min) / (input_max - input_min)

# --------------------------
# Sensor Classes
# --------------------------

class Sonde:
    def __init__(self, port):
        self.port = port
        self.disconnected = True
        self.serial_data = ""
        if port is not None:
            self.disconnected = False
            self.serial_port = serial.Serial(port=port, baudrate=9600, timeout=1)
            self.reader_thread = threading.Thread(target=self.read_from_port, daemon=True)
            self.reader_thread.start()
    
    def is_connected(self):
        return not self.disconnected
    
    def get_value(self):
        return self.serial_data
    
    def read_from_port(self):
        while not self.disconnected:
            try:
                if self.serial_port.in_waiting > 0:
                    self.serial_data = self.serial_port.readline().decode("utf-8").strip()
                    self.serial_port.flush()
            except:
                global disconnected_time
                disconnected_time = datetime.datetime.now()
                self.disconnected = True

class O2_sensor:
    def __init__(self, port):
        self.calibration = config['O2_sensor_calibration']
        self.port = port
        self.disconnected = True
        if port is not None:
            self.disconnected = False
            self.client = ModbusSerialClient(
                method="rtu",
                port=args.O2_port,
                baudrate=9600,
                bytesize=8,
                parity="N",
                stopbits=1,
                timeout=.2
            )
        self.oxygen_value = -1.0
        self.reader_thread = threading.Thread(target=self.loop, daemon=True)
        self.reader_thread.start()
    
    def is_connected(self):
        return not self.disconnected
    
    def get_value(self):
        return self.oxygen_value
    
    def loop(self):
        while True:
            self.get_data()
    
    def get_data(self):
        try:
            self.client.connect()
            slave_address = 5
            register_address = 7
            number_of_registers = 1
            response = self.client.read_input_registers(register_address, number_of_registers, unit=slave_address)
            if response.isError():
                print(f"Error in reading register: {response}")
                self.oxygen_value = "ERR"
            else:
                measuring_value_channel_1 = response.registers[0] * 0.001
                global o2_mA
                o2_mA = measuring_value_channel_1
                mapped_value = map_value(measuring_value_channel_1, self.calibration['current_1'], self.calibration['current_3'], self.calibration['percent_1'], self.calibration['percent_3'])
                self.oxygen_value = f"{mapped_value:.2f}"
            self.client.close()
        except:
            print("Error in reading register")
            self.disconnected = True
            self.client.close()
            self.oxygen_value = "ERR"

# JSON data writing loop
while True:
    sensor_data = {
        "pH": float(log_buffer[pH_idx]) if log_buffer[pH_idx] != "-" else 0.0,
        "ORP": float(log_buffer[orp_idx]) if log_buffer[orp_idx] != "-" else 0.0,
        "NH4": float(log_buffer[NH4_idx]) if log_buffer[NH4_idx] != "-" else 0.0,
        "NO3": float(log_buffer[NO3_idx]) if log_buffer[NO3_idx] != "-" else 0.0,
        "ODO": float(log_buffer[ODO_idx]) if log_buffer[ODO_idx] != "-" else 0.0,
        "Temperature": float(log_buffer[temp_idx]) if log_buffer[temp_idx] != "-" else 0.0
    }
    write_sensor_data(sensor_data)
    time.sleep(5)
