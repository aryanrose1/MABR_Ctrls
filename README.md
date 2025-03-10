# MABR_Ctrls

This project involves automating and monitoring a wastewater treatment system by integrating sensors, a data logger, and an industrial communication protocol (Modbus RTU). The system consists of:


Python scripts:
sonde.py
logger.py
modbus.py
Shell scripts:
run2.sh
get_port.sh
Configuration and documentation files:
config.json
README.md
debug.log
.python-version
Hardware design files:
backplane_rev_2.brd
backplane_rev_2.sch

These scripts are designed to monitor and control a Membrane Aerated Biofilm Reactor (MABR) in a wastewater treatment facility. They handle sensor data acquisition, logging, and communication using serial and Modbus protocols.
1. sonde.py - Sonde Sensor Communication
This script establishes a serial connection with a sonde sensor (a water quality monitoring device).
It retrieves real-time water quality parameters (e.g., pH, ammonia, nitrate levels).
Functions:
Initializes communication via a specified serial port.
Checks if the sensor is connected.
Reads and retrieves sensor data.
Detects disconnections and attempts to reconnect.
Relevance: Ensures continuous monitoring of water quality in the treatment process.
2. logger.py - Sensor Monitoring & OPC UA Integration
The core script that:
Collects data from multiple sensors (e.g., Sonde, Oxygen sensor).
Logs real-time water quality parameters.
Provides a GUI interface for monitoring.
Shares data through an OPC UA server, allowing integration with SCADA systems.
Includes:
Sonde class: Reads water quality data.
Oxygen sensor class: Uses Modbus to retrieve dissolved oxygen levels.
Data mapping: Converts raw sensor values into calibrated percentages.
Multi-threading: Runs background processes to update sensor data continuously.
Relevance: This script is essential for real-time monitoring, logging, and external system communication.
3. modbus.py - Modbus Sensor Data Retrieval & Calibration
Handles Modbus RTU communication for sensors using a serial port.
Reads raw sensor data from Modbus registers and applies calibration to obtain meaningful values.
Calibration mapping:
Converts raw electrical signals (mA) to real-world units (e.g., oxygen levels).
Uses predefined calibration points to ensure accuracy.
Relevance: Ensures precise data collection from Modbus-based sensors used in wastewater treatment.
4. run2.sh - Logger Script Automation
A Bash script that:
Detects and assigns correct serial ports for sensors.
Runs the logger script (logger.py) with detected ports.
Prints the assigned ports for debugging.
Relevance: Automates the startup process for continuous monitoring.
5. get_port.sh - USB Device Identification
Scans all connected USB devices and extracts their system paths.
Identifies:
Sonde sensor
Oxygen sensor
Arduino board (if used for control).
Outputs detected devices for use in run2.sh.
Relevance: Ensures proper device identification before launching monitoring scripts.
Conclusion
This set of scripts forms an automated sensor monitoring system for a wastewater treatment facility, ensuring:
Continuous water quality monitoring.
Automated sensor communication & calibration.
Integration with SCADA systems via OPC UA.
Efficient startup & debugging with automated scripts.


What is a GUI?
A GUI (Graphical User Interface) is a visual way for users to interact with software applications. Instead of using command-line inputs, a GUI provides buttons, text fields, graphs, and other interactive elements to make software more user-friendly.
The sonde.py script implements a GUI using Tkinter (Python’s built-in GUI library).
It provides real-time sensor data (e.g., pH, dissolved oxygen, temperature) in a clear, structured format.
Users can view and analyze sensor readings without needing to interact with raw serial data.

What is an OPC UA Server?
An OPC UA (Open Platform Communications Unified Architecture) server is a machine-to-machine communication protocol designed for industrial automation and process control. It is used to securely exchange real-time data between devices, sensors, and control systems.
The OPC UA server in logger.py gathers real-time sensor data (e.g., pH, ORP, NH₄, NO₃, ODO, temperature, etc.).
Other software applications (e.g., SCADA systems, HMIs, or data loggers) can connect to the OPC UA server to access this data in real-time.
It allows remote monitoring and control of the wastewater treatment process without directly connecting to the sensors.

Think of an OPC UA server as a translator and messenger:
Translator: It collects raw data from sensors and organizes it in a structured format.
Messenger: It allows different clients (dashboards, control systems, data loggers) to request or receive updatesfrom the sensors.

What is a Modbus RTU?
Modbus RTU (Remote Terminal Unit) is a widely used serial communication protocol in industrial automation. It allows a computer (or PLC) to communicate with sensors, actuators, and other field devices over a serial connection (e.g., RS-232, RS-485).
The modbus.py script connects to a sensor (e.g., dissolved oxygen meter) using Modbus RTU over a serial port.
It reads raw sensor values from specific registers.
It converts those values into meaningful percentages (e.g., oxygen concentration).
This data is then used for real-time monitoring and logging.
