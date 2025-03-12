# =============================================================
# SENSOR MONITORING & CONTROL SYSTEM
# -------------------------------------------------------------
# This script handles:
# 1. **Communication with multiple sensors** using Modbus RTU and Serial protocols.
# 2. **Background threads** for continuous sensor monitoring and data acquisition.
# 3. **Writes real-time sensor data to SQLite for external use.**
#
# This system is designed for **real-time monitoring of water quality** in a
# wastewater treatment plant or similar industrial setup.
# =============================================================

from pymodbus.client.sync import ModbusSerialClient  # Modbus communication
import serial  # Serial communication for sensors
import time  # Timing and delays
import sqlite3  # Database handling
import threading  # Background threads for continuous sensor data updates
import json  # Configuration file handling
import argparse  # Command-line argument parsing

# --------------------------
# Database File
# --------------------------
DB_FILE = "sensor_data.db"

# --------------------------
# Initialize Database
# --------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                        timestamp TEXT,
                        tag TEXT,
                        value REAL)''')
    conn.commit()
    conn.close()

# --------------------------
# Store Sensor Data in SQLite
# --------------------------
def store_sensor_data(tag, value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (timestamp, tag, value) VALUES (datetime('now'), ?, ?)", (tag, value))
    conn.commit()
    conn.close()

# --------------------------
# Sensor Classes
# --------------------------
class Sonde:
    def __init__(self, port):
        self.port = port
        self.serial_data = ""
        if port is not None:
            self.serial_port = serial.Serial(port=port, baudrate=9600, timeout=1)
            self.reader_thread = threading.Thread(target=self.read_from_port, daemon=True)
            self.reader_thread.start()
    
    def read_from_port(self):
        while True:
            if self.serial_port.in_waiting > 0:
                self.serial_data = self.serial_port.readline().decode("utf-8").strip()
                store_sensor_data("Sonde", float(self.serial_data) if self.serial_data.replace('.', '', 1).isdigit() else 0.0)

class O2Sensor:
    def __init__(self, port):
        self.port = port
        self.client = ModbusSerialClient(method="rtu", port=port, baudrate=9600, timeout=1)
        self.reader_thread = threading.Thread(target=self.read_from_modbus, daemon=True)
        self.reader_thread.start()
    
    def read_from_modbus(self):
        while True:
            self.client.connect()
            response = self.client.read_input_registers(7, 1, unit=5)
            if not response.isError():
                value = response.registers[0] * 0.001
                store_sensor_data("O2", value)
            self.client.close()
            time.sleep(5)

# --------------------------
# Initialize Sensors
# --------------------------
sonde = Sonde("COM3")  # Replace with actual port
oxygen_sensor = O2Sensor("COM4")  # Replace with actual port

# --------------------------
# Initialize Database and Start Sensor Logging
# --------------------------
init_db()

# Keep script running
while True:
    time.sleep(1)
