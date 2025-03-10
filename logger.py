from pymodbus.client.sync import ModbusSerialClient
from functools import partial
import tkinter as tk
import sys, os
import time
import serial
import re
import datetime
import json
import argparse, sys
import traceback
import threading
from opcua import ua, Server

# Buffer to store sensor log data, initialized with placeholders
log_buffer = ["-"] * 20

# Sensor data index mapping
pH_idx = 1
orp_idx = 2
NH4_idx = 3
NO3_idx = 4
ODO_idx = 5
temp_idx = 6
conductivity_idx = 7

class Logger:
    """
    Handles data logging from wastewater treatment sensors via Modbus and OPC UA communication.
    """
    def __init__(self, port):
        self.port = port
        self.disconnected = True
        self.server = Server()
        if port is not None:
            self.connect()
    
    def connect(self):
        """Establishes a connection to the Modbus serial client."""
        try:
            self.client = ModbusSerialClient(method='rtu', port=self.port, baudrate=9600, timeout=1)
            self.disconnected = not self.client.connect()
        except Exception as e:
            print(f"Error connecting to Modbus: {e}")
            self.disconnected = True
    
    def read_sensors(self):
        """Reads data from multiple sensors and updates the log buffer."""
        if self.disconnected:
            print("Logger is not connected to Modbus.")
            return
        try:
            # Example: Read multiple registers (modify based on actual sensor register map)
            response = self.client.read_holding_registers(0x0000, 10, unit=1)
            if response.isError():
                print("Error reading sensor data")
                return
            log_buffer[pH_idx] = response.registers[0]
            log_buffer[orp_idx] = response.registers[1]
            log_buffer[NH4_idx] = response.registers[2]
            log_buffer[NO3_idx] = response.registers[3]
            log_buffer[ODO_idx] = response.registers[4]
            log_buffer[temp_idx] = response.registers[5]
            log_buffer[conductivity_idx] = response.registers[6]
        except Exception as e:
            print(f"Error reading sensor data: {e}")
    
    def start_opcua_server(self):
        """Starts an OPC UA server to provide real-time sensor data."""
        self.server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
        idx = self.server.register_namespace("MABR")
        obj = self.server.nodes.objects.add_object(idx, "SensorData")
        self.pH_node = obj.add_variable(idx, "pH", 0.0)
        self.pH_node.set_writable()
        self.server.start()
        print("OPC UA server started.")

    def disconnect(self):
        """Disconnects the Modbus client and stops the OPC UA server."""
        if not self.disconnected:
            self.client.close()
            self.disconnected = True
        self.server.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Serial port for Modbus communication", default=None)
    args = parser.parse_args()
    
    logger = Logger(args.port)
    if not logger.disconnected:
        print("Logger connected successfully.")
        logger.read_sensors()
        logger.start_opcua_server()
        time.sleep(10)  # Run for 10 seconds as a test
        logger.disconnect()
    else:
        print("Failed to connect to Modbus.")
