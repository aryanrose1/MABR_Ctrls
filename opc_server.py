import sqlite3
import time
import serial
import threading
from pymodbus.client.sync import ModbusSerialClient

# Database file
DB_FILE = "sensor_data.db"

def store_sensor_data(tag, value):
    """Stores sensor data in SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sensor_data (timestamp, tag, value) VALUES (datetime('now'), ?, ?)", (tag, value))
    conn.commit()
    conn.close()

# Sonde Sensor Class
class Sonde:
    def __init__(self, port):
        self.port = port
        self.serial_data = ""
        if port:
            self.serial_port = serial.Serial(port=port, baudrate=9600, timeout=1)
            self.reader_thread = threading.Thread(target=self.read_from_port, daemon=True)
            self.reader_thread.start()
    
    def read_from_port(self):
        while True:
            if self.serial_port.in_waiting > 0:
                self.serial_data = self.serial_port.readline().decode("utf-8").strip()
                store_sensor_data("Sonde", float(self.serial_data) if self.serial_data.replace('.', '', 1).isdigit() else 0.0)

# Oxygen Sensor Class
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

# Initialize sensors
sonde = Sonde("COM3")  # Replace with actual port
oxygen_sensor = O2Sensor("COM4")  # Replace with actual port

# Keep script running
while True:
    time.sleep(1)
