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

# Parse command-line arguments for specifying the sonde port
parser=argparse.ArgumentParser()
parser.add_argument("--sonde_port", help="sonde port", default=None)
args=parser.parse_args()

class Sonde:
    """
    Handles communication with a water quality sensor (sonde) over a serial Modbus connection.
    """
    def __init__(self, port):
        self.port = port
        self.disconnected = True
        if port is not None:
            self.connect()
    
    def connect(self):
        """Establishes a connection with the sonde device over the specified serial port."""
        try:
            self.client = ModbusSerialClient(method='rtu', port=self.port, baudrate=9600, timeout=1)
            self.disconnected = not self.client.connect()
        except Exception as e:
            print(f"Error connecting to sonde: {e}")
            self.disconnected = True
    
    def read_data(self):
        """Reads data from the sonde device using Modbus communication."""
        if self.disconnected:
            print("Sonde is not connected.")
            return None
        
        try:
            # Example: Read holding register 0x0000, modify based on sonde's register map
            response = self.client.read_holding_registers(0x0000, 10, unit=1)
            if response.isError():
                print("Error reading from sonde")
                return None
            return response.registers
        except Exception as e:
            print(f"Error reading data: {e}")
            return None
    
    def disconnect(self):
        """Closes the connection to the sonde device."""
        if not self.disconnected:
            self.client.close()
            self.disconnected = True

# Main execution entry point
if __name__ == "__main__":
    sonde = Sonde(args.sonde_port)
    if not sonde.disconnected:
        print("Successfully connected to the sonde.")
        data = sonde.read_data()
        if data:
            print("Sonde Data:", data)
        sonde.disconnect()
    else:
        print("Failed to connect to the sonde.")
