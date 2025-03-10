# MABR Control System - Automated Wastewater Monitoring

## Overview
This project involves automating and monitoring a **wastewater treatment system** by integrating **sensors, a data logger, and an industrial communication protocol (Modbus RTU)**. The system is designed to monitor and control a **Membrane Aerated Biofilm Reactor (MABR)** by handling **sensor data acquisition, logging, and communication** using serial and Modbus protocols.

## Project Structure
### **Python Scripts**
- `sonde.py` - Sonde Sensor Communication
- `logger.py` - Sensor Monitoring & OPC UA Integration
- `modbus.py` - Modbus Sensor Data Retrieval & Calibration

### **Shell Scripts**
- `run2.sh` - Logger Script Automation
- `get_port.sh` - USB Device Identification

### **Configuration and Documentation Files**
- `config.json` - System configuration
- `README.md` - Project documentation
- `debug.log` - Log file for debugging
- `.python-version` - Python version specification

### **Hardware Design Files**
- `backplane_rev_2.brd` - Circuit board design
- `backplane_rev_2.sch` - Schematic design

---

## **Script Descriptions**
### **1. `sonde.py` - Sonde Sensor Communication**
- Establishes a **serial connection** with a **sonde sensor** (water quality monitoring device).
- Retrieves **real-time water quality parameters** (e.g., pH, ammonia, nitrate levels).
#### **Functions:**
- Initializes communication via a specified serial port.
- Checks if the sensor is connected.
- Reads and retrieves sensor data.
- Detects disconnections and attempts to reconnect.
#### **Relevance:**
Ensures continuous monitoring of water quality in the treatment process.

---

### **2. `logger.py` - Sensor Monitoring & OPC UA Integration**
This is the **core script** that:
- **Collects data** from multiple sensors (e.g., Sonde, Oxygen sensor).
- **Logs real-time water quality parameters**.
- **Provides a GUI interface** for monitoring.
- **Shares data through an OPC UA server**, allowing integration with SCADA systems.

#### **Includes:**
- **Sonde class:** Reads water quality data.
- **Oxygen sensor class:** Uses Modbus to retrieve dissolved oxygen levels.
- **Data mapping:** Converts raw sensor values into calibrated percentages.
- **Multi-threading:** Runs background processes to update sensor data continuously.
#### **Relevance:**
Essential for real-time monitoring, logging, and external system communication.

---

### **3. `modbus.py` - Modbus Sensor Data Retrieval & Calibration**
- Handles **Modbus RTU communication** for sensors using a serial port.
- Reads raw sensor data from **Modbus registers** and applies calibration to obtain meaningful values.
#### **Calibration Mapping:**
- Converts raw electrical signals (mA) to **real-world units** (e.g., oxygen levels).
- Uses predefined **calibration points** to ensure accuracy.
#### **Relevance:**
Ensures precise data collection from Modbus-based sensors used in wastewater treatment.

---

### **4. `run2.sh` - Logger Script Automation**
- Detects and assigns **correct serial ports** for sensors.
- Runs the **logger script** (`logger.py`) with detected ports.
- Prints the **assigned ports for debugging**.
#### **Relevance:**
Automates the startup process for continuous monitoring.

---

### **5. `get_port.sh` - USB Device Identification**
- Scans all **connected USB devices** and extracts their system paths.
- Identifies:
  - **Sonde sensor**
  - **Oxygen sensor**
  - **Arduino board** (if used for control)
- Outputs detected devices for use in `run2.sh`.
#### **Relevance:**
Ensures proper device identification before launching monitoring scripts.

---

## **Conclusion**
This set of scripts forms an **automated sensor monitoring system** for a wastewater treatment facility, ensuring:
- **Continuous water quality monitoring.**
- **Automated sensor communication & calibration.**
- **Integration with SCADA systems via OPC UA.**
- **Efficient startup & debugging with automated scripts.**

---

## **Additional Concepts**
### **What is a GUI?**
A **GUI (Graphical User Interface)** is a visual way for users to interact with software applications. Instead of using command-line inputs, a GUI provides **buttons, text fields, graphs, and other interactive elements** to make software more user-friendly.
- The `sonde.py` script implements a GUI using **Tkinter** (Python’s built-in GUI library).
- It provides **real-time sensor data** (e.g., pH, dissolved oxygen, temperature) in a **clear, structured format**.
- Users can **view and analyze sensor readings** without needing to interact with raw serial data.

---

### **What is an OPC UA Server?**
An **OPC UA (Open Platform Communications Unified Architecture) server** is a **machine-to-machine communication protocol** designed for **industrial automation and process control**. It is used to securely exchange **real-time data** between **devices, sensors, and control systems**.
- The **OPC UA server** in `logger.py` gathers **real-time sensor data** (e.g., pH, ORP, NH₄, NO₃, ODO, temperature, etc.).
- Other software applications (**SCADA systems, HMIs, or data loggers**) can connect to the **OPC UA server** to access this data in real-time.
- It allows **remote monitoring and control** of the wastewater treatment process without directly connecting to the sensors.

#### **Think of an OPC UA server as a translator and messenger:**
- **Translator:** It collects raw data from sensors and organizes it in a structured format.
- **Messenger:** It allows different clients (dashboards, control systems, data loggers) to request or receive updates from the sensors.

---

### **What is Modbus RTU?**
**Modbus RTU (Remote Terminal Unit)** is a widely used **serial communication protocol** in industrial automation. It allows a computer (or PLC) to communicate with **sensors, actuators, and other field devices** over a serial connection (e.g., RS-232, RS-485).
- The `modbus.py` script **connects to a sensor** (e.g., dissolved oxygen meter) using **Modbus RTU over a serial port**.
- It **reads raw sensor values** from specific **Modbus registers**.
- It **converts those values** into meaningful percentages (e.g., oxygen concentration).
- This data is then used for **real-time monitoring and logging**.

---

## **License**
This project is open-source and can be modified or extended to fit various wastewater treatment applications.

---

### **Contact**
For questions or contributions, feel free to submit an issue or pull request on GitHub.

